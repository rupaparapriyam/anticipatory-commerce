"""An anticipatory shopping agent.

It reads the request as it arrives (reader.py) and commits the moment the words so far
can only mean one product.

Why that is safe. The target is the product satisfying the shopper's complete set of
filters. Every filter stated so far belongs to that complete set, so the target always
lies inside the set of products matching the words so far. If exactly one product
matches, it must be the target. Uniqueness is therefore a proof, not a guess, and it is
the earliest moment an honest agent can commit.

One thing breaks the proof: a correction, which says a filter already used was never
wanted. Corrections are not random. They arrive as a fresh clause right after the
clause that stated the mistaken value ("size 8, I mean size 7"). So the agent holds its
commit for a couple of words when uniqueness lands on the end of a clause, and holds
again whenever a word that commonly opens a correction has just been said. Everywhere
else it commits at once, which is most of the time.

Searches are counted, so it looks products up only when the reading has settled, has
changed, and is specific enough that one product could remain.
"""
import os

from lexicon import SIZELESS_CATEGORIES
from reader import FIELDS, read

# Words that commonly open a correction. Their presence buys a short wait, not a verdict.
# Words that open a correction. "i" and "or" are in the set because a correction
# often starts "I mean ..." or "or rather ...", and one word is all we have to go on.
RETRACT_CUES = {"oops", "sorry", "wait", "hmm", "no", "nope", "nahi", "nahin",
                "actually", "rather", "mean", "meant", "scratch", "instead",
                "correction", "um", "uh", "er", "change", "make", "i", "or",
                "matlab", "balki", "galat"}
CLAUSE_END = ".,;!?"

# How long to sit on a proven answer before showing it, in words. Tuned on dev.jsonl.
# DEFER buys the chance to see a correction open; HOLD_AFTER_CUE is how long a
# correction opener keeps the agent quiet.
GATE_STRICT = os.environ.get("AX_GATE", "strict") == "strict"
DEFER = int(os.environ.get("AX_DEFER", "0"))
HOLD_AFTER_CUE = int(os.environ.get("AX_HOLD_CUE", "4"))
# A word that closes a clause is the usual seat of a correction ("size 8, I mean 7"),
# so a proof that lands on one waits this many words. Waiting only there is what makes
# the wait cheap: elsewhere the agent commits at once.
HOLD_AFTER_CLAUSE = int(os.environ.get("AX_HOLD_CLAUSE", "1"))


