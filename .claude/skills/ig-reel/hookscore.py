#!/usr/bin/env python3
"""
hookscore.py - score the first line of a Reel on the five things strong hooks
have in common, and rank a batch of them against each other.

What this is:  five local heuristics, computed on your machine from the text
alone. They measure properties that hooks which hold attention tend to share -
a length you can say in under three seconds, a concrete marker, something at stake,
the payload at the front rather than the back, and a viewer to aim it at.

What this is NOT:  a view predictor. It was tested against 74 real short-form
hooks, transcribed from the first three seconds of the top eight and bottom
eight performers on five channels. Separating a real hook from a deliberately
bad one it does well: AUC 0.83, and 9 of 10 written-to-be-bad hooks scored
below the real median. Separating a good creator's hits from that same
creator's misses it barely does at all: AUC 0.56, where 0.50 is a coin flip.

So use it for what it measured well. It catches greetings, preambles, hooks
with nothing concrete in them and hooks that take five seconds to say. It will
not tell you which of two decent hooks will travel, and nothing that reads text
can, because that is decided by your face, your edit, your audio and who
Instagram shows it to. Trust the retention graph over this script.

Each check returns 0 to 100. Higher is better.

On Persian all five run, on the Persian word lists below. Those lists were
written by hand, not measured: the AUC figures above are for English only,
and nobody has yet checked these checks against real Persian hooks and their
view counts. The length window is the English one in seconds, which at the
Persian rate measured on one reel (fa_text.FA_WPM, 115 a minute) is 4 to 8
words rather than 5 to 12.

Usage
  python3 hookscore.py hooks.txt              # one hook per line, ranked
  python3 hookscore.py --hook "I lost $18,000 on one missing contract."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py hooks.txt --json
  python3 hookscore.py hooks.txt --lang fa    # default: auto, per hook
"""

import argparse
import json
import math
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ig-human"))
try:
    import fa_text  # noqa: E402  the shared Persian text layer, in ig-human
except ImportError:
    sys.exit("hookscore.py needs ig-human/fa_text.py. Install the ig-human skill "
             "next to ig-reel.")

WORD_RE = fa_text.word_re("$%'’-")
NUMBER_RE = re.compile(
    r"\$\s?\d[\d,٬]*(?:[.٫]\d+)?"          # money, whole
    r"|\b\d[\d,٬]*(?:[.٫]\d+)?\s?"         # a figure, with or
    r"(?:[%٪]|k\b|x\b|hrs?\b|hours?\b|mins?\b|minutes?\b"  # without a unit
    r"|days?\b|weeks?\b|months?\b|years?\b)?",
    re.IGNORECASE)
PROPER_RE = re.compile(r"(?<!^)\b[A-Z][a-z]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Spoken hooks say their numbers out loud. "Zero dollars" and "twenty grand"
# are as concrete as "$0" and "$20,000", and counting only digits missed them.
# "one" and "first" are deliberately absent: they are filler far more often
# than they are a quantity.
SPOKEN_NUMBERS = {
    "zero", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "fifteen", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
    "billion", "dozen", "half", "twice", "triple",
}
MONEY_WORDS = {
    "dollars", "dollar", "bucks", "grand", "percent", "cents",
    "millionaire", "billionaire", "revenue", "profit", "salary", "rent",
}

# Words that put something on the line. A hook with none of these is a
# statement; a hook with one is a reason to keep watching.
STAKES = {
    "stop", "never", "wrong", "mistake", "mistakes", "lost", "lose", "losing",
    "cost", "costs", "broke", "broken", "failed", "failure", "fail", "nobody",
    "no", "not", "don't", "dont", "doesn't", "didn't", "can't", "won't",
    "quit", "quitting", "fired", "deleted", "delete", "killed", "kills", "kill",
    "replaced", "replaces", "cut", "beat", "free", "paid", "charged", "hired",
    "saved", "first",
    "banned", "illegal", "worst", "hate", "hated", "wasted", "waste", "scam",
    "lie", "lied", "lying", "truth", "secret", "hidden", "stole", "stolen",
    "before", "until", "instead", "but", "except", "unless", "problem",
    "risk", "danger", "warning", "regret", "wish", "should", "shouldn't",
    "still", "already", "only", "without", "versus", "vs", "actually",
}

# Openers that spend the first second saying nothing.
WEAK_OPENERS = [
    "so", "ok", "okay", "hey", "hi", "hello", "guys", "yo", "alright",
    "welcome", "today", "basically", "honestly", "look", "listen", "um",
    "just", "let", "lets", "let's", "i wanted", "i want", "one of",
    "have you", "did you", "do you", "are you", "in this", "in today",
    "the thing", "a lot", "there is", "there are", "this is", "it is",
    "as a", "when it", "if you've", "you know",
]

# Imperatives that earn the front position.
IMPERATIVES = {
    "stop", "steal", "copy", "delete", "try", "watch", "read", "save",
    "use", "build", "make", "write", "send", "take", "start", "quit",
    "never", "always", "don't", "dont", "do", "put", "run", "check",
}

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:stop scrolling|don'?t scroll)"),
     "Opens with \"stop scrolling\". Asking for attention proves you have not earned it."),
    (re.compile(r"(?i)\b(?:in (?:this|today'?s) (?:video|reel)|i'?m going to show you|i'?ll show you how)\b"),
     "Video preamble. Delete it and open on the payoff."),
    (re.compile(r"(?i)^\s*(?:hey |hi |what'?s up |welcome )"),
     "Greeting. Nobody came to the feed to be greeted."),
    (HASHTAG_RE,
     "Hashtag in the hook. Hashtags belong at the bottom of the caption, if anywhere."),
    (EMOJI_RE,
     "Emoji in the hook. On-screen text at hook size has room for words or for an emoji, not both."),
]


