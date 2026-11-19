#!/usr/bin/env bash
# bout.sh — rebuilds a sumo bout from the fighters' transcripts.
#
# Reads only the SendMessage and SubagentHandback calls of each transcript (JSONL),
# so the orchestrator watches the debate without loading the whole transcript into its context.
# Where SubagentHandback does not exist, the report is the fighter's last text that starts
# with «FINAL REPORT» or contains «Final position» (Spanish «INFORME FINAL» / «Posición final» too).
#
# Usage:
#   bout.sh [--md] [--reports] [--status] ROLE=transcript.output [ROLE=transcript.output ...]
#
#   ROLE          fighter label (e.g. CRITIC, DEFENDER)
#   --md          Markdown output (to save in dohyo/<bout>/transcript.md)
#   --reports     adds each fighter's final report (SubagentHandback)
#   --status      only prints the scoreboard: messages per fighter, last message,
#                 who has an unanswered message from the rival, whether anyone wrote
#                 «NO ARGUMENTS LEFT» and who delivered a report
#
# Example:
#   bout.sh --status CRITIC=/tmp/.../tasks/abc.output DEFENDER=/tmp/.../tasks/def.output
set -euo pipefail

command -v jq >/dev/null || { echo "bout.sh: requires jq" >&2; exit 2; }

md=0; reports=0; status=0; pairs=()
for a in "$@"; do
  case "$a" in
    --md) md=1 ;;
    --reports) reports=1 ;;
    --status) status=1 ;;
    -h|--help) sed -n '2,17p' "$0"; exit 0 ;;
    *=*) pairs+=("$a") ;;
    *) echo "bout.sh: unrecognized argument: $a (use ROLE=file)" >&2; exit 2 ;;
  esac
done
[ ${#pairs[@]} -ge 1 ] || { sed -n '2,17p' "$0" >&2; exit 2; }

# Extracts events {ts, role, kind, to, summary, text} from every transcript.
events() {
  for p in "${pairs[@]}"; do
    role="${p%%=*}"; f="${p#*=}"
    [ -r "$f" ] || { echo "bout.sh: cannot read $f" >&2; continue; }
    jq -c -s --arg role "$role" '
      [ .[] | select(.type=="assistant") | .timestamp as $ts
        | .message.content[]?
        | if (.type=="tool_use" and (.name=="SendMessage" or .name=="SubagentHandback")) then
            {ts:$ts, role:$role,
             kind:(if .name=="SendMessage" then "msg" else "report" end),
             to:(.input.to // ""), summary:(.input.summary // ""),
             text:(.input.message // "" | if type=="string" then . else tostring end)}
          elif (.type=="text" and ((.text // "") | test("^\\s*\\**\\s*(FINAL REPORT|INFORME FINAL)|final position|posici[oó]n final"; "im"))) then
            {ts:$ts, role:$role, kind:"report_text", to:"", summary:"", text:.text}
          else empty end ]
      | (map(select(.kind=="report_text"))) as $tx
      | map(select(.kind!="report_text"))
      | if (map(select(.kind=="report")) | length) == 0 and ($tx | length) > 0
        then . + [$tx[-1] | .kind="report"] else . end
      | .[]
    ' "$f" 2>/dev/null || true
  done | jq -s 'sort_by(.ts)'
}

all="$(events)"

if [ "$status" = 1 ]; then
  jq -r '
    def surrender: ltrimstr(" ") | ascii_upcase | (startswith("NO ARGUMENTS LEFT") or startswith("SIN ARGUMENTOS"));
    (map(select(.kind=="msg")) | group_by(.role)
      | map("\(.[0].role): \(length) messages, last \(.[-1].ts[11:19])") | .[]),
    (map(select(.kind=="msg")) as $m
      | ($m | map(.role) | unique) as $roles
      | if ($roles|length)==2 and ([.[]|select(.kind=="report")]|length)==0 then
          ($m[-1]) as $u
          | "Pending: \($roles - [$u.role] | .[0]) has not replied to \($u.role)'"'"'s message from \($u.ts[11:19])"
        else empty end),
    (map(select(.kind=="msg" and (.text|surrender)))
      | if length>0 then "NO ARGUMENTS LEFT: \(.[0].role) at \(.[0].ts[11:19])" else "NO ARGUMENTS LEFT: nobody" end),
    (map(select(.kind=="report")) | if length>0 then "Reports delivered: \(map(.role)|join(", "))" else "Reports delivered: none" end)
  ' <<<"$all"
  exit 0
fi

filter='map(select(.kind=="msg"'
[ "$reports" = 1 ] && filter+=' or .kind=="report"'
filter+='))'

if [ "$md" = 1 ]; then
  jq -r "$filter"' | to_entries[] | .value as $e
    | if $e.kind=="msg"
      then "### \(.key+1). \($e.role) · \($e.ts[11:19]) UTC\(if $e.summary!="" then " · " + $e.summary else "" end)\n\n\($e.text)\n"
      else "### Final report of \($e.role) · \($e.ts[11:19]) UTC\n\n\($e.text)\n" end' <<<"$all"
else
  jq -r "$filter"' | .[]
    | if .kind=="msg"
      then "── [\(.ts[11:19])] \(.role) → \(.to)\(if .summary!="" then "  (" + .summary + ")" else "" end)\n\(.text)\n"
      else "══ [\(.ts[11:19])] FINAL REPORT of \(.role)\n\(.text)\n" end' <<<"$all"
fi
