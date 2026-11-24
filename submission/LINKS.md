# Anticipatory Commerce — Team Clauduss

AgentX: The Agentic Commerce Challenge · Techfest IIT Bombay 2026–27
**Challenge 1 — Anticipatory Commerce** · Team ID **TM-3C7A31667D2**

**Code repository — https://github.com/rupaparapriyam/anticipatory-commerce**

## The team

Priyam Rupapara (leader), Nivaan Shah, Ved Patel, Manan Nagar.

## What is in this folder

| File | What it is |
|---|---|
| Abstract.pdf | 486 words, within the 500-word limit |
| Code repository | link above; `agent.py`, `reader.py`, `lexicon.py` |
| outputs-dev.jsonl | our results on the public development set |
| outputs-stress.jsonl | our results on 300 unseen-wording requests we generated |
| Demo video | 3 minutes |

## The numbers

|  | dev.jsonl | stress.jsonl (wording we never taught it) |
|---|---|---|
| Score | **44.9** (baseline 20.0) | **47.4** (baseline 11.9) |
| Accuracy | **1.000** (baseline 0.527) | **1.000** |
| Wrong commits | 4 in 300 | 4 in 300 |
| Searches per request | **1.23** (baseline 1.53) | 1.20 |

Reproduce both with `python evaluate.py --agent agent.py` and
`python evaluate.py --agent agent.py --data stress.jsonl`.
Python 3.9, standard library only. No model and no API call at run time.
