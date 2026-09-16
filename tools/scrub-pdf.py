#!/usr/bin/env python3
"""Blank the document properties of a PDF, in place, without re-encoding it.

LaTeX and every PDF tool downstream of it write an Info dictionary. Even when
/Author and /Title come out empty, pdfTeX leaves /PTEX.Fullbanner (its own
version and the TeX Live year) and the toolchain leaves creation and
modification timestamps that date the submission.

Rewriting the file with ghostscript or qpdf would strip these, but it also
re-encodes fonts and images and rewrites the link annotations. This script
instead overwrites the offending values with spaces of exactly the same byte
length, so every cross-reference offset in the file stays valid and the page
content is untouched.

Usage: tools/scrub-pdf.py FILE [FILE...]
"""

import re
import sys

# Keys whose values are blanked outright.
BLANK_KEYS = [
    b"Author", b"Title", b"Subject", b"Keywords",
    b"Creator", b"Producer", b"PTEX.Fullbanner",
]
# Dates are normalised rather than blanked: some readers dislike an empty date.
EPOCH = b"D:20260101000000Z"
DATE_KEYS = [b"CreationDate", b"ModDate"]

# A string value is either a literal (...) or a hex string <...>. The literal
# form may contain escaped parentheses, hence the backslash alternation.
VALUE = rb"(?:\((?:\\.|[^()\\])*\)|<[0-9A-Fa-f\s]*>)"


def info_spans(data):
    """Byte ranges of top-level objects that look like an Info dictionary."""
    spans = []
    for m in re.finditer(rb"\d+\s+0\s+obj\b", data):
        end = data.find(b"endobj", m.end())
        if end == -1:
            continue
        body = data[m.end():end]
        # An Info dict carries document properties and, unlike a page or
        # catalogue object, has no /Type.
        if b"/Type" in body:
            continue
        if any(b"/" + k in body for k in BLANK_KEYS + DATE_KEYS):
            spans.append((m.end(), end))
    return spans


def scrub(data):
    changed = 0
    for start, end in info_spans(data):
        body = bytearray(data[start:end])

        def replace(match, filler):
            nonlocal changed
            span = match.span(1)
            old = bytes(body[span[0]:span[1]])
            new = filler(len(old))
            assert len(new) == len(old), "replacement changed byte length"
            if new != old:
                body[span[0]:span[1]] = new
                changed += 1

        for key in BLANK_KEYS:
            pat = re.compile(rb"/" + re.escape(key) + rb"\s*(" + VALUE + rb")")
            for m in list(pat.finditer(bytes(body))):
                # "()" is the shortest literal; pad the rest with spaces.
                replace(m, lambda n: b"(" + b" " * (n - 2) + b")" if n >= 2 else b" " * n)

        for key in DATE_KEYS:
            pat = re.compile(rb"/" + re.escape(key) + rb"\s*(" + VALUE + rb")")
            for m in list(pat.finditer(bytes(body))):
                def date(n, _k=key):
                    stamp = b"(" + EPOCH + b")"
                    return stamp + b" " * (n - len(stamp)) if n >= len(stamp) else b" " * n
                replace(m, date)

        data = data[:start] + bytes(body) + data[end:]
    return data, changed


def main(argv):
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 1
    status = 0
    for path in argv:
        try:
            original = open(path, "rb").read()
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            status = 1
            continue
        scrubbed, changed = scrub(original)
        if len(scrubbed) != len(original):
            print(f"error: {path}: length changed, refusing to write", file=sys.stderr)
            status = 1
            continue
        open(path, "wb").write(scrubbed)
        print(f"scrubbed {changed} propert{'y' if changed == 1 else 'ies'}: {path}")
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
