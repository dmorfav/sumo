---
name: sumo
description: Claude Code skill for making hard technical decisions with guarantees. It pits two agents with fixed positions (CRITIC against DEFENDER) in an adversarial debate where they argue directly using mechanically verified citations, while the orchestrator watches without intervening and issues a verdict with the recommended option, confidence, what was conceded, the experiment that would settle the doubt and what would change the decision. Use it for costly decisions where a single model would tend to agree with whoever asks, such as keeping or scrapping a repository, rewriting or refactoring, approving an RFC, design or PR, adopting an architecture, tool, library, vendor or process, or any "should we X or Y". Also trigger on "sumo", "bout", "pit them against each other", "adversarial debate", "have two agents argue", "stress-test this plan", "devil's advocate with evidence", "don't just agree with me" or "I don't trust my gut". Not for line-by-line PR review, single-agent premortems or factual questions.
---

# Sumo

Two fighters (*rikishi*) step into the ring (*dohyō*) with fixed, opposing positions. Whoever leaves the circle loses, that is, whoever runs out of verifiable arguments. You are the referee (*gyōji*): you frame the decision, pair the fighters, watch, verify and deliver the verdict. During the bout you do not speak.

**Language.** These skill files are in English, but you write the fighter prompts, talk to the user and write the verdict in the user's language. The machine keywords `NO ARGUMENTS LEFT` and `FINAL REPORT` always stay literally in English, whatever the language, because the scripts look for them.

**Claude Code first.** The bout needs background subagents that message each other with `SendMessage` (plus `Monitor` and `SubagentHandback`, which have fallbacks). In other environments only the degraded relay mode of step 3 is available.

## Why it works

- **A single model arguing both sides converges toward what the asker thinks**, and consensus formats reward giving in early. Here each position is pushed to the limit by a different agent that cannot switch sides.
- **Two opposing experts help decide better than a single one**, provided the judge can check what they say. That is why every claim carries a citation that `scripts/verify.py` checks mechanically, and you reopen the decisive ones.
- **LLMs give in under pressure even when they are right, and drift from their assigned role.** The fighters' playbook carries explicit rules against that: bounded concessions, and only in the face of verified evidence.

What is still standing after the bout has been tested against a motivated opponent and stops being an opinion. The verdict does not say who debated better: it says what to decide, with what confidence and which data point would change it. The sources are in `docs/research/` in the repository.

## Bout rules (non-negotiable)

1. **Fixed positions.** The CRITIC attacks the motion and the DEFENDER upholds it. Neither lets itself be convinced wholesale.
2. **Only objective arguments.** No "I like it", "I don't like it", "it's elegant" or "it's messy". What counts is what it really contributes or really costs, measured against the criterion.
3. **Own, checkable evidence.** Every claim carries a proof the agent has checked itself: `path:line → «literal»`, a command's output, `git log`, tests, a calculation. A claim without proof does not score.
4. **Surgical concession.** If an agent cannot rebut a specific point, it concedes it explicitly **for that point only** and moves on to another.
5. **End.** The bout ends at the time limit (10 minutes by default) or when an agent writes `NO ARGUMENTS LEFT` on the first line.
6. **The fighters talk to each other.** You do not pass them your analysis or the user's opinion, and you do not act as messenger. Any conclusion that leaks into the prompts biases the bout and takes away the independence that makes it worth anything.

## Flow

### 1. Frame the decision (without analyzing the material)

Settle the following with the user. Do not ask what can be inferred from the conversation; in a non-interactive session, decide with judgment and say so in the verdict.

- **Motion**: a decidable statement, written literally. The fighters will quote it to defend themselves against reframing. ✅ "We should keep repository X instead of rewriting it." ❌ "Let's talk about X."
- **Criterion** both are judged by. Default: maximize software production with guarantees (reproducible, verifiable, traceable, secure, maintainable and with real, demonstrable value). Adapt it to the decision (reliability, cost, deadline, risk…) and say what weighs most. If the criteria are not fixed beforehand, the bout ends up arguing about the criteria instead of the motion.
- **Burden of proof**: it lies with whoever proposes changing the status quo (scrapping, migrating, adopting, rewriting). The status quo has the presumption unless the user says otherwise.
- **What is at stake**: what being wrong costs and whether the decision can be undone. A costly, irreversible decision (scrapping a repository, switching vendor) justifies more time and the other-model auditor (step 6). A cheap, reversible one does not.
- **Material**, read-only: local paths, repositories, documents, URLs. If something has to be cloned, clone it into a temporary directory. The fighters modify nothing, do not commit or push and publish nothing.
- **Duration**: 10 minutes by default, or whatever the user asks. Compute the absolute end time with `date -v+10M +%H:%M` (macOS) or `date -d '+10 min' +%H:%M` (Linux).