# The same lists for Persian. Every entry is compared after fa_text.fold(), so
# "هیچ‌وقت" and "هیچ وقت" are one entry and ي/ك match ی/ک.
def _fa(items):
    return {fa_text.fold(i) for i in items}


# "یک" and "اول" are left out for the reason "one" and "first" are, and "نه"
# because it is "no" far more often than it is "nine".
FA_SPOKEN_NUMBERS = _fa([
    "دو", "سه", "چهار", "پنج", "شش", "هفت", "هشت", "ده", "یازده", "دوازده",
    "سیزده", "چهارده", "پانزده", "پونزده", "شانزده", "هفده", "هجده", "هیجده",
    "نوزده", "بیست", "سی", "چهل", "پنجاه", "شصت", "هفتاد", "هشتاد", "نود",
    "صد", "دویست", "سیصد", "پانصد", "پونصد", "هزار", "میلیون", "میلیارد",
    "نصف", "نیم", "دوبرابر", "سه‌برابر",
])
FA_MONEY_WORDS = _fa([
    "تومان", "تومن", "ریال", "دلار", "درآمد", "سود", "حقوق", "اجاره", "فروش",
    "قیمت", "هزینه", "درصد",
])
FA_STAKES = _fa([
    "ضرر", "باختم", "باختن", "اشتباه", "اشتباهات", "اشتباهی", "هرگز", "هیچ‌وقت",
    "هیچوقت", "هیچ‌کس", "هیچکس", "هیشکی", "نه", "نیست", "نبود", "نشد", "غلط",
    "خراب", "شکست", "اخراج", "حذف", "جایگزین", "رایگان", "مجانی", "گرون", "گران",
    "راز", "مخفی", "پنهان", "دروغ", "حقیقت", "واقعیت", "قبل", "اما", "ولی",
    "مگر", "مشکل", "خطر", "هشدار", "پشیمون", "پشیمان", "کاش", "فقط", "بدون",
    "واقعاً", "هنوز", "دیگه", "بدترین", "متنفر", "کلاهبرداری", "بدزد", "بدزدید",
    "باید", "نباید", "ممنوع", "مرده", "اولین", "استخدام", "صرفه‌جویی", "پس‌انداز",
])
# Several words that only put something at stake together.
FA_STAKES_PHRASES = [fa_text.fold(p) for p in [
    "از دست دادم", "از دست دادی", "از دست دادن", "از دست ندید", "از دست نده",
    "از دست میدی", "به جای", "در برابر", "ضرر کردم", "پول دور ریختم", "وقت تلف",
    "تلف کردم",
]]
# A verb negated with ن- or نمی-. Only common verbs, because a bare ن- is also
# the first letter of a lot of nouns.
FA_NEG_RE = re.compile(
    r"^(?:نمی |ن(?:کن|کنید|کنین|ذار|ذارید|گذارید|خر|خرید|نویس|نویسید|فرست|فرستید"
    r"|زن|زنید|ده|دید|گو|گید|ساز|سازید|رو|روید|دار|داری|دارید|دارم|داره|داشتم"
    r"|بود|بودم|شد|شده|کرد|کردم)$)")
