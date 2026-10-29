#!/usr/bin/env python3
"""
fa_text.py - the Persian text layer every script in this pack shares.

The scripts were written for English and read words with [A-Za-z]. On Persian
that counts zero words, misses every hashtag, and, worst of all, treats the
half-space (U+200C, ZERO WIDTH NON-JOINER) as a machine fingerprint and
deletes it, which turns "می‌خواهم" into "میخواهم". This module is the fix, in
one place:

  - word and letter patterns that read Persian, keep the half-space inside a
    word, and match exactly what the old ASCII patterns matched on English
  - sentence ends that include the Persian question mark
  - a language guess, so a check that was only ever calibrated on English can
    say so instead of returning a confident wrong number
  - which invisible characters are legitimate and which are a fingerprint
  - a conservative orthography pass: Arabic yeh and kaf, stray half-spaces,
    and the missing half-space in "می خواهم" and "کتاب ها"

Standard library only, like the rest of the pack. The other skills import it
from this folder, so ig-human has to be installed next to them.
"""

import re
import sys
import unicodedata

ZWNJ = "‌"
ZWJ = "‍"
BIDI_MARKS = {"‎", "‏", "؜"}     # LRM, RLM, ARABIC LETTER MARK

# Persian letters, plus the Arabic ones that turn up in Persian text.
FA_LETTERS = "ء-غف-يپچژکگۀی"
# Harakat and the other marks that sit on a letter without being one.
MARKS = "ً-ٰٟۖ-ۭ"
FA_LETTER_RE = re.compile(f"[{FA_LETTERS}{MARKS}]")

# Persian speaking rate, words a minute. Measured on one edited reel of an
# AI-tools workshop for teachers (2026-10-19): 165 words over
# 86.7 s from first word to last, 114 to 117 depending on how pauses count.
# One speaker in one video, so a starting point: beats.py --wpm overrides it.
# English, by comparison, is the 165 this pack was built on.
FA_WPM = 115

SENT_END = ".!?؟"                            # the last one is ؟
SENT_RE = re.compile(f"[^{SENT_END}\\n]+[{SENT_END}]*")
SENT_RE_KEEP_LINES = re.compile(f"[^{SENT_END}]+[{SENT_END}]*")

# Thousands separators between digits: "18,000" and "۱۸٬۰۰۰".
THOUSANDS_RE = re.compile(r"(?<=\d)[,٬](?=\d)")

# Words that carry no meaning of their own. beats.py uses them to decide
# whether the last line echoes the hook, so they must not count as an echo.
FA_STOPWORDS = {
    "و", "در", "به", "از", "که", "این", "آن", "را", "رو", "با", "برای", "تا",
    "است", "هست", "بود", "شد", "یک", "یه", "هم", "اما", "ولی", "یا", "اگر",
    "اگه", "چون", "پس", "من", "تو", "او", "اون", "ما", "شما", "آنها", "اونا",
    "خود", "خودم", "هر", "همه", "چه", "چی", "کی", "کجا", "چرا", "چطور", "نه",
    "بله", "آره", "دیگر", "دیگه", "خیلی", "فقط", "حتی", "بر", "روی", "توی",
    "هیچ", "باید", "شاید", "می", "نمی", "ها", "های", "ای", "همین", "اینو",
    "اینه", "کرد", "کردم", "کن", "کنید", "کنم", "دارم", "داره", "دارد",
}

_YEH_KAF = str.maketrans({"ي": "ی", "ى": "ی", "ك": "ک"})
_HARAKAT_RE = re.compile(f"[{MARKS}ـ]")      # and tatweel
_SPACE_RE = re.compile(r"\s+")


def word_re(extra=""):
    """Letters and digits in any script, plus the characters in `extra`, with
    the half-space and harakat kept inside the word.

    On ASCII text this matches exactly what [A-Za-z0-9{extra}]+ matched, so
    every English number this pack has published stays the same.
    """
    return re.compile(r"(?:[^\W_]|[" + MARKS + ZWNJ + re.escape(extra) + r"])+")


def letters_re(extra=""):
    """word_re without digits: [A-Za-z{extra}]+ on ASCII text."""
    return re.compile(r"(?:[^\W\d_]|[" + MARKS + ZWNJ + re.escape(extra) + r"])+")


def phrase_re(find):
    """A lexicon entry as a pattern. A space in the entry matches a space or a
    half-space, and ی and ک also match their Arabic forms, so "می‌توان گفت"
    and "میتوان گفت" are the same entry. On English this is the pattern the
    lexicon always used: word boundaries, and any whitespace between words."""
    body = re.escape(find).replace(r"\ ", "[\\s" + ZWNJ + "]+")
    body = body.replace("ی", "[یيى]").replace("ک", "[کك]")
    return re.compile(r"\b" + body + r"\b", re.IGNORECASE)


def is_fa_letter(ch):
    return bool(ch) and bool(FA_LETTER_RE.match(ch))


