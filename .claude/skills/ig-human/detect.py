#!/usr/bin/env python3
"""
detect.py - a five-check panel that scores how machine-written a draft looks.

What this is:  five local heuristics modelled on the signals public AI
detectors actually measure - sentence-length variation, concreteness, stock
vocabulary, typographic fingerprint, and voice. Every score is computed on
your machine from the text alone. Nothing is uploaded.

What this is NOT:  GPTZero, Originality, Copyleaks, Winston or Turnitin.
It does not call their APIs and it cannot promise their verdict. It catches
the things they all key on, which is why fixing them tends to move their
numbers too - but the only honest claim is the one on this line.

Each check returns a HUMAN score from 0 to 100. Higher is better.

On Persian all five run. SLOP DENSITY reads the Persian block of slop.json,
and VOICE counts only the structural tells, because contractions and subject
pronouns are English measures. The thresholds are still the English ones:
nobody has measured them against real Persian captions yet.

Usage
  python3 detect.py draft.txt
  pbpaste | python3 detect.py -
  python3 detect.py draft.txt --json
  python3 detect.py before.txt after.txt      # compare two drafts
  python3 detect.py draft.txt --lang fa       # default: auto
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")
sys.path.insert(0, HERE)
import fa_text  # noqa: E402

SENT_RE = fa_text.SENT_RE
WORD_RE = fa_text.letters_re("'")
CONTRACTIONS = re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.IGNORECASE)
PRONOUNS = re.compile(r"\b(i|me|my|mine|we|us|our|you|your)\b", re.IGNORECASE)
NUMBERS = re.compile(r"\b\d[\d,.٫٬]*[%٪]?\b|\$\d")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}\b", re.MULTILINE)


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Map value onto 0-100 where `human` -> 100 and `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def check_burstiness(text):
    """Humans vary sentence length hard. Models write even."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "too short to judge"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variation {cv:.2f} across {len(lens)} sentences (want 0.55+)"


def check_specificity(text, lang="en"):
    """Numbers, names and concrete nouns. Slop is abstract."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "too short to judge"
    per100 = 100 / len(w)
    hits = len(NUMBERS.findall(text)) + len(set(PROPER.findall(text)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    # Names are found by their capital letter, and Persian has none.
    note = ". Persian names are not counted yet" if lang == "fa" else ""
    return score, f"{hits} concrete markers, {density:.1f} per 100 words (want 4+){note}"


def check_slop(text, lex, lang="en"):
    """Stock vocabulary density against the lexicon. The Persian entries are
    in the same lexicon, so this runs the same way on both languages."""
    w = words(text)
    if not w:
        return 50.0, "empty"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        n = len(fa_text.phrase_re(entry["find"]).findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} stock terms, {density:.1f} per 100 words"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text, lang="en"):
    """Characters a phone keyboard does not produce. The Persian half-space,
    the joiner inside an emoji and the direction marks in Persian text are
    typed on purpose and do not count."""
    invisible = fa_text.stray_invisibles(text, lang)
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisible, {em} em dash, {curly} curly quote, "
              f"{ellip} ellipsis, {nbsp} hard space")
    return score, detail


def check_voice(text, lex, lang="en"):
    """Contractions, person, and the shapes models default to.

    On Persian only the shapes count. Persian has no contractions to count, and
    it drops the subject pronoun into the verb ending, so a pronoun count would
    call every natural Persian sentence machine-written."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "too short to judge"
    per100 = 100 / len(w)
    contractions = len(CONTRACTIONS.findall(text)) * per100
    person = len(PRONOUNS.findall(text)) * per100
    tells = 0
    names = []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    if lang == "fa":
        # Tells are the whole score here, where they are 30% of it in English,
        # so each kind counts once: five emoji bullets are one habit, not five.
        kinds = len(set(names))
        score = clamp(100 - kinds * 22)
        detail = (f"{kinds} kind(s) of structural tell, {tells} in all; "
                  "contractions and pronouns skipped on Persian")
    else:
        score = (scale(contractions, human=3.0, machine=0.0) * 0.35
                 + scale(person, human=8.0, machine=1.0) * 0.35
                 + clamp(100 - tells * 22) * 0.30)
        detail = (f"{contractions:.1f} contractions, {person:.1f} personal pronouns "
                  f"per 100 words, {tells} structural tell(s)")
    if uniform:
        score -= 12
        names.append("uniform-bullets")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["BURSTINESS", "SPECIFICITY", "SLOP DENSITY", "FINGERPRINT", "VOICE"]


def run(text, lex, lang="auto"):
    lang = fa_text.resolve_lang(lang, text)
    results = {}
    results["BURSTINESS"] = check_burstiness(text)
    results["SPECIFICITY"] = check_specificity(text, lang)
    results["SLOP DENSITY"] = check_slop(text, lex, lang)
    results["FINGERPRINT"] = check_fingerprint(text, lang)
    results["VOICE"] = check_voice(text, lex, lang)
    # A check that is not built for this language scores None and sits out.
    scores = [results[c][0] for c in CHECKS if results[c][0] is not None]
    # The weakest check drags the verdict: a detector only needs one signal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASS" if overall >= 70 and min(scores) >= 55 else (
        "REVIEW" if overall >= 50 else "FLAGGED")
    return results, overall, verdict


def weakest_check(results):
    return min((c for c in CHECKS if results[c][0] is not None), key=lambda c: results[c][0])


def bar(score, width=24):
    if score is None:
        return " " * width
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "AI DETECTION PANEL" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        shown = "  n/a" if score is None else f"{score:5.1f}"
        print(f"  {name:<13} {bar(score)} {shown}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'HUMAN SCORE':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    skipped = sum(1 for c in CHECKS if results[c][0] is None)
    if skipped:
        print(f"  {'':<13} over {len(CHECKS) - skipped} of {len(CHECKS)} checks", file=out)
    if verdict != "PASS":
        print(f"\n  Weakest signal: {weakest_check(results)}. Fix that first.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Score how machine-written a draft looks.")
    ap.add_argument("input", nargs="?", default="-", help="file, or - for stdin")
    ap.add_argument("compare", nargs="?", help="second file, to show before/after")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    ap.add_argument("--lang", default="auto", choices=["auto", "fa", "en"],
                    help="language of the draft (default: guess from the letters)")
    args = ap.parse_args()

    fa_text.utf8_stdio()
    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = fa_text.read_input

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex, args.lang)
        payload.append({
            "source": name,
            "checks": {k: {"score": None if v[0] is None else round(v[0], 1), "detail": v[1]}
                       for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex, args.lang)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  "
              f"{b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