FA_PRICE_RE = re.compile(r"\d[\d,٬]*\s*(?:هزار|میلیون|میلیارد)?\s*(?:تومان|تومن|دلار|ریال)")
# Openers that spend the first second saying nothing, matched against the
# first three words.
FA_WEAK_OPENERS = [fa_text.fold(o) for o in [
    "سلام", "درود", "خب", "خوب", "بچه‌ها", "دوستان", "رفقا", "امروز", "توی این",
    "در این", "تو این", "این ویدیو", "می‌خوام", "می‌خواهم", "قراره", "بیایید",
    "بیاید", "بیاین", "بذارید", "بزارید", "اجازه بدید", "راستش", "یکی از", "آیا",
    "تا حالا", "شاید", "ببینید", "گوش کنید", "اینجا", "یه سری", "یک سری",
    "همونطور که",
]]
# Imperatives. Persian puts the verb last, so the first and the last words
# both get looked at.
FA_IMPERATIVES = _fa([
    "بدزد", "بدزدید", "کپی کن", "کپی کنید", "امتحان کن", "امتحان کنید", "سیو کن",
    "سیو کنید", "ذخیره کن", "ذخیره کنید", "پاک کن", "پاک کنید", "بنویس",
    "بنویسید", "بخون", "بخوانید", "بساز", "بسازید", "بفرست", "بفرستید", "شروع کن",
    "شروع کنید", "استفاده کن", "استفاده کنید", "نکن", "نکنید", "هرگز", "همیشه",
    "دست نگه دار", "بذار", "بزن", "بزنید", "چک کن", "تست کن",
    # The negative ones, the way "don't" is in the English list.
    "نذار", "نذارید", "نگذارید", "نخر", "نخرید", "ننویس", "ننویسید", "نفرست",
    "نفرستید", "نزن", "نزنید", "نده", "ندید", "نگو", "نگید", "نساز", "نسازید",
    "نرو", "نروید",
])
# "تو" is left out: spoken, it means "in" ("تو این ویدیو") as often as "you",
# and the verb ending ("می‌تونی") catches the "you" it would have caught.
FA_YOU = _fa([
    "شما", "خودت", "خودتون", "خودتان", "برات", "براتون", "برایتان", "بهت",
    "بهتون", "داری", "دارید", "دارین", "نداری", "ندارید", "هستی", "هستید", "هستین",
    "کردی", "کردید", "کردین", "گرفتی",
])
FA_ME = _fa(["من", "ما", "خودم", "خودمون", "برام", "برامون", "بهم", "بهمون"])

FA_DEALBREAKERS = [
    (re.compile(r"^\s*(?:اسکرول نکن|رد نشو)"),
     "Opens with \"stop scrolling\". Asking for attention proves you have not earned it."),
    (re.compile(r"(?:در|توی|تو) (?:این (?:ویدیو|ویدئو|ریلز)|ویدیوی امروز)"
                r"|(?:قراره|می خوام|می خواهم) (?:بهتون|به شما) (?:نشون|نشان|بگم|بگویم)"),
     "Video preamble. Delete it and open on the payoff."),
    (re.compile(r"^\s*(?:سلام|درود)\b"),
     "Greeting. Nobody came to the feed to be greeted."),
]


def _fa_negated(t):
    """A negated verb: the list in FA_NEG_RE, or ن- on a first- or second-person
    past verb ("نساختم", "ندیدی"), which is the "I didn't" a hook is built on."""
    return bool(FA_NEG_RE.match(t)) or (
        t.startswith("ن") and len(t) >= 5
        and t[1:].endswith(("دم", "تم", "دیم", "تیم", "دی", "تی", "دید", "تید")))


def _fa_you_verb(t):
    """A second-person verb (می‌دونی، نمی‌کنید) or "your" on a plural (پست‌هات)."""
    return ((t.startswith(("می ", "نمی ")) and t.endswith(("ی", "ید", "ین")))
            or t.endswith("هات") or (len(t) >= 5 and t.endswith("تون")))


def _fa_me_verb(t):
    """A first-person verb: می‌خوام، کرده‌ام، باختم."""
    return ((t.startswith(("می ", "نمی ")) and t.endswith("م")) or t.endswith(" ام")
            or (len(t) >= 4 and t.endswith(("دم", "تم", "دیم", "تیم")) and t != "مردم"))


def _fa_has(phrase, folded):
    return re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", folded) is not None


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # "$18,000" is one word when it is spoken, so it is one word here too.
    return WORD_RE.findall(fa_text.THOUSANDS_RE.sub("", text))


