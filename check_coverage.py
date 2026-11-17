"""Run from this folder:  python check_coverage.py
Shows how many recorded pairs get a label sentence, and why the others do not."""
import random
import re
from collections import Counter

import backend as B

_, lk, _, _, labint, known = B._data()
keys = list(known.index)
random.Random(0).shuffle(keys)
keys = keys[:300]


def reason(a, b):
    """Why no sentence was accepted, using the first sentence that names the partner."""
    seen = False
    for src, partner in ((a, b), (b, a)):
        rec = labint.get(src)
        if not rec:
            continue
        pat = re.compile(r"\b(" + "|".join(re.escape(t) for t in B._terms(lk, partner)) + r")\b", re.I)
        text = re.sub(r"\s+", " ", rec["text"])
        for sent in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text):
            if not pat.search(sent):
                continue
            seen = True
            if len(sent) > 600: return "sentence longer than 600 characters", sent
            if len(sent) < 40: return "sentence shorter than 40 characters", sent
            if not sent[0].isupper() or not sent.endswith("."): return "starts mid-sentence or lacks a full stop", sent
            if re.search(r"Table \d|Drug Class", sent): return "table residue", sent
            if B._DOSING.search(sent): return "dosing or instruction wording", sent
    return ("partner drug never named in either label" if any(labint.get(x) for x in (a, b))
            else "no label text for either drug"), ""


found, why, example = 0, Counter(), {}
for k in keys:
    a, b = k.split("|")
    if B.get_label_sentence(a, b):
        found += 1
    else:
        r, s = reason(a, b)
        why[r] += 1
        example.setdefault(r, s)
print(f"\nLabel sentence found for {found} of {len(keys)} recorded pairs ({found / len(keys):.0%})\n")
for r, n in why.most_common():
    print(f"{n:4d}  {r}")
    if example[r]:
        print("      e.g.", example[r][:220], "\n")
