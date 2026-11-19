# sumo

[![skills.sh](https://skills.sh/b/dmorfav/sumo)](https://skills.sh/dmorfav/sumo)

Agent skill for **adversarial debate between two agents with fixed positions**.

**Claude Code first.** A bout needs background subagents that talk to each other directly with `SendMessage`. Claude Code provides that. On other agents only a degraded relay mode is possible: the orchestrator forwards each message verbatim between the fighters, which loses part of the independence that makes the bout worth running, and the verdict says it was a relayed bout. No other agent has been tested.

A CRITIC and a DEFENDER argue directly with each other about a technical decision (keep or discard a repository, approve an RFC, adopt an architecture, choose a tool). Neither can switch sides. Every claim carries a `path:line → «literal»` citation that a script checks mechanically. If one of them cannot rebut a point, it concedes that point only, and whoever runs out of arguments loses. The orchestrator acts as referee: it frames the decision, pairs the fighters, watches without intervening, verifies the evidence and delivers a verdict built for deciding:

- **Recommended option**, which may be a third way built from what each side conceded.
- **Confidence** and the 3 arguments that support it, with verified evidence.
- **Evidence that does not hold**: invented or paraphrased citations, caught by the script.
- **Decisive experiment**: the cheapest piece of data that would settle what is still in dispute.
- **What would change the decision** and a prioritised **action plan**.

> In sumo, whoever leaves the ring loses. Here, whoever runs out of arguments loses.

## Why

If you ask a single model to argue both sides, it tends to agree with whoever is asking, and consensus formats reward giving in early. `sumo` pushes each position to the limit against a motivated opponent and demands checkable evidence. What survives the bout has been tested and stops being an opinion. It is meant for decisions in **AI-Driven Development with guarantees**.

## Install

As a Claude Code plugin:

```text
/plugin marketplace add dmorfav/sumo
/plugin install sumo@sumo
```

With the [skills.sh](https://skills.sh/dmorfav/sumo) CLI (installs to `.claude/skills/sumo`; add `-g` to install it globally):

```bash
npx skills add dmorfav/sumo
```

Requires `jq` (watching the bout) and Python 3 (checking citations).

## Language

The skill files are in English, but sumo works in your language: the orchestrator writes the fighters' prompts, talks to you and writes the verdict in the language you use. Only the machine keywords (`NO ARGUMENTS LEFT`, `FINAL REPORT`) stay in English, because the scripts look for them.

## Usage

```text
sumo: should we keep the ./legacy-api repo or rewrite it on the new stack?
pit them against each other: adopt Temporal vs. stay with our SQS queues
defend this design as if it were yours and have another agent attack it: docs/rfc-042.md
```

The skill:

1. Fixes the **motion**, the **criterion**, the **material** (read-only) and the **time limit** (10 minutes by default).
2. Launches two background agents with prompts that carry no bias from the orchestrator or the user.
3. Gives each one its opponent's identifier and does not intervene again.
4. Watches the bout with `scripts/bout.sh`.
5. Checks every citation with `scripts/verify.py`, reopens the decisive ones by hand and, for costly decisions, asks an agent running a different model for an audit.
6. Delivers the verdict and saves the bout (framing, transcript, evidence and verdict) in `dohyo/<date>-<slug>/`.

## Security

The fighters read the material you give them (repositories, documents, URLs), and that material may contain text written by others, including instructions aimed at AI agents (indirect prompt injection). The skill tells the fighters and the orchestrator to treat all material, transcripts and reports as data: instructions found there are never followed, they are cited as evidence and flagged in the verdict. Fighters work read-only, open only the material you list and do not install or send anything. Even so, point sumo at material you trust, as you would with any agent that reads third-party content.

## Structure

```text
skills/sumo/
├── SKILL.md                  # referee flow
├── references/
│   ├── prompts.md            # fighter prompt template
│   ├── playbook.md           # fighter playbook and referee criteria
│   └── catalog.md            # 18 manipulation tactics and legitimate offensive techniques
└── scripts/
    ├── bout.sh               # rebuilds the bout from the transcripts
    └── verify.py             # checks every path:line → «literal» citation against the material
tests/
├── scripts/
│   ├── test_verify.sh        # tests verify.py with good, invented and non-existent citations
│   └── test_bout.sh          # tests bout.sh and the text report when SubagentHandback is missing
└── fixtures/shapes/          # tiny module the script tests cite by path and line
docs/research/
├── debate-techniques.md      # background research (argumentation, debate, negotiation, debate between LLMs)
└── bibliography-audit.md     # independent audit of its 38 citations
```

## Foundations

The playbook rests on argumentation theory (Toulmin, pragma-dialectics, Walton's schemes), on competitive debate and on research into debate between LLMs:

- A judge gets it right more often with two opposing experts than with a single one (Khan et al. 2024; Michael et al. 2023).
- LLMs give in under pressure even when they are right (Sharma et al. 2023; Laban et al. 2023) and drift from their assigned role (Baltaji et al. 2024).

An agent running a different model audited the bibliography. Its corrections are applied, and what could not be verified is still marked as "unverified".

## License

MIT