def check_length(text):
    """A hook has to land before the thumb moves. Roughly two seconds."""
    w = words(text)
    n = len(w)
    secs = n / 2.75                      # ~165 words per minute, spoken
    chars = len(text.strip())
    if 5 <= n <= 12:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 12) * 11)
    if chars > 60:                       # two lines of big on-screen text
        score -= 12
    return clamp(score), f"{n} words, {chars} chars, ~{secs:.1f}s spoken (want 5-12 words)"


def check_length_fa(text):
    """The same window as check_length, in seconds rather than words.

    Persian is spoken at fewer words a minute (fa_text.FA_WPM), so 5 to 12
    English words, about 1.8 to 4.4 seconds, is 4 to 8 Persian ones. The
    penalty per second outside the window is the English one too.
    """
    en_wps, wps = 2.75, fa_text.FA_WPM / 60.0
    n = len(words(text))
    secs = n / wps
    lo, hi = 5 / en_wps, 12 / en_wps
    chars = len(text.strip())
    if lo <= secs <= hi:
        score = 100.0
    elif secs < lo:
        score = clamp(100 - (lo - secs) * 20 * en_wps)
    else:
        score = clamp(100 - (secs - hi) * 11 * en_wps)
    if chars > 60:                       # two lines of big on-screen text
        score -= 12
    return clamp(score), (f"{n} words, {chars} chars, ~{secs:.1f}s spoken at {fa_text.FA_WPM} wpm "
                          f"(want {math.ceil(lo * wps)}-{math.floor(hi * wps)} words)")


def check_specificity(text):
    """One concrete thing beats three abstract ones."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    low = [w.lower().strip("'’") for w in words(text)]
    spoken = [w for w in low if w in SPOKEN_NUMBERS or w in MONEY_WORDS
              or fa_text.fold(w) in FA_SPOKEN_NUMBERS or fa_text.fold(w) in FA_MONEY_WORDS]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} concrete marker(s)" + (f": {found}" if found else
                   " - no number, no name, nothing checkable"))


def check_stakes(text):
    """Tension, cost, negation. Something the viewer might lose."""
    w = [x.lower().strip("'’") for x in words(text)]
    hits = [x for x in w if x in STAKES]
    markers = sorted(set(hits))
    if re.search(r"\$\s?\d", text):
        markers.append("a price")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} tension marker(s)" + (f": {', '.join(markers[:4])}" if markers else
                                         " - nothing is at stake in this line")
    return clamp(score), detail


def check_frontload(text):
    """The interesting word cannot be in position nine."""
    w = words(text)
    if not w:
        return 0.0, "empty"
    low = [x.lower().strip("'’") for x in w]
    opener = " ".join(low[:2])
    penalty = 0
    hit_opener = None
    for weak in WEAK_OPENERS:
        if opener.startswith(weak) or low[0] == weak:
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or token in SPOKEN_NUMBERS or token in MONEY_WORDS
                or NUMBER_RE.match(w[i]) or (i and PROPER_RE.match(w[i]))):
            payload = i
            break
    return _placed(payload, penalty, hit_opener)


def _placed(payload, penalty, hit_opener):
    """FRONTLOAD's score from where the payload word landed."""
    if payload is None:
        base = 30.0
        where = "no payload word anywhere in the line"
    elif payload <= 3:
        base = 100.0
        where = f"payload at word {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"payload at word {payload + 1}, could move forward"
    else:
        base = 40.0
        where = f"payload at word {payload + 1}, too late"
    detail = where + (f"; weak opener \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Aimed at one viewer, or floating in the air."""
    low = text.lower()
    w = [x.lower().strip("'’") for x in words(text)]
    if re.search(r"\b(you|your|you're|youre|yourself)\b", low):
        return 100.0, "speaks to the viewer"
    if w and w[0] in IMPERATIVES:
        return 90.0, f"imperative opener (\"{w[0]}\")"
    if re.search(r"\b(i|my|me|we|our)\b", low):
        return 70.0, "first person, no viewer named"
    return 35.0, "third person, nobody in the room"


# The three checks that read words, for Persian. Same scores, same thresholds;
# only the word lists differ, and Persian is compared after fold().

def check_stakes_fa(text):
    toks = [fa_text.fold(x) for x in words(text)]
    folded = fa_text.fold(text)
    markers = sorted({t for t in toks if t in FA_STAKES})
    markers += [p for p in FA_STAKES_PHRASES if _fa_has(p, folded)]
    if any(_fa_negated(t) for t in toks if t not in FA_STAKES):
        markers.append("a negation")
    if re.search(r"\$\s?\d", text) or FA_PRICE_RE.search(folded):
        markers.append("a price")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} tension marker(s)" + (f": {', '.join(markers[:4])}" if markers else
                                         " - nothing is at stake in this line")
    return clamp(score), detail


