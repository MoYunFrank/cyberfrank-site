#!/usr/bin/env bash
# Smoke test for cyberfrank site. Usage: scripts/smoke-test.sh [base_url ...]
# Checks: HTTP 200, key content present, no forbidden words, all external links reachable.
set -uo pipefail
URLS=("${@:-https://cyberfrank.is-a.dev/}")
fail=0
for base in "${URLS[@]}"; do
  html=$(curl -fsSL --max-time 20 "$base") || { echo "FAIL $base not reachable"; fail=1; continue; }
  echo "OK   $base reachable"
  for must in "CyberFrank" "乙方合同体检"; do
    grep -q "$must" <<<"$html" && echo "OK   contains '$must'" || { echo "FAIL missing '$must'"; fail=1; }
  done
  # is-a.dev terms: no prices / checkout; product must never be called 律师函
  for bad in "律师函" "¥" "￥" "立即购买" "收款码"; do
    grep -q "$bad" <<<"$html" && { echo "FAIL forbidden '$bad' found"; fail=1; } || true
  done
  for link in $(grep -oE 'href="https?://[^"]+"' <<<"$html" | sed -E 's/href="|"//g' | sort -u); do
    code=$(curl -s -o /dev/null -L --max-time 15 -w '%{http_code}' "$link")
    if [[ "$code" =~ ^(2|3) ]] || [[ "$code" =~ ^(401|403|429)$ ]]; then echo "OK   $code $link"; else echo "FAIL $code $link"; fail=1; fi
  done
done
exit $fail
