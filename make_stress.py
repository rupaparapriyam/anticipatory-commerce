"""Build a stress set: the same catalogue, deliberately unfamiliar wording.

dev.jsonl is the only labelled data in the kit, and the agent's vocabulary was written
while looking at it, so a good score there proves less than it seems. This script
writes requests in wordings dev.jsonl does not use -- including category words,
correction phrases and number forms the agent's vocabulary does NOT contain -- and
works out the answer from the catalogue itself, so the labels are not guesses.

    python make_stress.py > stress.jsonl
    python evaluate.py --agent agent.py --data stress.jsonl
"""
import json
import random

from search import load_catalogue, search

random.seed(20261124)
CAT = load_catalogue()

# Wordings chosen to be unlike dev.jsonl. Those marked # new are not in lexicon.py
# either, so they test what happens when a word is genuinely unknown.
CATEGORY_WORDS = {
    "running shoes": ["sports shoes", "road-running shoes", "marathon shoes"],
    "sneakers": ["canvas shoes", "lifestyle shoes", "plimsolls"],
    "sandals": ["sliders", "flip flops", "open-toe sandals"],
    "t-shirts": ["crewneck", "polo tee", "half sleeve tee"],
    "shirts": ["button down", "office shirt", "formal shirts"],
    "hoodies": ["pullover", "zip hoodie", "hoody"],
    "jackets": ["windcheater", "bomber jacket", "puffer"],
    "jeans": ["denim pants", "jeans pant", "jean"],
    "track pants": ["sweat pants", "jogger pants", "tracks"],
    "kurtas": ["kurti", "ethnic top", "kurta top"],
    "dresses": ["gown", "frock", "midi dress"],
    "backpacks": ["haversack", "laptop bag", "school bag"],
    "caps": ["baseball cap", "snapback", "topi"],
    "headphones": ["earbuds", "over ear headphones", "ear phones"],
    "watches": ["hand watch", "analog watch", "wrist watch"],
    "wallets": ["purse", "card holder", "batua"],
}
COLOUR_WORDS = {
    "black": ["jet black", "black"], "white": ["off white", "white"],
    "navy": ["midnight blue", "navy"], "blue": ["royal blue", "blue"],
    "grey": ["charcoal", "grey"], "olive": ["army green", "olive"],
    "green": ["bottle green", "green"], "red": ["crimson", "red"],
    "maroon": ["burgundy", "maroon"], "beige": ["khaki", "beige"],
    "brown": ["chocolate", "brown"], "yellow": ["mustard", "yellow"],
    "pink": ["blush", "pink"], "tan": ["camel", "tan"],
    "gold": ["rose gold", "gold"], "silver": ["silver"],
}
LETTER_WORDS = {"XS": ["x-small", "extra small"], "S": ["sm", "small"],
                "M": ["md", "medium"], "L": ["lg", "large"],
                "XL": ["x-large", "extra large"], "XXL": ["xx-large", "double xl"]}
BUDGET = ["or less", "or below", "at most", "no more than", "cheaper than"]
CORRECT = ["scratch that", "my bad", "hold on", "belay that", "on second thought",
           "sorry", "i mean", "make that", "no wait"]      # some are new
HINDI = ["mujhe {} chahiye", "{} dikhao na", "bhaiya {} dikhaiye", "{} milega kya"]


def size_phrase(product):
    s = product["size"]
    if not s:
        return ""
    if s in LETTER_WORDS:
        return random.choice([f"size {random.choice(LETTER_WORDS[s])}",
                              f"{random.choice(LETTER_WORDS[s])} size"])
    if s in {"6", "7", "8", "9", "10", "11"}:
        return random.choice([f"size {s} UK", f"UK {s}", f"size {s}"])
    return random.choice([f"waist {s}", f"size {s}", f"{s} waist"])


def budget_phrase(price):
    cap = ((price + 499) // 500) * 500
    style = random.randrange(4)
    if style == 0:
        return f"{cap} {random.choice(BUDGET)}", cap
    if style == 1:
        return f"under {cap / 1000:g}k", cap
    if style == 2:
        return f"not above Rs. {cap:,}", cap
    return f"budget {cap}", cap


def render(product, kind):
    cat = random.choice(CATEGORY_WORDS[product["category"]])
    col = random.choice(COLOUR_WORDS[product["colour"]])
    brand = product["brand"]
    size = size_phrase(product)
    money, cap = budget_phrase(product["price"])
    parts = [f"{col} {brand} {cat}"]
    if size:
        parts.append(size)
    parts.append(money)
    if kind == "late_constraint":
        body = [f"{brand} {cat}"] + ([size] if size else []) + [money]
        text = ", ".join(body) + f". and in {col} please"
    elif kind == "correction":
        wrong = random.choice([c for c in COLOUR_WORDS if c != product["colour"]])
        text = (f"{random.choice(COLOUR_WORDS[wrong])} {brand} {cat}"
                + (f", {size}" if size else "") + f", {money}. "
                + f"{random.choice(CORRECT)}, in {col}")
    elif kind == "code_mixed":
        text = random.choice(HINDI).format(f"{col} {brand} {cat} "
                                           + (f"{size} " if size else "")
                                           + f"{cap} rupaye tak")
    else:
        text = random.choice(["i'd like ", "show me ", "", "looking for "]) + ", ".join(parts)
    return text, cap


def unique_target(product, cap):
    f = {"category": product["category"], "colour": product["colour"],
         "brand": product["brand"], "max_price": cap}
    if product["size"]:
        f["size"] = product["size"]
    hits = search("", f, k=3)
    return hits[0]["product_id"] if len(hits) == 1 else None


out, kinds = [], ["plain"] * 6 + ["correction", "late_constraint", "code_mixed"]
tries = 0
while len(out) < 300 and tries < 40000:
    tries += 1
    product = random.choice(CAT)
    kind = random.choice(kinds)
    text, cap = render(product, kind)
    target = unique_target(product, cap)
    if target is None:
        continue
    words = text.split()
    out.append({"id": f"stress-{len(out):04d}", "text": text, "words": words,
                "filters": {"category": product["category"], "colour": product["colour"],
                            "size": product["size"] or None, "brand": product["brand"],
                            "max_price": cap},
                "target": target, "earliest": len(words),
                "tags": [] if kind == "plain" else [kind]})
for row in out:
    print(json.dumps(row, ensure_ascii=False))
