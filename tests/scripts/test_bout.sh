#!/usr/bin/env bash
# Test of bout.sh and of the text report in verify.py: where SubagentHandback does not exist, the
# final report arrives as the fighter's last text and has to show up all the same.
set -euo pipefail
cd "$(dirname "$0")/../.."
S=skills/sumo/scripts
MAT=tests/fixtures/shapes
D="$(mktemp -d)"; trap 'rm -rf "$D"' EXIT

cat > "$D/c.jsonl" <<'EOF'
{"type":"assistant","timestamp":"2026-01-01T00:01:00Z","message":{"content":[{"type":"tool_use","name":"SendMessage","input":{"to":"B","message":"C1: tests/test_shapes.py:15 → «assert square_area(side) == expected»"}}]}}
{"type":"assistant","timestamp":"2026-01-01T00:03:00Z","message":{"content":[{"type":"tool_use","name":"SendMessage","input":{"to":"B","message":"C2 rebuttal"}}]}}
{"type":"assistant","timestamp":"2026-01-01T00:05:00Z","message":{"content":[{"type":"text","text":"FINAL REPORT\nFinal position: rewrite. shapes.py:400"}]}}
EOF
cat > "$D/d.jsonl" <<'EOF'
{"type":"assistant","timestamp":"2026-01-01T00:02:00Z","message":{"content":[{"type":"tool_use","name":"SendMessage","input":{"to":"A","message":"D1"}}]}}
{"type":"assistant","timestamp":"2026-01-01T00:02:30Z","message":{"content":[{"type":"text","text":"Preparing the rebuttal."}]}}
EOF

fails=0
expect() { grep -qF -- "$2" <<<"$1" || { echo "FAIL: «$2» does not appear"; fails=$((fails+1)); }; }

st="$($S/bout.sh --status CRITIC="$D/c.jsonl" DEFENDER="$D/d.jsonl")"
expect "$st" "CRITIC: 2 messages"
expect "$st" "Reports delivered: CRITIC"

md="$($S/bout.sh --md --reports CRITIC="$D/c.jsonl" DEFENDER="$D/d.jsonl")"
expect "$md" "Final report of CRITIC"
grep -q "Preparing the rebuttal" <<<"$md" && { echo "FAIL: an arbitrary text was taken as a report"; fails=$((fails+1)); }

# With nobody's report, the status says who owes a reply.
head -2 "$D/c.jsonl" > "$D/c2.jsonl"
st2="$($S/bout.sh --status CRITIC="$D/c2.jsonl" DEFENDER="$D/d.jsonl")"
expect "$st2" "Pending: DEFENDER has not replied to CRITIC's message"

ver="$(python3 -I $S/verify.py --root "$MAT" CRITIC="$D/c.jsonl" DEFENDER="$D/d.jsonl")"
expect "$ver" "CRITIC report"
expect "$ver" "CRITIC: 2 citations · 1 with literal verified · 1 failed"

[ "$fails" = 0 ] && echo "OK: bout.sh" || { echo "$fails failures"; exit 1; }
