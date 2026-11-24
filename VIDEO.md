# The 3-minute demo video

Screen recording of a terminal, one voice over it. Nothing to build or edit beyond
trimming. Record at 1080p; make the terminal font large enough to read on a phone.

Everything below is already working, so this is a recording job, not a building job.
Total 2:50, which leaves room to breathe inside the 3-minute limit.

---

### 0:00–0:20 — what the problem is

**On screen:** the title line of `ABSTRACT.md`, then the terminal.

> "A shopper types *black running shoes, size nine, under two thousand*. Most
> assistants wait for the full stop, then search. A good shop assistant is already
> walking to the shelf. The hard part isn't searching early — it's knowing when
> guessing early is safe."

### 0:20–1:05 — watch it read a request

**Run:**
```
python demo.py --id dev-0002 --pause 0.35
```

> "Each line is one more word. On the right is what the agent believes so far. It
> hasn't searched yet, because nothing it could search for would narrow anything down."

Let the commit line appear — the green arrow.

> "There. Eight words before the end — halfway through the sentence — it shows the
> product. The shopper is still talking. And it's not a guess. The
> shopper wants whichever product matches their whole request, so every word so far is
> part of that request — which means the right product is always still in the matching
> set. When exactly one product is left, it has to be the right one. That's a proof. So
> the agent can speak as early as the words allow, and never be wrong for speaking."

### 1:05–1:35 — the correction

**Run:**
```
python demo.py --id dev-0182 --pause 0.35
```

> "Now the shopper changes their mind twice. *Navy blue hoodie — hmm, size L — actually
> size S.* Watch the size appear as L and then flip to S. One rule does that: for each thing the shopper
> mentions, the last thing they said wins. The same rule handles a constraint that
> turns up late — *oh, and in blue* — with no extra code.
>
> But a correction is the one thing that breaks the proof, because it says a filter we
> already used was never wanted. So we checked all fifty-five corrections in the data.
> Every single one opens with one of about ten words — *no, sorry, wait, actually, I
> mean*. So the agent waits in just those two places: one word after a comma, four
> words after one of those openers. Everywhere else it answers immediately. That's why
> waiting costs almost nothing."

### 1:35–2:20 — the numbers

**Run:**
```
python evaluate.py --agent agent.py
```

> "On the three hundred development requests: the baseline scores twenty. We score
> forty-four point nine. Accuracy goes from fifty-three percent to a hundred percent —
> every request, every filter. Four wrong commits in three hundred. And it uses fewer
> searches than the baseline, one point two three against one point five three, because
> adding a filter can only remove products, so most lookups are answered from one we
> already paid for."

**Run:**
```
python evaluate.py --agent agent.py --data stress.jsonl
```

> "Our word list was written while reading that data, so a good score there proves
> less than it looks. This set is three hundred fresh requests built from the
> catalogue, deliberately worded in ways we never taught it — *sliders*, *windcheater*,
> *batua*, *belay that*. Accuracy holds at a hundred percent. The score goes up, to
> forty-seven point four."

### 2:20–2:50 — cost, and close

**Run:**
```
python tune.py
```

> "The two waiting numbers aren't fitted to the data either: tune them on one half, and
> the other half picks the same pair.
>
> There is no model and no API call at run time — it's three files of plain Python. One
> core handles eleven hundred requests a second, in twenty-one megabytes, so running
> this costs effectively nothing.
>
> It commits as early as the words allow, it's right every time, and it can prove why.
> Team Clauduss."

---

## Before recording

```
cd agentx
python make_stress.py > stress.jsonl     # if stress.jsonl is missing
python evaluate.py --agent agent.py      # check it still prints 44.9
```

Say the team name and the challenge once, at the start or the end. Do not read the
score off a slide — let the terminal print it.
