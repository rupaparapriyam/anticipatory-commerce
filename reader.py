"""Reads a shopping request, one word at a time, into catalogue filters.

The whole prefix is re-read on every word. That costs nothing at this length and it
keeps one rule in one place: for each field, the last thing the shopper said wins.
That single rule handles both corrections ("black, oops, grey" -> grey) and
constraints that arrive late ("... and in blue" -> blue).

The reader also reports whether its reading is settled. While the last word could still
grow into a longer phrase ("navy" -> "navy blue") or a longer number ("one thousand
five" -> "one thousand five hundred"), the reading is provisional and the agent waits.
"""
import re

from lexicon import (BRAND, BUDGET_CUES_AFTER, BUDGET_CUES_BEFORE, CATEGORY, COLOUR,
                     HINDI_HALF, HINDI_SPECIAL, HINDI_UNITS, LETTER_SIZE, NUMBER_SIZE,
                     SCALES, SHOE_CATEGORIES, SHOE_SIZES, SIZE_CUES,
                     SIZELESS_CATEGORIES, TENS, UNITS, WAIST_CATEGORIES, WAIST_SIZES)

FIELDS = ("category", "colour", "size", "brand", "max_price")

# Single letters that are a size only beside a size cue; "xs"/"xl"/"xxl" are safe alone.
AMBIGUOUS_LETTERS = {"s", "m", "l"}
NUMBER_WORDS = (set(UNITS) | set(TENS) | set(SCALES) | set(HINDI_UNITS)
                | set(HINDI_HALF) | set(HINDI_SPECIAL))

_ALL_PHRASES = tuple(set(CATEGORY) | set(COLOUR) | set(BRAND) | set(LETTER_SIZE)
                     | set(NUMBER_SIZE) | set(BUDGET_CUES_BEFORE) | set(SIZE_CUES))
_PHRASE_WORDS = tuple(p.split() for p in _ALL_PHRASES if " " in p)
_BREAKS = ".,;!?"          # a number does not run past the end of a clause


def clean(word):
    """Lower-case a word and strip the punctuation a shopper leaves on it."""
    return re.sub(r"^[^\w₹.]+|[^\w]+$", "", word.lower())


def prepare(raw_words):
    """Clean each word, and note which words ended a clause.

    Returns (tokens, ends_clause) of the same length; blank tokens are dropped.
    """
    toks, ends = [], []
    for w in raw_words:
        t = clean(w)
        if not t:
            continue
        toks.append(t)
        ends.append(bool(w) and w.rstrip()[-1:] in _BREAKS)
    return toks, ends


def _read_digits(tok):
    """'4,500' -> 4500, '2.5k' -> 2500, '₹1500' -> 1500. None if it is not a number."""
    t = tok.replace("₹", "")
    t = re.sub(r"^(rs\.?|inr)", "", t).replace(",", "")
    m = re.fullmatch(r"(\d+(?:\.\d+)?)(k)?", t)
    if not m:
        return None
    val = float(m.group(1))
    if m.group(2) == "k":
        val *= 1000
    return int(round(val))


def _read_spelled(toks, ends, i):
    """Read a spelled-out number at toks[i]. Returns (value, next_i, may_continue)."""
    total, current, half, seen = 0, 0.0, 0.0, False
    j = i
    while j < len(toks):
        t = toks[j]
        if t in HINDI_HALF:
            half = HINDI_HALF[t]
        elif t in UNITS:
            current += UNITS[t]
        elif t in TENS:
            current += TENS[t]
        elif t in HINDI_SPECIAL:
            current += HINDI_SPECIAL[t]
        elif t in HINDI_UNITS:
            current += HINDI_UNITS[t]
        elif t in SCALES:
            total += (current + half if current + half else 1) * SCALES[t]
            current, half = 0.0, 0.0
        else:
            break
        seen = True
        j += 1
        if ends[j - 1]:        # a comma or full stop closes the number
            break
    if not seen:
        return None, i, False
    value = int(round(total + current + half))
    may_continue = j >= len(toks) and not ends[j - 1]
    return value, j, may_continue


def _match_phrase(toks, i, table):
    """Longest phrase in `table` starting at toks[i]. Returns (value, length)."""
    for span in (4, 3, 2, 1):
        if i + span <= len(toks):
            phrase = " ".join(toks[i:i + span])
            if phrase in table:
                return table[phrase], span
    return None, 0


def _cue_at(toks, start, end, cues):
    """Is any cue phrase wholly inside toks[start:end]?"""
    start = max(0, start)
    for span in (3, 2, 1):
        for k in range(start, min(end, len(toks)) - span + 1):
            if " ".join(toks[k:k + span]) in cues:
                return True
    return False


