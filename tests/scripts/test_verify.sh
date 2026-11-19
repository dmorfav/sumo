#!/bin/bash
# Test of verify.py with citations of known outcome on the invoicer material.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
msg() { python3 -I -c 'import json,sys; print(json.dumps({"type":"assistant","timestamp":sys.argv[1],"message":{"content":[{"type":"tool_use","name":"SendMessage","input":{"to":"x","message":sys.argv[2]}}]}}))' "$1" "$2"; }
{
  msg 2026-01-01T00:00:01Z 'C1: VAT is rounded per invoice, `invoicer/calc.py:13` → "return round(base * rate, 2)".'
  msg 2026-01-01T00:00:02Z 'C2: the README boasts about coverage, README.md:5 → «Test coverage: 99 %».'
  msg 2026-01-01T00:00:03Z 'C3: the calculation has 200 lines (invoicer/calc.py:150-160).'
  msg 2026-01-01T00:00:04Z 'C4: there is a tax module in invoicer/taxes.py:10.'
} > "$tmp/c.jsonl"
{
  msg 2026-01-01T00:00:05Z 'D1: the test expects «assert total(lines) == 1.27» (test_calc.py:15).'
  msg 2026-01-01T00:00:06Z 'D2: the rounding test is in tests/test_calc.py:13-15, no literal.'
} > "$tmp/d.jsonl"
out="$(python3 -I skills/sumo/scripts/verify.py --root tests/fixtures/invoicer CRITIC="$tmp/c.jsonl" DEFENDER="$tmp/d.jsonl")"
echo "$out"
fail=0
expect() { grep -F -- "$1" <<<"$out" | grep -qF -- "$2" || { echo "FAIL: $1 should give «$2»"; fail=1; }; }
expect 'calc.py:13 '           'literal on the cited line'
expect 'README.md:5'           'is not there'
expect 'calc.py:150-160'       'does not have those lines'
expect 'taxes.py:10'           'does not exist'
expect 'test_calc.py:15'       'literal on the cited line'
expect 'test_calc.py:13-15'    'the line exists'
expect 'CRITIC: 4 citations'   '3 failed'
expect 'DEFENDER: 2 citations' '0 failed'
[ $fail = 0 ] && echo "OK: verify.py"
exit $fail
