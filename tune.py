"""Two-fold check that the two waiting numbers are not fitted to this data.

Tunes HOLD_AFTER_CLAUSE and HOLD_AFTER_CUE on one half of dev.jsonl and scores the
other half with them, both ways round. If the chosen pair is picking up something real
about how people talk, the held-out score is close to the tuned one.
"""
import importlib
import json
import os

import evaluate as ev

requests = [json.loads(l) for l in open("dev.jsonl") if l.strip()]
fold_a = requests[0::2]
fold_b = requests[1::2]
GRID = [(c, q) for c in (0, 1, 2, 3) for q in (2, 3, 4, 5)]


def score(rows, clause, cue):
    os.environ["AX_HOLD_CLAUSE"] = str(clause)
    os.environ["AX_HOLD_CUE"] = str(cue)
    import agent
    importlib.reload(agent)
    return ev.summarise(ev.run(agent.Agent, rows)[0])["score"]


def best_on(rows):
    return max(GRID, key=lambda cq: score(rows, *cq))


for name, tune_rows, test_rows in (("A->B", fold_a, fold_b), ("B->A", fold_b, fold_a)):
    clause, cue = best_on(tune_rows)
    print(f"{name}: tuned clause={clause} cue={cue} "
          f"| tuned half {score(tune_rows, clause, cue):.1f} "
          f"| held-out half {score(test_rows, clause, cue):.1f} "
          f"| held-out with shipped (1,4) {score(test_rows, 1, 4):.1f}")
