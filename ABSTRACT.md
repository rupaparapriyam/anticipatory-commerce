# Anticipatory Commerce: commit when the words prove the product

**Team Clauduss** (TM-3C7A31667D2) — Priyam Rupapara, Nivaan Shah, Ved Patel, Manan Iyer. AgentX Challenge 1.

**The idea.** Most shopping assistants guess early and hope. Ours never guesses. The
wanted product satisfies the shopper's complete request, so every word so far is part
of that request, and the wanted product is always among those still matching. The
instant exactly one product matches, it *must* be the right one. Committing early
becomes a proof, not a gamble, and it is the earliest moment an honest agent can act.
It also shows why a late constraint — "oh, and in blue" — can never mislead us: it only
removes products, never the right one.

**What breaks it.** A correction is different: "size 8, I mean size 7" says a filter we
already used was never wanted. Every correction in the data opens with one of a small
set of words — *no, sorry, wait, actually, make, I, oops, or, nahi, matlab*. So the
agent waits where corrections live: one word when the proof lands on a comma or full
stop, four after one of those openers. Waiting only there keeps it cheap; elsewhere it
answers at once.

**Build summary.** Three small Python files, standard library only. A lexicon maps the
many ways people speak onto the 16 categories, 16 colours, 18 brands and 18 sizes the
catalogue holds — "runners" to running shoes, "navy blue" to navy and never blue,
"kaala" to black, "saadhe teen hazaar" and "3.5k" both to 3500. A reader re-reads the
request on every word under one rule, that the last thing said about a field wins,
handling corrections and late constraints together. It also reports when a reading is
unsettled — "navy" may become "navy blue", "under" still awaits its number — and an
unsettled reading is never acted on. Searches cost score, so the agent reuses them:
adding a filter only removes products, and a search returning fewer rows than it asked
for has listed them all, so tighter readings are answered from one already paid for.

**Results.** On the 300 development requests: score **44.9** against the baseline's
20.0, accuracy **1.000** against 0.527, all five filters right on every request, 4
wrong commits in 300, and **1.23 searches** per request against the baseline's 1.53.
Our vocabulary was written while reading that data, so we also built 300 requests from
the catalogue in deliberately unfamiliar wording, including words the lexicon does not
contain. Accuracy stays **1.000** and the score rises to 47.4. The two waiting
constants survive a two-fold test: each half of the data picks the same pair alone.

**Cost and scale.** No model and no API call at run time. One core serves **1,141
requests per second** at 0.066 ms per word, p95 0.27 ms, in 21 MB. Run cost is
effectively zero: one small cloud instance covers millions of requests a day.