Do not investigate the material yourself first. The only thing you prepare is the frame. If you know what is wrong before starting, it shows in how you write the prompts.

Write the frame now to `dohyo/<YYYY-MM-DD>-<slug>/motion.md` (motion, criterion, burden of proof and **who opens**, stakes, material, end time), while you have it in front of you. You will append the two prompts in step 2.

### 2. Launch the fighters

Launch **in the same message** two `general-purpose` agents in the background (`run_in_background: true`), with the same model, because a weak fighter drags down a strong one. Build each prompt with the template in `references/prompts.md` and paste into it the "Fighter playbook" section of `references/playbook.md`, with `{ROLE}`, `{POSITION}` and `{CATALOG_PATH}` (the absolute path of `references/catalog.md`) substituted, and `{{VERIFY_PATH}}` with the absolute path of `scripts/verify.py`, so each fighter checks its citations before sending them. The fighters have no access to this skill, and the playbook is what lets them detect and neutralize the rival's manipulation.

Before launching, append both prompts verbatim to `motion.md`. Note each one's `agentId` and `output_file`.

### 3. Pair them (your only intervention)

With both already launched, send with `SendMessage` **a single message to each**:

- To the one who opens: "Your rival is `<agentId of the other>`. You open."
- To the other: "Your rival is `<agentId of the other>`. They open; wait for their opening argument."

Whoever has the burden of proof opens, that is, whoever argues for changing the status quo:

| The motion… | Example | Burden of proof and opener |
|---|---|---|
| keeps the status quo | "We should keep X", "We should not adopt Y" | CRITIC |
| changes it | "We should migrate to Y", "Approve RFC-7", "Rewrite X" | DEFENDER |

Check the opener against `motion.md` before sending. From then on you do not write to them again until time is up.

**If `SendMessage` is not available** (another environment, another version): no direct bout is possible. Tell the user. If they still want to go ahead, act as a literal relay, forwarding each message in full and unedited, and state in the verdict that it was a relayed bout.

### 4. Watch without intervening

