# AgentX Round 1 — what goes in the Drive folder

Due **30 November 2026, 11:59 PM IST**. Only Priyam (team leader) may submit.
Everything goes in **one** Google Drive folder, set to "Anyone with the link can view",
and the folder link is pasted in the "Submission Link" box on
https://techfest.org/competitions/agentx — that box is already open on the page.

| In the folder | File | Ready? |
|---|---|---|
| Abstract, max 500 words | `ABSTRACT.md` (486 words) — print to PDF | ready |
| Code | this whole `agentx/` folder, or a GitHub repo link | ready, repo not pushed |
| Outputs on the dev set | `outputs-dev.jsonl`, `outputs-stress.jsonl` | ready |
| 3-minute demo video | not recorded | **needs recording** |
| Architecture note | `README.md` | ready |

## What only Priyam can do

1. **Record the video.** `VIDEO.md` is a shot-by-shot script with the exact commands.
   It is a screen recording of a terminal with one voice over it, about 2:50.
2. **Decide the code link.** Either drop the `agentx/` folder straight into Drive, or
   push it to a GitHub repo and put the link in. Pushing needs Priyam's go-ahead.
3. **Upload and paste the folder link**, once all four teammates are registered and
   added, per the agreed plan.

## Checks before submitting

```
python evaluate.py --agent agent.py                        # expect SCORE 44.9
python evaluate.py --agent agent.py --data stress.jsonl    # expect SCORE 47.4
python tune.py                                             # two-fold check
```

The three data files from the starter kit (`catalogue.csv`, `dev.jsonl`, `search.py`,
`evaluate.py`) are left exactly as Rezolve shipped them, so the jury can re-run the
score without changing anything. `README-starter-kit.md` is their original README.
