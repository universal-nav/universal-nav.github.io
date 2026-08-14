#!/usr/bin/env bash
# Strip identifying metadata from images and video, then verify.
#
# iPhone media embeds GPS coordinates, device model, and capture timestamps.
# GPS alone reveals the collection city and possibly a street address, so no
# asset enters this repo without going through here first.
#
# Usage: tools/scrub-media.sh FILE [FILE...]
#
# This handles metadata only. It does NOT blur faces or license plates, and it
# does not watch the footage for street signs, storefronts, or campus
# buildings. Both of those are still on you.

set -euo pipefail

if [ $# -eq 0 ]; then
  sed -n '2,13p' "$0" | sed 's/^# \?//'
  exit 1
fi

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "error: $1 not installed ($2)" >&2
    exit 1
  }
}

status=0

for f in "$@"; do
  [ -f "$f" ] || { echo "error: no such file: $f" >&2; status=1; continue; }

  case "${f##*.}" in
    jpg|jpeg|png|JPG|JPEG|PNG|heic|HEIC|tif|tiff|webp)
      need exiftool "apt install libimage-exiftool-perl"
      exiftool -all= -overwrite_original "$f" >/dev/null
      ;;
    mp4|mov|MP4|MOV|m4v|webm)
      need ffmpeg "apt install ffmpeg"
      tmp="${f%.*}.scrubbed.${f##*.}"
      ffmpeg -loglevel error -y -i "$f" -map_metadata -1 -c copy "$tmp"
      mv "$tmp" "$f"
      ;;
    *)
      echo "skip: unrecognised extension: $f" >&2
      continue
      ;;
  esac

  # Verify. Anything beyond file size, format, and dimensions is a leak.
  if command -v exiftool >/dev/null 2>&1; then
    leaks=$(exiftool -s -G "$f" | grep -iE 'gps|serial|make|model|software|create date|date/time|modify date|artist|author|copyright|comment|location|owner' || true)
    if [ -n "$leaks" ]; then
      echo "LEAK REMAINS in $f:" >&2
      echo "$leaks" >&2
      status=1
    else
      echo "clean: $f"
    fi
  else
    echo "scrubbed (unverified, exiftool missing): $f"
    status=1
  fi
done

exit $status