Never read the whole `output_file`, because it overflows your context. Use the scripts (`S` is this skill's `scripts/` folder):

```bash
$S/bout.sh --status CRITIC=<f1> DEFENDER=<f2>              # scoreboard: replies, NO ARGUMENTS LEFT, reports
$S/bout.sh CRITIC=<f1> DEFENDER=<f2>                       # the messages in chronological order
python3 -I $S/verify.py --root <material> CRITIC=<f1> DEFENDER=<f2>   # citations checked so far
```

To wait, use `Monitor` (or a `Bash` loop if you do not have it) that ends when both have delivered their report or the time limit plus 2 minutes has passed:

```bash
until $S/bout.sh --status CRITIC=<f1> DEFENDER=<f2> | grep -q 'Reports delivered: .*,' \
      || [ "$(date +%s)" -ge <limit_epoch_plus_120> ]; do sleep 20; done
```

If the scoreboard shows "Pending: X has not replied…" for more than 2 minutes, the fighter ended its turn and has not resumed. Send it only this: "You have an unanswered message from your rival. Reply to it with SendMessage." This is procedure, not content: do not summarize the rival's message or add anything.

If a fighter delivers its report before exchanging any message (the scoreboard lists it under "Reports delivered" with no messages of its own), it ended its turn before your pairing message arrived. Send it the pairing message again, once, adding: "The bout has not started yet. Do not report; stay in the ring as your instructions say." That uses its pending-reply notice. If it reports alone again, run the bout as relayed for that side and say so in the verdict.

Do not end your turn while the bout lasts. If the user is present, tell them the news in one line (replies, concessions, failed citations), without anticipating the verdict.

**Known behavior:** when a fighter ends its turn and the rival writes to it, it resumes. Its final report (`SubagentHandback`) may end up in the rival's context instead of yours. That is why reports are taken from the transcripts with `bout.sh --reports`, not from the notifications.

### 5. Closing

If time is up and a report is missing, send whoever has not delivered it: "Time. Do not reply to your rival. Deliver your final report now with SubagentHandback, or as text starting with FINAL REPORT if you do not have that tool." This message and the pending-reply notice of step 4 are procedure, not content, and are the only exceptions to not intervening. `bout.sh` and `verify.py` pick up the report in either form.

### 6. Verify before judging

The verdict only gives guarantees if the evidence is real. Convincing text is not enough: it has to be checked.

1. **Mechanical verification.** Run `verify.py --md` on both transcripts. For each citation it says whether the file and lines exist and whether the quoted text is where the fighter says. A failed citation voids the point it supported and lowers the credibility of the rest of that fighter's unverified evidence.
2. **Manual verification of what is decisive.** Identify the arguments that decide: the key concessions, what remained standing and what will ground a recommendation. Reopen 3 to 5 per fighter. Read the line and check that it says what the fighter claims it means, because the script checks that the text exists, not what it means. Rerun the cited commands and counts.
3. **Clean judgment.** Apply the "For the referee" section of `references/playbook.md`: the argument table, the signs of an illegitimate win, the symmetry test (would you give the same verdict with the roles swapped?) and the complacency test (if the verdict matches what the user hinted at, review it more strictly, not less).
4. **Other-model auditor** (for costly or irreversible decisions). If you are the same model as the fighters, you may struggle to see their blind spots. Launch an agent of another model with the motion, `transcript.md`, the output of `verify.py` and the material. Ask it to verify the decisive evidence on both sides and to return a ✔/✘ table, without giving it your provisional verdict.

### 7. Verdict

With this structure:

```markdown
# Sumo: <motion>

**Decision:** <one sentence>. **Confidence:** high | medium | low, because <reason>.
**Criterion:** … · **Bout:** HH:MM–HH:MM, N replies (CRITIC n, DEFENDER m), ended by <NO ARGUMENTS LEFT from X | time>
**Evidence:** N citations, M mechanically verified, K failed · R reopened by hand

## Recommended option
The motion, its opposite or a third way built from what each side conceded. Cross concessions
often sketch a better option than the two initial positions; if so, describe it and say which
piece each side contributes.

## Why
The 3 arguments that decide, each with its evidence (✔ verified by you).

## How the bout went
3–6 lines: opening arguments, turning points and how the disagreement narrowed.

## Concessions
| Conceded by | Point | Evidence that forced it |

## Still standing, unrebutted
By side, with its evidence. What remains standing on the losing side are the risks of the decision.

## Evidence that does not hold
The failed citations and what did not survive your reopening, with what voids it. If there are none, "none".

## Residual disagreement and decisive experiment
What they still disagree on. For each point: the cheapest data point that would settle it, how to
obtain it (command, test, measurement, whom to ask) and what result would change the decision.

## What would change the decision
The concrete conditions that would flip the verdict.

## Action plan
Prioritized. Each step linked to the evidence that justifies it, starting with the risks the losing
side left standing.
```

The verdict decides the motion, not who debated better. The number of replies, who spoke last and who wrote more do not count. A `NO ARGUMENTS LEFT` that arrives after pressure without new evidence is not a clean win, and you say so. A bout that ends on time with important points unanswered leaves those points as residual disagreement, not as anyone's win.

### 8. Save the bout

Save it in `dohyo/<YYYY-MM-DD>-<slug>/`, in the user's working directory:

- `motion.md`: already written in steps 1 and 2 (framing, opener and both prompts); check it is complete.
- `transcript.md`: `$S/bout.sh --md --reports CRITIC=<f1> DEFENDER=<f2> > transcript.md`
- `evidence.md`: `python3 -I $S/verify.py --md --root <material> CRITIC=<f1> DEFENDER=<f2> > evidence.md`
- `verdict.md`: the full verdict from step 7, with all its sections. Write it to the file before showing it, and show the user that same text, so that what is saved and what is said do not differ.

That way anyone can audit the decision later. Bouts often contain internal details (paths, security flaws, names): if `dohyo/` is inside a repository, check that it is in `.gitignore` or ask before it ends up in a commit.

## Variants

- **No code**: if the material is documents or proposals, the evidence is the literal quote with its location (`document.md:line → «literal»`), published data or a reproducible calculation. `verify.py` works the same with any text file.
- **More than two options** (A, B or C): do not put in three fighters. Run one bout per option against today's status quo, or a first bout to eliminate and a final one between the two survivors.
- **Rematch**: if the verdict leaves a concrete, costly residual disagreement, launch a second bout with that disagreement as the motion.
- **More time**: for big decisions, 15–20 minutes. More time does not fix a badly framed motion; fix the motion first.