class Agent:
    # How many products a search asks for. A search costs the same whatever K is, and a
    # result shorter than K is a complete list, which later words can be filtered
    # against without paying again.
    K = int(os.environ.get("AX_K", "40"))

    def __init__(self, tools):
        self.tools = tools

    # ------------------------------------------------------------------ per request
    def start(self, request_id):
        self.raw = []
        self.filters = {f: None for f in FIELDS}
        self.settled = False
        self.last_searched = None
        self.last_hits = []
        self.paid = []               # (filters, hits) for every search already paid for
        self.committed = None
        self.hold_until = 0          # no commit before this many words have been heard
        self.proved = None           # (product, words heard when it was first proved)

    def observe(self, word):
        self.raw.append(word)
        seen = len(self.raw)
        bare = word.lower().strip(CLAUSE_END + " '\"")
        if bare in RETRACT_CUES:
            self.hold_until = max(self.hold_until, seen + HOLD_AFTER_CUE)

        self.filters, self.settled = read(self.raw)
        out = {"filters": dict(self.filters), "confidence": self._confidence()}

        if self.settled and self._specific_enough() and self._changed():
            self._lookup()

        if len(self.last_hits) == 1 and self.settled:
            product = self.last_hits[0]["product_id"]
            if not self.proved or self.proved[0] != product:
                self.proved = (product, seen)
            # Wait DEFER words before showing it. Every correction in the data opens
            # with a word from RETRACT_CUES, so those words are the thing worth
            # waiting for: if one arrives the proof is void and the wait restarts.
            if word.rstrip()[-1:] in CLAUSE_END:
                self.hold_until = max(self.hold_until, seen + HOLD_AFTER_CLAUSE)
            old_enough = seen - self.proved[1] >= DEFER
            if old_enough and seen >= self.hold_until and product != self.committed:
                self.committed = product
                out["commit"] = product
        else:
            self.proved = None
        return out

    def finish(self):
        """The request is complete: answer on the whole of it."""
        if self._changed() or not self.last_hits:
            self._lookup()
        if self.last_hits:
            return self.last_hits[0]["product_id"]
        return self._relax()

    # ------------------------------------------------------------------ searching
    def _filter_args(self):
        return {k: v for k, v in self.filters.items() if v is not None}

    def _changed(self):
        return self._filter_args() != self.last_searched

    def _specific_enough(self):
        """Is the reading worth a search yet?

        A category narrows the catalogue from 1,074 products to at most 89, which one
        search returns in full. Every later word is then matched against that list for
        free, so the agent sees the moment one product remains without paying again.
        Below a category the result would be too long to come back whole, and paying
        for it would buy nothing.
        """
        f = self.filters
        if not f["category"]:
            return False
        if GATE_STRICT:
            if f["category"] not in SIZELESS_CATEGORIES and not f["size"]:
                return False
            return bool(f["colour"] or f["brand"])
        return True

    @staticmethod
    def _covers(old, new):
        """Is `old` a looser version of `new`? (every old filter repeated in new)"""
        if any(new.get(k) != v for k, v in old.items() if k != "max_price"):
            return False
        if "max_price" in old:
            return "max_price" in new and new["max_price"] <= old["max_price"]
        return True

    @staticmethod
    def _still_fits(product, args):
        for key in ("category", "colour", "size", "brand"):
            if key in args and str(product.get(key, "")).lower() != str(args[key]).lower():
                return False
        if "max_price" in args and product["price"] > args["max_price"]:
            return False
        return True

    def _reuse(self, args):
        """Answer from a search already paid for, where that is sound.

        Adding a filter can only remove products, never add one. A search that came
        back with fewer than K products therefore listed every product matching those
        looser filters, so the products matching a tighter set are exactly the ones in
        that list which still fit. Where that leaves one product, it is the only one,
        and no second search is needed. Where it leaves several, the ranking matters
        and the agent pays for a fresh search.
        """
        for old, hits, complete in self.paid:
            if not self._covers(old, args):
                continue
            if not hits:
                return []
            if not complete:
                continue
            kept = [h for h in hits if self._still_fits(h, args)]
            if len(kept) <= 1:
                return kept
        return None

    def _lookup(self):
        args = self._filter_args()
        reused = self._reuse(args)
        if reused is not None:
            self.last_hits, self.last_searched = reused, args
            return
        hits = self.tools.search(" ".join(self.raw), args, k=self.K)
        self.last_hits, self.last_searched = hits, args
        self.paid.append((dict(args), list(hits), len(hits) < self.K))

    def _relax(self):
        """Nothing matched, so part of the reading is wrong. Drop the least reliable
        parts in turn: price first, then brand, colour, size."""
        base = self._filter_args()
        query = " ".join(self.raw)
        for drop in ("max_price", "brand", "colour", "size", "category"):
            base.pop(drop, None)
            hits = self.tools.search(query, base, k=1)
            if hits:
                return hits[0]["product_id"]
        return None

    # ------------------------------------------------------------------ judgement
    def _confidence(self):
        """How much of the reading is pinned down, 0 to 1. Reported for analysis."""
        f = self.filters
        have = sum(1 for k in ("category", "colour", "size", "brand") if f[k])
        if f["category"] in SIZELESS_CATEGORIES:
            have += 1
        score = have / 4
        if not self.settled:
            score *= 0.5
        return round(min(1.0, score), 2)