def lang_of(text):
    """'fa' when most of the letters are Persian, otherwise 'en'.

    AI content in Persian is full of English names (ChatGPT, Claude, prompt),
    so the bar is 40% of the letters rather than a majority.
    """
    fa = sum(1 for c in text if is_fa_letter(c))
    latin = sum(1 for c in text if c.isascii() and c.isalpha())
    if not fa:
        return "en"
    return "fa" if fa / (fa + latin) >= 0.4 else "en"


def resolve_lang(choice, text):
    return lang_of(text) if choice in (None, "", "auto") else choice


def fold(text):
    """A comparison key: case, yeh and kaf, harakat, tatweel and the
    half-space-versus-space difference all stop mattering."""
    text = text.lower().translate(_YEH_KAF).replace(ZWNJ, " ")
    return _SPACE_RE.sub(" ", _HARAKAT_RE.sub("", text)).strip()


def _is_emoji(ch):
    if not ch:
        return False
    cp = ord(ch)
    return (0x1F000 <= cp <= 0x1FAFF or 0x2600 <= cp <= 0x27BF
            or 0x2B00 <= cp <= 0x2BFF or cp == 0xFE0F)


def is_legit_invisible(text, i, lang):
    """Is the invisible character at text[i] doing a real job?

    - A half-space between two Persian letters is spelling, not a fingerprint.
    - A zero-width joiner between two emoji builds one emoji (the technologist
      and family emoji are built this way). Deleting it splits them in two.
    - LRM, RLM and ALM in Persian text fix the direction of a line that starts
      with an English word, which Instagram would otherwise lay out
      left-to-right.
    """
    ch = text[i]
    before = text[i - 1] if i > 0 else ""
    after = text[i + 1] if i + 1 < len(text) else ""
    if ch == ZWNJ:
        return is_fa_letter(before) and is_fa_letter(after)
    if ch == ZWJ:
        return _is_emoji(before) and _is_emoji(after)
    if ch in BIDI_MARKS:
        return lang == "fa"
    return False


def drop_stray(text, chars, lang):
    """Delete each character in `chars` that is not doing a real job.
    Returns (text, deleted, kept)."""
    deleted = kept = 0
    if ZWNJ in chars:
        # A doubled half-space is one half-space too many.
        collapsed = re.sub(ZWNJ + "{2,}", ZWNJ, text)
        deleted += len(text) - len(collapsed)
        text = collapsed
    out = []
    for i, ch in enumerate(text):
        if ch not in chars:
            out.append(ch)
        elif is_legit_invisible(text, i, lang):
            out.append(ch)
            kept += 1
        else:
            deleted += 1
    return "".join(out), deleted, kept


def stray_invisibles(text, lang):
    """How many format characters are a fingerprint rather than spelling."""
    n = 0
    for i, ch in enumerate(text):
        if unicodedata.category(ch) == "Cf" and not is_legit_invisible(text, i, lang):
            n += 1
    return n


# The half-space a phone keyboard leaves out. Only the cases with one reading:
# the verb prefix می / نمی standing alone before a word, and the plural and
# superlative suffixes standing alone after one. Bare ها and های are only
# joined mid-sentence, because sentence-final "ها" is often the spoken
# emphasis ("یادت نره ها"), not a plural.
_FA = f"[{FA_LETTERS}]"
_PREFIX_RE = re.compile(rf"(?<![\w{ZWNJ}])(ن?می) +(?={_FA})")
_SUFFIX_RE = re.compile(
    rf"(?<={_FA}) +(هایی|هایم|هایت|هایش|هایمان|هایتان|هایشان|ترین)(?![\w{ZWNJ}])")
_PLURAL_RE = re.compile(rf"(?<={_FA}) +(ها|های)(?= +{_FA})")


def fix_orthography(text):
    """Arabic yeh and kaf to Persian, and the missing half-spaces above.
    Returns (text, hits), one hit per kind of change, for the report."""
    hits = []
    n = sum(text.count(c) for c in "يىك")
    if n:
        hits.append({"name": "Arabic yeh/kaf -> Persian ی/ک", "count": n})
        text = text.translate(_YEH_KAF)
    for name, pattern, repl in (
            ("missing half-space after می/نمی", _PREFIX_RE, r"\1" + ZWNJ),
            ("missing half-space before a suffix", _SUFFIX_RE, ZWNJ + r"\1"),
            ("missing half-space before ها/های", _PLURAL_RE, ZWNJ + r"\1")):
        text, n = pattern.subn(repl, text)
        if n:
            hits.append({"name": name, "count": n})
    return text, hits


def read_input(path):
    """A file or stdin, as text. utf-8-sig drops the byte-order mark Windows
    Notepad puts at the start of a file, which is a file format, not text."""
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8-sig") as fh:
        return fh.read()


def utf8_stdio():
    """Windows hands Python a cp1252 console, which turns Persian on stdin into
    mojibake and crashes on Persian output. Every script calls this first."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
