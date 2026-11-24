"""Watch the agent think, one word at a time. This is what the demo video shows.

    python demo.py                                  # a few requests from dev.jsonl
    python demo.py "black Pacevo running shoes size 9 under 4000"
    python demo.py --id dev-0042
    python demo.py --tag correction --n 3
"""
import argparse
import json
import sys
import time

import agent as agent_module
from evaluate import Tools
from search import load_catalogue

CAT = {p["product_id"]: p for p in load_catalogue()}
GREEN, DIM, BOLD, RESET = "\033[32m", "\033[2m", "\033[1m", "\033[0m"


def title_of(pid):
    p = CAT.get(pid)
    return f"{p['title']} / size {p['size'] or '-'} / Rs {p['price']}" if p else pid


def play(words, target=None, pause=0.0):
    tools = Tools()
    agent = agent_module.Agent(tools)
    agent.start("demo")
    shown, commits = None, []
    print()
    for i, word in enumerate(words, 1):
        out = agent.observe(word) or {}
        said = " ".join(words[:i])
        filters = {k: v for k, v in (out.get("filters") or {}).items() if v is not None}
        # While the reading is unsettled the agent will not act on it, so say so
        # rather than showing a value the next word is about to replace.
        mark = "" if agent.settled else "  ...still listening"
        line = f"  {said}"
        print(f"{line:<62}{DIM}{filters}{mark}{RESET}")
        if out.get("commit") and out["commit"] != shown:
            shown = out["commit"]
            commits.append((i, shown))
            left = len(words) - i
            print(f"      {GREEN}-> shows {shown}: {title_of(shown)}{RESET}"
                  f"{DIM}  ({left} words before the end){RESET}")
        if pause:
            time.sleep(pause)
    final = agent.finish() or shown
    print(f"\n  {BOLD}final answer {final}: {title_of(final)}{RESET}")
    if target:
        wrong = [c for _, c in commits if c != target]
        print(f"  target {target} -> {'right' if final == target else 'WRONG'}"
              f", {len(wrong)} wrong commit(s), {tools.searches} search(es)")
    return final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("request", nargs="*", help="a request to type in, in quotes")
    ap.add_argument("--id", help="one request from dev.jsonl by id")
    ap.add_argument("--tag", help="plain, correction, late_constraint or code_mixed")
    ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--data", default="dev.jsonl")
    ap.add_argument("--pause", type=float, default=0.0, help="seconds per word, for recording")
    args = ap.parse_args()

    if args.request:
        play(" ".join(args.request).split(), pause=args.pause)
        return
    rows = [json.loads(l) for l in open(args.data) if l.strip()]
    if args.id:
        rows = [r for r in rows if r["id"] == args.id]
    elif args.tag:
        rows = [r for r in rows if (args.tag in r["tags"])
                or (args.tag == "plain" and not r["tags"])][:args.n]
    else:
        rows = rows[:args.n]
    if not rows:
        sys.exit("no such request")
    for r in rows:
        print(f"\n{BOLD}{r['id']}{RESET}  {DIM}{', '.join(r['tags']) or 'plain'}{RESET}")
        play(r["words"], r["target"], args.pause)


if __name__ == "__main__":
    main()
