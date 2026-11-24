"""How well the reader recovers the gold filters at the last word of each request."""
import json, sys, collections
import reader

rows = [json.loads(l) for l in open("dev.jsonl") if l.strip()]
FIELDS = ("category", "colour", "size", "brand", "max_price")
wrong = collections.defaultdict(list)
ok_all = 0
for r in rows:
    got, _ = reader.read(r["words"])
    gold = r["filters"]
    bad = [f for f in FIELDS if str(got.get(f)).lower() != str(gold.get(f)).lower()]
    if bad:
        for f in bad:
            wrong[f].append((r["id"], r["text"], gold.get(f), got.get(f)))
    else:
        ok_all += 1
print(f"all five filters exactly right: {ok_all}/{len(rows)} = {ok_all/len(rows):.3f}\n")
for f in FIELDS:
    print(f"{f:11} wrong {len(wrong[f]):3}  ({1-len(wrong[f])/len(rows):.3f} right)")
print()
for f in FIELDS:
    if wrong[f] and (len(sys.argv) < 2 or sys.argv[1] in (f, "all")):
        print(f"\n===== {f} =====")
        for rid, text, g, got in wrong[f][:14]:
            print(f"  gold {g!r:16} got {got!r:16} | {text}")
