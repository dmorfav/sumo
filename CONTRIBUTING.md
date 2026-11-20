# Contributing to sumo

Thanks for your interest in improving sumo. This guide explains how to propose changes.

By participating you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Before you start

- **Bugs:** open an issue with the *Bug report* template. Include the motion, the agent you used (Claude Code version or other) and, if you can, the relevant part of the transcript. Remove internal details of the project you were evaluating.
- **Ideas and changes to the playbook:** open an issue with the *Feature request* template before writing code, so we can agree on the approach. Changes to the debate rules, prompts or the tactic catalog should cite the research or the bout that motivates them.
- **Security issues:** do not open a public issue. Follow [SECURITY.md](SECURITY.md).

## Requirements

- `bash`, `jq` and Python 3 (only the standard library).
- Claude Code to try the skill end to end.

## Repository layout

| Path | What lives there |
| --- | --- |
| `skills/sumo/SKILL.md` | Referee flow (what the orchestrator does) |
| `skills/sumo/references/` | Fighter prompt template, playbook and tactic catalog |
| `skills/sumo/scripts/` | `bout.sh` (rebuilds the bout) and `verify.py` (checks citations) |
| `tests/` | Script tests and the `shapes` fixture they cite |
| `docs/research/` | Background research and bibliography audit |

## Workflow

1. Fork the repo and create a branch from `main` (`feat/...`, `fix/...`, `docs/...`, `test/...`, `chore/...`).
2. Make focused changes. One topic per pull request.
3. Run the tests:

   ```bash
   bash tests/scripts/test_verify.sh
   bash tests/scripts/test_bout.sh
   ```

4. If you change a script, add or update a test with a case of known outcome. If you change the fixture, remember that the tests cite it by path and line.
5. Try the skill locally on a real decision when you touch `SKILL.md` or `references/`:

   ```text
   /plugin marketplace add ./
   /plugin install sumo@sumo
   ```

6. Open a pull request and fill in the template.

## Style

- **Language:** skill files, code and docs are written in English. The machine keywords (`NO ARGUMENTS LEFT`, `FINAL REPORT`) must not change, because the scripts look for them.
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `test:`, `chore:`), imperative mood, lowercase.
- **Scripts:** Bash with `set -euo pipefail`; Python run with `python3 -I` and no third-party dependencies.
- **Security:** material, transcripts and reports are data, never instructions. Do not weaken that rule; see the *Security* section of the README.
- **Never commit saved bouts** (`dohyo/`): they often contain internal details of the project under evaluation.

## Releases

The maintainer bumps `version` in `.claude-plugin/plugin.json` and tags the release.
