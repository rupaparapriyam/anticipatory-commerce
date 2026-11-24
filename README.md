# Anticipatory Commerce — Team Clauduss

AgentX, Techfest IIT Bombay 2026–27, Challenge 1.
Team ID TM-3C7A31667D2. Members: Priyam Rupapara (leader), Nivaan Shah, Ved Patel, Manan Iyer.

A shopping request arrives one word at a time. This agent reads it as it comes, and
shows the product the moment the words so far can only mean one thing.

```
python evaluate.py --agent agent.py            # score it on dev.jsonl
python demo.py --tag correction --n 2          # watch it think, word by word
python make_stress.py > stress.jsonl           # build the unseen-wording set
python evaluate.py --agent agent.py --data stress.jsonl
python tune.py                                 # two-fold check on the two constants
```

Python 3.9, standard library only. Nothing to install. No model and no API call at
run time.

## Results

| | dev.jsonl | stress.jsonl (unseen wording) |
|---|---|---|
| **Score** | **44.9** (baseline 20.0) | **47.4** (baseline 11.9) |
| Accuracy | 1.000 (baseline 0.527) | 1.000 |
| Wrong commits | 4 in 300 | 4 in 300 |
| Earliness | 1.47 words, 11.2% of the request | 1.64 words, 15.2% |
| Searches per request | 1.23 (baseline 1.53) | 1.20 |
| Speed | 1,141 requests/second on one core, 0.066 ms per word, p95 0.27 ms | |

`outputs-dev.jsonl` and `outputs-stress.jsonl` hold one line per request, as the kit's
`--log` writes them.

## How it works

Three files, each with one job.

**`lexicon.py` — the words.** The catalogue holds only 16 categories, 16 colours, 18
brands and 18 sizes, but a shopper reaches for far more words than that. This file maps
every phrase to the one value the catalogue stores: "runners", "jogging shoes" and
"sports shoes" all mean running shoes; "navy blue" means navy, never blue; "kaala" and
"jet black" mean black; "saadhe teen hazaar" and "3.5k" both mean 3500. It also holds
the words that open a correction, and the words that announce a price or a size.

**`reader.py` — the reading.** On every word the whole request so far is read again.
That is cheap at this length and it keeps one rule in one place: **for each field, the
last thing the shopper said wins.** That single rule handles corrections ("black, oops,
grey" gives grey) and constraints that arrive late ("… and in blue" adds blue) without
treating them as separate cases. Longest phrases match first, numbers are read from
digits or from words in English and Hindi, and a number is read as a size or as a price
ceiling from the words around it.

The reader also reports whether its reading is **settled**. It is not settled while the
last word could still grow — "navy" into "navy blue", "size 6" into "size 6 UK", "one
thousand five" into "one thousand five hundred" — or while the request ends on a word
plainly waiting for the next one, like "under" or "up to". An unsettled reading is
never acted on.

**`agent.py` — the judgement.** It commits when exactly one product matches.

### Why committing on uniqueness is safe, not a gamble

The target is the product that satisfies the shopper's **complete** set of filters.
Every filter stated so far is part of that complete set. So the target always sits
inside the set of products matching the words heard so far. If exactly one product is
in that set, it **must** be the target.

So uniqueness is a proof, not a guess, and it is the earliest moment an honest agent
can commit. It also explains why a constraint arriving late can never hurt: it only
removes products, and the target is never among them. In 300 development requests and
300 unseen-wording requests, not one wrong commit came from a late constraint.

### The one thing that breaks the proof

A correction says a filter already used was never wanted, which makes the earlier
reading wrong rather than incomplete. Corrections are not random: in all 55 correction
requests in `dev.jsonl`, the correction opens with a word from a small set — *no,
sorry, make, wait, actually, I, oops, or, nahi, not, uh, um, hmm, matlab*. The agent
therefore waits in the two places where a correction is likely:

- for 1 word when the proof lands on a word that closes a clause, since "size 8," is
  where "I mean size 7" tends to follow;
- for 4 words after any of those opening words is heard.

Waiting only there is what makes waiting cheap. Everywhere else it commits at once.
Both numbers were chosen by the two-fold check in `tune.py`: each half of the data
picks the same pair on its own, and the held-out score matches the tuned score, so they
are not fitted to this data.

### Keeping searches down

Every search costs score, so the agent pays for as few as possible — 1.23 per request,
below the baseline's 1.53, while committing early and getting every answer right.

It looks a product up only when the reading has settled, has actually changed, and
holds at least a category, a size and either a colour or a brand, which is the smallest
combination that ever picks out a single product. Then two facts about search let it
reuse what it has already paid for. Adding a filter only ever removes products. And a
search that returns fewer products than it asked for has listed **every** product that
matches, so the matches for any tighter reading are exactly the ones in that list which
still fit. Where that leaves one product, it is the only one and no second search is
needed. Where it leaves several, ranking matters, so the agent pays.

If nothing matches at the end, part of the reading must be wrong, and the agent drops
the least reliable parts in turn — price, then brand, colour, size. This fires on 6 of
300 requests and never on a request whose answer exists.

## Honest limits

- The vocabulary was written while reading `dev.jsonl`, so a strong score there proves
  less than it looks. `stress.jsonl` is the answer to that: it is built from the
  catalogue with deliberately different wording, including category words, correction
  phrases and number forms the lexicon does **not** contain. Accuracy stays at 1.000;
  the category is read correctly 96% of the time there, and the full-text ranking
  recovers the rest.
- 4 wrong commits remain on each set. Each is a correction whose opening word arrives
  after the agent has already spoken, and no rule that reads only the words so far can
  prevent all of them.
- The earliness ceiling in this data is low: 16.3% of the request on `dev.jsonl` even
  for an agent told the answer in advance. The agent reaches 11.2% of the request, or
  69% of that ceiling.
- A spoken request would need the words segmented before this runs. Nothing here
  depends on text, but we have not built that part.
