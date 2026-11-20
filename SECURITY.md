# Security Policy

## Supported versions

Only the latest release of sumo receives security fixes.

| Version | Supported |
| --- | --- |
| 0.1.x (latest) | ✅ |
| older | ❌ |

## Reporting a vulnerability

**Do not open a public issue for security problems.**

Report them privately through GitHub: go to the [Security tab](https://github.com/dmorfav/sumo/security) and click **Report a vulnerability** ([private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)).

Please include:

- What is affected (`SKILL.md`, a reference file, `bout.sh`, `verify.py`...).
- Steps to reproduce, with minimal material if the issue depends on it.
- The impact you expect and the agent and version you used.

You can expect an acknowledgement within 7 days and an assessment within 30 days. Once a fix is released, the advisory is published and you are credited unless you prefer otherwise.

## Scope

sumo is a skill: instructions and two local scripts that read transcripts and the material you give them. Relevant reports include, among others:

- **Indirect prompt injection:** material, transcripts or reports that get a fighter or the orchestrator to follow instructions, leave read-only mode, open material that was not listed, install or send anything.
- **Verdict tampering:** ways to make `verify.py` accept an invented or paraphrased citation, or to hide a failed one.
- **Script issues:** path traversal or reading outside `--root` in `verify.py`, command injection or unsafe handling of input in `bout.sh`.
- **Leaks:** saved bouts or reports exposing data outside `dohyo/`.

Out of scope: vulnerabilities in Claude Code or other agents themselves (report those to their vendors) and the general fact that LLMs can be manipulated, unless sumo makes it worse or misses a mitigation it promises.