def check_frontload_fa(text):
    w = words(text)
    if not w:
        return 0.0, "empty"
    toks = [fa_text.fold(x) for x in w]
    opener = " ".join(toks[:3])
    penalty, hit_opener = 0, None
    for weak in FA_WEAK_OPENERS:
        if opener == weak or opener.startswith(weak + " "):
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, t in enumerate(toks):
        # A Latin name ("ChatGPT") counts at word one too: Persian has no
        # sentence capital to mistake it for.
        if (t in FA_STAKES or t in FA_SPOKEN_NUMBERS or t in FA_MONEY_WORDS
                or _fa_negated(t) or NUMBER_RE.match(w[i]) or PROPER_RE.match(w[i])):
            payload = i
            break
    return _placed(payload, penalty, hit_opener)


def check_address_fa(text):
    toks = [fa_text.fold(x) for x in words(text)]
    if any(t in FA_YOU or _fa_you_verb(t) for t in toks):
        return 100.0, "speaks to the viewer"
    ends = {" ".join(toks[:1]), " ".join(toks[:2]), " ".join(toks[-1:]), " ".join(toks[-2:])}
    hit = sorted(ends & FA_IMPERATIVES)
    if hit:
        return 90.0, f"imperative (\"{hit[0]}\")"
    if any(t in FA_ME or _fa_me_verb(t) for t in toks):
        return 70.0, "first person, no viewer named"
    return 35.0, "third person, nobody in the room"


CHECKS = ["LENGTH", "SPECIFICITY", "STAKES", "FRONTLOAD", "ADDRESS"]


def run(text, lang="auto"):
    lang = fa_text.resolve_lang(lang, text)
    fa = lang == "fa"
    results = {
        "LENGTH": check_length_fa(text) if fa else check_length(text),
        "SPECIFICITY": check_specificity(text),
        "STAKES": check_stakes_fa(text) if fa else check_stakes(text),
        "FRONTLOAD": check_frontload_fa(text) if fa else check_frontload(text),
        "ADDRESS": check_address_fa(text) if fa else check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    if fa:
        flags += [msg for pattern, msg in FA_DEALBREAKERS
                  if pattern.search(fa_text.fold(text)) and msg not in flags]
    scores = [results[c][0] for c in CHECKS if results[c][0] is not None]
    # The weakest property caps the hook, same logic as detect.py: one bad
    # property is enough for the thumb to keep moving.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "STRONG" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "WEAK")
    return results, overall, verdict, flags


def weakest_check(results):
    return min((c for c in CHECKS if results[c][0] is not None), key=lambda c: results[c][0])


def scored(results):
    return sum(1 for c in CHECKS if results[c][0] is not None)


def bar(score, width=24):
    if score is None:
        return " " * width
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nHOOK SCORE", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        shown = "  n/a" if score is None else f"{score:5.1f}"
        print(f"  {name:<13} {bar(score)} {shown}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'HOOK SCORE':<13} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if scored(results) < len(CHECKS):
        print(f"  {'':<13} over {scored(results)} of {len(CHECKS)} checks", file=out)
    for f in flags:
        print(f"\n  DEALBREAKER  {f}", file=out)
    if verdict != "STRONG":
        print(f"\n  Weakest property: {weakest_check(results)}. Fix that one and re-run.",
              file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nHOOK RANKING\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        partial = f"  [{r['scored']} of {len(CHECKS)} checks]" if r["scored"] < len(CHECKS) else ""
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {hook}{partial}", file=out)
        print(f"        weakest: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        dealbreaker: {f}", file=out)
    print("\nShoot the top one. If the top one is under 50, none of these are the hook.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Score a Reel hook on five properties.")
    ap.add_argument("input", nargs="?", default="-", help="file with one hook per line, or -")
    ap.add_argument("--hook", help="score a single hook given on the command line")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lang", default="auto", choices=["auto", "fa", "en"],
                    help="language of the hooks (default: guess, per hook)")
    args = ap.parse_args()

    fa_text.utf8_stdio()
    if args.hook:
        lines = [args.hook]
    else:
        raw = fa_text.read_input(args.input)
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("nothing to score", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line, args.lang)
        payload.append({
            "hook": line,
            "checks": {k: {"score": None if v[0] is None else round(v[0], 1), "detail": v[1]}
                       for k, v in results.items()},
            "weakest": weakest_check(results),
            "scored": scored(results),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0], args.lang)
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