def open_phrase(toks):
    """Could the words at the end of the prefix be the start of a longer phrase?

    "navy" may still become "navy blue", "extra" may become "extra large". While that
    is possible the reading is provisional, so the agent waits for the next word
    rather than acting on a value the next word may replace.
    """
    for span in (1, 2, 3):
        if span > len(toks):
            break
        tail = toks[len(toks) - span:]
        for words in _PHRASE_WORDS:
            if len(words) > span and words[:span] == tail:
                return True
    return False


def _dangling(toks, ends):
    """Does the prefix end on a word that is plainly waiting for the next one?

    "under", "up to", "size" and "waist" all announce a value that has not arrived,
    and a bare shoe size may still be followed by its unit ("size 6" -> "size 6 UK").
    A reading that ends this way is not finished, whatever it currently says.
    """
    if not toks:
        return True
    if ends[-1]:                      # a comma or full stop: the clause is closed
        return False
    for span in (1, 2, 3):
        if span <= len(toks):
            tail = " ".join(toks[len(toks) - span:])
            if tail in BUDGET_CUES_BEFORE or tail in SIZE_CUES:
                return True
    last = toks[-1]
    if (last in SHOE_SIZES or last in WAIST_SIZES or last in NUMBER_SIZE) \
            and _cue_at(toks, len(toks) - 3, len(toks) - 1, SIZE_CUES):
        return True                   # "size 6" may become "size 6 UK"
    return False


def read(raw_words):
    """Read a prefix of the request. Returns (filters, settled)."""
    toks, ends = prepare(raw_words)
    mentions = {f: [] for f in FIELDS}
    numbers = []
    i, open_number = 0, False

    while i < len(toks):
        tok = toks[i]
        digits = _read_digits(tok)
        if digits is not None:
            numbers.append((i, digits, i + 1))
            i += 1
            continue
        if tok in NUMBER_WORDS and tok not in LETTER_SIZE:
            val, nxt, may_continue = _read_spelled(toks, ends, i)
            if val is not None:
                numbers.append((i, val, nxt))
                open_number = open_number or may_continue
                i = nxt
                continue
        for table, field in ((CATEGORY, "category"), (COLOUR, "colour"),
                             (BRAND, "brand"), (LETTER_SIZE, "size")):
            value, span = _match_phrase(toks, i, table)
            if value is None:
                continue
            if field == "size" and span == 1 and tok in AMBIGUOUS_LETTERS \
                    and not _cue_at(toks, i - 1, i + 2, SIZE_CUES):
                continue
            mentions[field].append((i, value))
            i += span
            break
        else:
            i += 1

    category = max(mentions["category"])[1] if mentions["category"] else None
    number_positions = [pos for pos, _, _ in numbers]

    def no_number_between(a, b):
        return not any(a < p < b for p in number_positions)

    # Decide for each number whether it names a size or caps the price.
    for idx, (pos, value, after) in enumerate(numbers):
        text_size = str(value)
        if category in SHOE_CATEGORIES:
            plausible_size = text_size in SHOE_SIZES
        elif category in WAIST_CATEGORIES:
            plausible_size = text_size in WAIST_SIZES
        elif category in SIZELESS_CATEGORIES:
            plausible_size = False
        else:
            plausible_size = text_size in SHOE_SIZES or text_size in WAIST_SIZES

        # "size 9", "9 uk", "uk 10", "waist 36", "das number": a cue right beside it.
        size_cue = _cue_at(toks, pos - 2, pos, SIZE_CUES) or _cue_at(toks, after, after + 2, SIZE_CUES)
        # "under 2000": the nearest cue before it, with no other number in between.
        pre = any(_cue_at(toks, k, k + 3, BUDGET_CUES_BEFORE) and no_number_between(k, pos)
                  for k in range(max(0, pos - 4), pos))
        post = _cue_at(toks, after, after + 3, BUDGET_CUES_AFTER)

        if size_cue and plausible_size:
            mentions["size"].append((pos, text_size))
        elif pre or post:
            mentions["max_price"].append((pos, value))
        elif plausible_size and value < 100:
            mentions["size"].append((pos, text_size))
        elif value >= 100:
            mentions["max_price"].append((pos, value))

    # A size spelled out in words: "size eight" -> 8, "das number" -> 10.
    for pos, tok in enumerate(toks):
        if tok not in NUMBER_SIZE:
            continue
        if not _cue_at(toks, pos - 2, pos + 3, SIZE_CUES):
            continue
        if any(_cue_at(toks, k, k + 3, BUDGET_CUES_BEFORE) for k in range(max(0, pos - 3), pos)):
            continue
        mentions["size"].append((pos, NUMBER_SIZE[tok]))

    filters = {f: (max(mentions[f])[1] if mentions[f] else None) for f in FIELDS}
    if filters["category"] in SIZELESS_CATEGORIES:
        filters["size"] = None

    settled = not open_phrase(toks) and not open_number and not _dangling(toks, ends)
    return filters, settled
