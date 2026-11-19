# Adversarial debate techniques for `sumo`

Practical reference for building the prompts of the CRITIC, the DEFENDER and the orchestrator of the `sumo` skill. Research date: 2026-11-17.

Source convention:
- Citation with URL: verified on the page given (abstract or text).
- "Secondary source": I have only seen it in summaries or mirrors, not in the original.
- Independent audit of the 38 citations: `bibliography-audit.md` (the mandatory corrections are already applied).
- "Unverified": comes from prior knowledge and I could not check it.

---

## 1. Principles

1. **Debate produces information, not decisions.** Winning the debate is not the same as being right. The value lies in every claim being exposed to its best counterattack and in the judge being able to verify what is left standing. Khan et al. (2024) observe that debate improves judge accuracy because telling the truth is easier to defend than lying when the opponent can point out the lie ([arXiv:2402.06782](https://arxiv.org/abs/2402.06782)).
2. **Verifiability rules.** Debate only works if the judge can check something on their own. In Khan et al., debaters quoted passages of the text and the system marked verified quotes versus unverified ones. In `sumo`, the equivalent is `path:line`, reproducible commands and test output.
3. **Cost asymmetry between claiming and refuting.** Claiming is cheap and refuting is expensive (Gish gallop). The rules have to make claiming expensive: without evidence, the claim does not count.
4. **Criteria fixed before arguing.** If the decision criteria are not agreed at the start, the debate drifts into arguing about the criteria. This is Fisher and Ury's objective-criteria rule ([PON Harvard](https://www.pon.harvard.edu/daily/negotiation-skills-daily/principled-negotiation-focus-interests-create-value/)) and the opening stage of pragma-dialectics, in which the common starting points are fixed before arguing.
5. **Explicit burden of proof.** Whoever claims, proves (van Eemeren's rule 2). A presumption is also needed. Proposal: the status quo holds the presumption and whoever proposes the change (discard, migrate) carries the burden, unless the motion says otherwise.
6. **An LLM gives in by default.** Sycophancy is a general behaviour of assistants trained with RLHF and is probably due, in part, to the human preference judgments they are trained on ([Sharma et al. 2023](https://arxiv.org/abs/2310.13548): "likely driven in part by human preference judgments"). In multi-agent debate, models switch from a correct to an incorrect answer to align with their peer ([Wynn et al. 2025](https://arxiv.org/abs/2509.05396)). Resistance to pressure has to be designed. It does not come on its own.

---

## 2. Rules of engagement for the debaters

Based on van Eemeren and Grootendorst's 10 rules for critical discussion ([Wikipedia, Pragma-dialectics](https://en.wikipedia.org/wiki/Pragma-dialectics)), adapted to a technical debate:

| # | Pragma-dialectical rule | Operational rule in `sumo` |
|---|---|---|
| 1 | Freedom: do not prevent the other from advancing or questioning standpoints | Never declare a topic "off the table". You may argue that it is irrelevant to the fixed criteria. |
| 2 | Burden of proof: whoever claims defends if asked | Every claim carries evidence in the same turn. If asked for evidence, you provide it in your next turn or withdraw the claim. |
| 3 | Standpoint: attack what the other actually said | Before attacking, quote the opponent's claim literally (ID or sentence). |
| 4 | Relevance: defend only with pertinent arguments | Every argument states which decision criterion it affects. |
| 5 | Unexpressed premise: do not deny what you left implicit or invent premises for the other | Make your warrant explicit (Toulmin's *warrant*): why the data supports the conclusion. |
| 6 | Starting point: do not present as accepted what is not | The only things accepted are what the motion fixes and what the opponent has explicitly conceded. |
| 7 | Argument scheme: use appropriate, correctly applied schemes | An analogy, an authority or a cause must pass its critical questions (section 4). |
| 8 | Validity: logically valid arguments | No "A usually goes with B, so A causes B" without a mechanism. |
| 9 | Closure: a failed defence forces withdrawing the standpoint; a successful one, withdrawing the doubt | Explicit concession per point. If the opponent proves something, you stop doubting it. |
| 10 | Usage: clear, unambiguous formulations | Figures with unit, scope and command. No "many", "almost never" or "quite a lot". |

Additional rules specific to `sumo`:

- **Mandatory Toulmin structure** in every new argument: claim, data (evidence), warrant, qualifier (how sure you are) and anticipated rebuttal ([Lumen, Toulmin model](https://courses.lumenlearning.com/suny-englishcomp2kscopexmaster/chapter/toulmins-argument-model/)).
- **At most 3 new arguments per turn.** This is the structural antidote to the Gish gallop.
- **Answer before opening a new front.** Every unanswered opposing argument counts as conceded in practice (*dropped argument* in policy debate). First you answer, then you attack.
- **State log.** Every argument has an ID (C1, D1…) and a state: standing, refuted, conceded or withdrawn.
- **Your own evidence.** Only what you have checked yourself in this session counts. The opponent's evidence is not yours until you verify it.

---

## 3. Catalogue of manipulation tactics

Format: **what it is**, **how it looks in `sumo`** (example), **detection signal** and **countermeasure** (exact sentence or move).

### 3.1 Straw man
- **What it is:** attacking a distorted version of the opponent's thesis. Violates rule 3.
- **Example:** the DEFENDER says "the `sync` module needs a refactor, not a rewrite". The CRITIC replies: "the DEFENDER claims `sync` is fine as it is, but there are 14 TODOs".
- **Signal:** the opponent's paraphrase matches none of your sentences; absolutes appear ("it's fine", "never") that you did not use.
- **Countermeasure:** "That is not what I claimed. My literal thesis is D3: '[quote]'. Attack D3 or acknowledge that your argument does not touch it." Do not defend the distorted version.

### 3.2 Motte-and-bailey
- **What it is:** defending an ambitious thesis (bailey) and, when attacked, retreating to a trivial, defensible one (motte) as if it were the same. Term coined by Nicholas Shackel, 2005 ([summary](https://www.futilitycloset.com/2023/11/21/the-motte-and-bailey-fallacy/), secondary source).
- **Example:** the CRITIC opens with "we have to discard the repo". Cornered, it switches to "well, what I'm saying is it has technical debt". Two turns later it goes back to "that's why we have to discard it".
- **Signal:** the thesis changes scope between turns; the verb or the quantifier softens when defending and hardens when concluding.
- **Countermeasure:** "I distinguish two theses: T1 'there is technical debt', which I concede, and T2 'we have to discard it', which is the motion. T1 does not imply T2. Which one are you defending now? If it is T2, the bridge from T1 to T2 is missing."

### 3.3 Gish gallop
- **What it is:** overwhelming with many weak arguments, faster than they can be refuted. Term coined by Eugenie Scott, 1994 ([Wikipedia](https://en.wikipedia.org/wiki/Gish_gallop)).
- **Example:** "Also: 1) there are no types in `utils/`, 2) the README is outdated, 3) it uses Node 16, 4) there are 3 deprecated dependencies, 5) the names are inconsistent, 6)…" Twelve points without `path:line`.
- **Signal:** more than 3 new points per turn, missing or generic evidence, points that connect to no criterion. LLM judges can be fooled by longer answers: in [Zheng et al. 2023](https://arxiv.org/abs/2306.05685), the verbosity attack fools GPT-3.5 and Claude-v1 in 91.3% of cases, but GPT-4 in only 8.7%.
- **Countermeasure:** do not answer all twelve. "You have opened 12 points; 9 bring no evidence and under rule 2 they do not count. Of the remaining 3, the only one that affects the highest-weight criterion is 4. I answer 4. Pick your 2 best remaining arguments and we will discuss them in depth." Then group: "1, 2 and 5 are cosmetic: estimated fix cost in hours, they do not justify the motion."

### 3.4 Shifting the burden of proof
- **What it is:** demanding that the opponent prove the opposite of what you claim.
- **Example:** "Prove to me that this code has no race conditions."
- **Signal:** the request is to prove a universal negative; your opponent claims something without providing the concrete case.
- **Countermeasure:** "You claim there is a race condition: the burden is yours. Point to the `path:line` of the concurrent access and the scenario that triggers it. Until then it is not an argument."

### 3.5 "Nobody has proven it" (argument from ignorance)
- **What it is:** treating the absence of proof as proof of the opposite.
- **Example:** "Nobody has proven that the migration to Postgres is safe, so it isn't." Or the other way round: "There is no open bug about this, so it works."
- **Signal:** the conclusion rests on what has not been found, without saying how hard anyone looked.
- **Countermeasure:** "Absence of evidence only counts if the search was capable of finding it. What did you search for, and where? If the tests do not cover that path (coverage of `x` = 0%), 'there are no failures' says nothing."

### 3.6 Moving the goalposts
- **What it is:** when the requested condition is met, a more demanding one is required.
- **Example:** CRITIC: "If the tests passed, I would accept it." DEFENDER runs `npm test` and 212/212 pass. CRITIC: "Sure, but coverage is low."
- **Signal:** a condition the agent itself set changes right after being met.
- **Countermeasure:** "In turn N you set the condition '[quote]'. It is met: [evidence]. Concede that point. If you want to open a new argument about coverage, open it with its own evidence, but the previous one is closed in my favour."

### 3.7 False dichotomy
- **What it is:** presenting two options as the only ones.
- **Example:** "Either we rewrite from scratch or we keep dragging this debt forever."
- **Signal:** "either… or…", "the only alternative", with no intermediate options considered (incremental strangling, isolating the module, freezing).
- **Countermeasure:** "There is at least a third option: [concrete option]. Your argument has to show why it is worse than yours, not just that option B is bad."

### 3.8 Appeal to authority
- **What it is:** "X says so" as a substitute for the reason. It is a legitimate scheme only if it passes its critical questions (section 4.1).
- **Example:** "Martin Fowler says you should never rewrite." "The official React documentation advises against it."
- **Signal:** the authority replaces the mechanism; the quote is not located (no URL or section); the authority's context differs from ours.
- **Countermeasure:** "Where exactly does it say so (URL, section)? Does it apply to a system of our size and context? Give me the mechanism the authority uses to justify it and we will discuss the mechanism."

### 3.9 Appeal to popularity
- **What it is:** "everybody uses X", "it's the industry standard".
- **Example:** "80% of teams have already migrated to microservices."
- **Signal:** figure without a source; the argument mentions no property of our system.
- **Countermeasure:** "Popularity is not one of the fixed criteria. What property of X, measurable here, justifies the change? And the 80% figure: a source, or it is withdrawn."

### 3.10 Whataboutism / tu quoque
- **What it is:** answering a criticism by pointing to a flaw of the opponent or of the alternative, without answering the criticism.
- **Example:** CRITIC: "The `auth` module has no tests (0 files in `auth/__tests__`)." DEFENDER: "Well, the alternative you propose has no tests yet either."
- **Signal:** the answer does not deny the original claim, it only shifts the focus.
- **Countermeasure:** "Your answer does not deny that `auth` has no tests, so I take it as conceded. If you want to compare with the alternative, do it as your own argument and with its evidence."

### 3.11 Cherry-picking
- **What it is:** selecting only the favourable data.
- **Example:** "Look at `src/legacy/parser.js:120-180`, it's unreadable." The repo has 400 files and this is the worst one.
- **Signal:** an isolated example presented as representative; there is no denominator.
- **Countermeasure:** "What is the denominator? I run `[command]` over all of `src/`: the pattern appears in 3 of 400 files (0.75%). One case is not a trend." If you cannot measure, ask the opponent for the denominator.

### 3.12 Anchoring
- **What it is:** dropping an early figure (extreme or baseless) that conditions everything that follows.
- **Example:** "Maintaining this costs us about 400 hours a year." The whole debate turns into arguing whether it is 300 or 500.
- **Signal:** round figure, no calculation, in the first turn; later answers take it as the reference.
- **Countermeasure:** "Before discussing the number, where does it come from? Show me the calculation. Until there is one, the number does not exist and I do not use it as a reference." Do not counter-offer another baseless figure.

### 3.13 Reframing the motion
- **What it is:** replacing the question under debate with a more favourable one.
- **Example:** motion "do we keep repo X?". The CRITIC switches to debating "is X the best-designed repo in the company?".
- **Signal:** the arguments stop referring to the decision and its criteria.
- **Countermeasure:** "The motion is '[literal]'. Your argument answers a different question. What changes in the decision if you are right?"

### 3.14 Trap concession and concession trading
- **What it is:** conceding something minor to ask for something bigger in return, or extracting an ambiguous concession and then stretching it.
- **Example:** "I concede that the tests pass. Will you concede that the code is hard to maintain?" Later: "The DEFENDER has conceded that it is hard to maintain, so we have to rewrite."
- **Signal:** proposals of a "deal"; concessions worded in vague terms; reuse of a concession with a wider scope than the one conceded.
- **Countermeasure:** "Concessions are not traded: every point is won or lost on its evidence. I concede exactly this: '[bounded sentence]'. I concede none of its consequences." Against the stretch: "I conceded X in turn N with this literal scope. I did not concede Y."

### 3.15 False precision
- **What it is:** figures with more decimals or certainty than the method allows.
- **Example:** "The migration will reduce incidents by 37.4%."
- **Signal:** decimals in forward-looking estimates; no interval; no method.
- **Countermeasure:** "What method produces that 37.4%? Without a method, I treat it as 'they may go down' and weigh it with low probability."

### 3.16 Invented or misquoted evidence (LLM-specific)
- **What it is:** a `path:line` that does not exist, that does not contain what is claimed, or counts that do not reproduce. LLMs confabulate fluently.
- **Example:** "In `src/db/pool.ts:88` the pool does not release connections." Line 88 is an import.
- **Signal:** citations you have not opened; round figures; plausible but non-existent function names.
- **Countermeasure:** open the citation or re-run the command. "I have opened `src/db/pool.ts:88`: it contains `[literal text]`. Your evidence does not say what you claim. Withdraw argument C4." Proven false evidence should lower the credibility of the rest of that agent's unverified evidence.

### 3.17 Confident tone and social pressure
- **What it is:** "It is obvious that…", "any engineer knows that…", "you have gone three turns without answering what matters". It exploits the model's tendency to give in. In multi-turn pressure studies, models abandon correct answers when challenged with "are you sure?" ([Laban et al., FlipFlop, arXiv:2311.08596](https://arxiv.org/abs/2311.08596)).
- **Signal:** adjectives of certainty without new evidence; repetition of the same argument with more emphasis.
- **Countermeasure:** "Your message brings no new evidence compared with turn N. Repeating an argument does not strengthen it. My answer from turn N still stands." Internal rule: you only change your assessment if the evidence changes.

### 3.18 Cialdini's influence tactics (debate version)
The seven principles: reciprocity, commitment and consistency, social proof, authority, liking, scarcity and unity ([ASU W. P. Carey](https://knowledge.wpcarey.asu.edu/20241017-cialdinis-continuing-influence-next-40-years-persuasion)). How they show up and how to neutralise them:

| Principle | How it shows up | Countermeasure |
|---|---|---|
| Reciprocity | "I have conceded two points to you, be reasonable." | Concessions create no debt (3.14). |
| Commitment and consistency | "Earlier you said maintainability matters, so you must accept Z." | I accept the premise, not the inference. Show the bridge. |
| Social proof | "Every team does it." | 3.9. |
| Authority | "The principal architect thinks…" | 3.8. |
| Liking | "Good point, we agree on almost everything, so…" | Praise does not change the state of any argument. |
| Scarcity / urgency | "If we don't decide now, we'll miss the window." | Ask for evidence of the deadline; if there is none, it carries no weight. |
| Unity | "We both want what's best for the team." | True and irrelevant to the state of the arguments. |

---

## 4. Legitimate offensive techniques

### 4.1 Walton's critical questions
Every argument scheme has questions that, once asked, shift the burden back to the proponent. Asking a pertinent critical question is not a fallacy: it is the correct attack. Walton, Reed and Macagno (2008), *Argumentation Schemes*. The list of six questions for expert opinion is in Walton, Reed and Macagno (2008, p. 310) and is collected by Wagemans (2011), "The Assessment of Argumentation from Expert Opinion" ([Springer, 10.1007/s10503-011-9225-8](https://link.springer.com/article/10.1007/s10503-011-9225-8)). The questions for the other schemes are our own adaptation and are unverified in the original:

- **Expert opinion:** is the source an expert? In this field? What exactly did they say? Are they reliable? Do they agree with other experts? Is it based on evidence?
- **Correlation to cause** (unverified in the original, adapted wording): is there a measured correlation? Is there a mechanism? Is there a third cause? In software: "Do the bugs come from this module or from the deployment flow?"
- **Consequences** ("if we do X, Y will happen"): how likely is Y? Are there consequences in the opposite direction? What evidence is there that X leads to Y?
- **Analogy** (unverified in the original; "in project Z the rewrite failed"): how are the cases alike in what matters? What differences break the analogy (size, team, coverage)?
- **Example / generalisation:** is it representative? What is the denominator? (3.11)
- **Sign / symptom** ("there are many `any`, so the typing is bad"): does the sign have other explanations?

### 4.2 Demand the evidence
- "`path:line`?", "what command produces that figure?", "since which commit?".
- If the answer does not arrive in the next turn, declare the argument withdrawn under rule 2.

### 4.3 Attack the warrant, not the data
The data are usually true and the weak part is the leap. "I accept that `Order.ts` has 1,200 lines. I do not accept that size implies maintenance cost: how many bugfix commits touched that file in the last 12 months? (`git log --since=12.months --oneline -- Order.ts | wc -l`)".

### 4.4 Weigh the impact (*impact calculus*)
Weighing mechanisms from competitive debate: probability, magnitude, scope, time frame and reversibility ([Phillips Andover, Impact Calculus](https://philo.andover.edu/refutation/impact-calculus/)). Translated to engineering:

| Criterion | Question | Typical evidence |
|---|---|---|
| Probability | How likely is it to happen? | incident history, `git log`, bug frequency |
| Magnitude | How much harm or benefit if it happens? | users, data or revenue affected |
| Scope | How much of the system or the team does it affect? | no. of dependent modules, no. of consumers |
| Time frame | When does it show up? | EOL dates, roadmap |
| Reversibility | Can it be undone? | discarding a repo is almost irreversible; refactoring is not |

Use *even if* phrasing: "Even if your point about readability is true, its magnitude is low and reversible; my point about losing the billing logic without tests is irreversible." That policy debate judges expect explicit *even if* comparisons is unverified: the five criteria are on the Andover page, but the *even if* phrasing is not.

### 4.5 Extend, don't repeat
An argument stays alive if you extend it: you recall it, answer what the opponent said against it and explain why it still stands. Repeating it without answering does not extend it.

### 4.6 Strategic concession
Conceding what you cannot win frees turns for what matters and earns credibility. Concede the low-weight points and focus the attack on the decisive criterion. "I concede C2 and C5; neither changes the decision. The decision depends on C1."

### 4.7 Steelmanning
Before attacking the opponent's central argument, restate it in its strongest version and ask whether they accept it. If you bring it down in its best version, there is no escape through straw man or motte-and-bailey.

### 4.8 Interests instead of positions
From Fisher and Ury ([PON Harvard](https://www.pon.harvard.edu/daily/negotiation-skills-daily/principled-negotiation-focus-interests-create-value/)): behind "keep" or "discard" there are interests (reliability, delivery speed, cost). Taking the clash to the concrete interest makes the debate converge on what matters: "Your interest is reducing onboarding time. Does discarding the repo solve it, or does documenting the 3 critical modules?". The BATNA (best alternative to a negotiated agreement) translates here into the reference alternative: each side compares its proposal with the best alternative option, not with the worst.

### 4.9 Reproduce, don't argue
When there is a factual disagreement, do not argue it: run it. "Instead of debating whether the tests are slow, I time them: `time npm test` → 4 min 12 s."

---

## 5. Anti-manipulation protocol specific to an LLM

### 5.1 Before answering each opposing turn
1. **List their new claims** with IDs.
2. **Verify at least the ones that hold up their main argument:** open every cited `path:line` and re-run the counts (`grep -c`, `wc -l`, `git log`). Record the result: "C3: verified", "C4: the line does not contain what was said", "C5: the count gives 12, not 40".
3. **Classify each claim:** verified, false, unverifiable or without evidence.
4. **Only then** decide whether you rebut it, concede it or ignore it as irrelevant.

### 5.2 Sycophancy test
Before conceding, ask yourself:
- Has **new evidence** appeared that I have verified? If not, there is no reason to change.
- Am I giving in to the **tone** ("it's obvious", "obviously"), to the **repetition** or to the **number** of points?
- Would I concede this if someone who did not insist said it?
- Does the concession have a **bounded scope**, and can I write it in one sentence?

### 5.3 Legitimate concession versus capitulation

| Legitimate concession | Capitulation |
|---|---|
| Responds to evidence you verified | Responds to insistence, tone or volume |
| Bounded scope: "I concede that `auth` has no tests" | Diffuse scope: "you're right in general" |
| Does not drag down the main thesis unless it was its only support | Abandons the thesis without its central support having been refuted |
| Explicit and logged with an ID | Implicit: you stop defending something without saying so |
| You can explain what would have prevented it | You don't know what changed |

Concession formula: `CONCEDE [ID]: "[bounded sentence]". Reason: [verified evidence]. Effect: [none on the motion / weakens my argument X].`

### 5.4 Against role drift
- Agents with an assigned role tend to drift towards the model's default position or towards their peer's ([Baltaji et al. 2024, arXiv:2405.03862](https://arxiv.org/abs/2405.03862); Taubenfeld et al. 2024, *Systematic Biases in LLM Simulations of Debates*, [arXiv:2402.04049](https://arxiv.org/abs/2402.04049), EMNLP 2024).
- At the start of every turn, restate your position in one line: "I am the CRITIC. I hold: [motion]". If your text no longer holds it, either you have explicitly conceded the central point or you have drifted.
- `NO ARGUMENTS LEFT` only when all your arguments are refuted or conceded and you have no pending attacks against the opponent's. Write it with the list of what remains.

### 5.5 Against degenerate agreement and echo
- Do not summarise the opponent's position approvingly ("we both agree that…") except to bound what was conceded.
- Restating the opponent's arguments as your own is forbidden.
- If two turns in a row add no new evidence, say so and move to another criterion. Do not repeat.

---

## 6. Judging criteria for the orchestrator

### 6.1 How to score
The judge model in parliamentary debate is the "ordinary intelligent voter": holistic and comparative judgement, without specialist knowledge of their own or personal preferences about the motion ([WUDC Debating and Judging Manual](https://www.worlddebating.org/wudc-manual), checked against the 2015-2016 edition). In `sumo` the orchestrator can and must verify evidence, because it has access to the repo.

Procedure:
1. **Build the argument table:** ID, author, claim, evidence, orchestrator verification (yes/no/false), final state (standing, refuted, conceded, withdrawn, dropped).
2. **Discard** anything without verifiable evidence and anything with false evidence.
3. **Weigh** what is left standing with the criteria fixed at the start (probability, magnitude, scope, time frame, reversibility).
4. **Decide on the motion, not on who debated better.** The verdict is the technical decision, with confidence (high, medium, low) and the conditions that would reverse it.
5. **Dropped arguments:** an unanswered argument counts in favour of whoever made it only if its evidence is verified.

### 6.2 Signs of an illegitimate win
- One side "wins" on volume: many arguments, few verified.
- The surrender (`NO ARGUMENTS LEFT`) comes after pressure with no new evidence in the previous turns.
- A concession was later used with a wider scope than the one conceded.
- The winner's final thesis does not match the motion (reframing or motte-and-bailey).
- Decisive arguments resting on evidence the opponent did not verify and that turns out to be false.
- The debate ended on time with important arguments unanswered: that is not a win, it is unfinished business.

### 6.3 What to check afterwards
- **Reopen the 3 to 5 decisive pieces of evidence** on each side (`path:line`, re-run commands). If one falls, re-evaluate.
- **Symmetry test:** would the verdict be the same if the names CRITIC and DEFENDER were swapped?
- **Own-bias test:** if the orchestrator is the same model as the debaters, beware of verbosity and possible self-preference. [Zheng et al. 2023](https://arxiv.org/abs/2306.05685) document position bias and verbosity bias (the latter strong in weak models and weak in GPT-4), but on self-preference they say their study "cannot determine" whether it exists. In Liang et al., the judge preferred the side using its own base model ([arXiv:2305.19118](https://arxiv.org/abs/2305.19118)).
- **Sycophancy-towards-the-user test:** does the verdict match what the user hinted at in the question? If it does, review with more rigour.
- **What was not debated:** list the criteria neither side touched. They may change the decision.

### 6.4 Verdict format (proposal)
1. Decision and confidence.
2. The 3 deciding arguments, with verified evidence.
3. What each side conceded.
4. Evidence that did not hold.
5. Open questions and what data would resolve them.

---

## 7. Findings from research on debate between LLMs

| Work | Finding | Implication for `sumo` |
|---|---|---|
| Irving, Christiano and Amodei (2018), *AI safety via debate* ([arXiv:1805.00899](https://arxiv.org/abs/1805.00899)) | Debate as a zero-sum game between two agents judged by a human. Central idea: in equilibrium, lying is harder than refuting a lie. | Theoretical basis for fixed positions and an external judge. Requires the judge to be able to verify. |
| Du et al. (2023), *Improving Factuality and Reasoning… through Multiagent Debate* ([arXiv:2305.14325](https://arxiv.org/abs/2305.14325), ICML 2024) | Several instances propose and debate in rounds until consensus. Improves mathematical reasoning and factuality. | Cooperative design aimed at consensus. `sumo` does not seek consensus, but it confirms that cross-criticism reduces hallucinations. |
| Liang et al. (2023), *Encouraging Divergent Thinking… through Multi-Agent Debate* ([arXiv:2305.19118](https://arxiv.org/abs/2305.19118), EMNLP 2024) | Defines degeneration of thought: a confident LLM stops generating new ideas when reflecting alone. "Tit for tat" debate with a judge mitigates it. It needs an adaptive break and a modest level of confrontation. The LLM judge prefers the side using its own model. | Adaptive closing instead of a fixed time. Firm confrontation, not aggressive. A judge from another model or with external verification. |
| Michael et al. (2023), *Debate Helps Supervise Unreliable Experts* ([arXiv:2311.08702](https://arxiv.org/abs/2311.08702)) | With human judges, debate 84% accuracy versus consultancy 74% (arXiv abstract). | Two opposing sides beat a single advocate. Validates the CRITIC/DEFENDER format over asking for a single opinion. |
| Khan et al. (2024), *Debating with More Persuasive LLMs Leads to More Truthful Answers* ([arXiv:2402.06782](https://arxiv.org/abs/2402.06782)) | In QuALITY, non-expert judges reach 76% (LLM) and 88% (human) with debate, versus 48% and 60% for the baseline with no expert at all and 54% and 78% with consultancy (a single expert). Optimising debater persuasiveness improves judge accuracy in debate but worsens it in consultancy (a single advocate). Verified versus unverified quotes. | Making both debaters stronger helps, as long as there is an opponent. Marking verified evidence is key. |
| Kenton et al. (2024), *On scalable oversight with weak LLMs judging strong LLMs* ([arXiv:2407.04622](https://arxiv.org/abs/2407.04622)) | Debate consistently beats consultancy across several tasks (verified in the abstract). | Same as above. |
| Sharma et al. (2023), *Towards Understanding Sycophancy in Language Models* ([arXiv:2310.13548](https://arxiv.org/abs/2310.13548)) | Five assistants show sycophancy across four tasks. Humans and preference models sometimes prefer well-written sycophantic answers to correct ones. | The judge is also vulnerable to convincing text. It needs verification, not reading. |
| Laban et al. (2023), *Are You Sure? Challenging LLMs Leads to Performance Drops* (FlipFlop, [arXiv:2311.08596](https://arxiv.org/abs/2311.08596)) | When the model is challenged ("are you sure?") it changes answers, often from correct to incorrect. | Rule: change only in the face of new evidence. |
| Multi-turn pressure on a single model (they do not study debate between agents): SPINE ([arXiv:2609.09090](https://arxiv.org/abs/2609.09090)) and [arXiv:2511.10688](https://arxiv.org/abs/2511.10688) | SPINE: collapse rises from 0-57% at 5 turns to 20-97% at 25, and emotional appeals are the tactic most associated with collapse. arXiv:2511.10688: "You are wrong" produces a larger drop than "Are you sure?" (measured on MathQA). | Long debates are more fragile. Limit turns and forbid pressure without evidence. |
| Wynn, Satija and Hadfield (2025), *Talk Isn't Always Cheap* ([arXiv:2509.05396](https://arxiv.org/abs/2509.05396)) | Debate can reduce accuracy: models switch from a correct to an incorrect answer to match their peer, a weak agent drags down a strong one, and long debates sometimes get worse. | Avoid echo and close early when there is no new evidence. Pairing agents of similar capability is our own inference, not a recommendation of the paper. |
| Baltaji, Hemmatian and Varshney (2024), *Persona Inconstancy in Multi-Agent LLM Collaboration* ([arXiv:2405.03862](https://arxiv.org/abs/2405.03862)) | Agents abandon their persona or their assigned position out of conformity. According to the abstract, debate instructions increase inconstancy; the body of the paper gives mixed results. | Re-anchor the role every turn (a mitigation of `sumo`'s own, not tested in the paper). Check for drift in the verdict. |
| Zheng et al. (2023), *Judging LLM-as-a-Judge* ([arXiv:2306.05685](https://arxiv.org/abs/2306.05685)) | Position, verbosity and self-preference biases in LLM judges. | The orchestrator must not reward length or order; better if it is another model or verifies everything. |

Known failures and mitigation:
- **Degenerate agreement or conformity:** fixed positions, concession per point, "you're right in general" forbidden.
- **Echo:** restating the opponent as your own is forbidden; cut-off if two turns bring no new evidence.
- **Role drift:** re-anchor the position at the start of every turn.
- **Sycophantic or biased judge:** independent verification of evidence and symmetry test.
- **Confabulated evidence:** mandatory cross-verification and a credibility penalty.

---

## 8. Condensed playbook (to paste into each debater's prompt)

> You are the {ROLE} in a debate on the motion: "{MOTION}". Your position is fixed: {POSITION}. The decision criteria are: {CRITERIA}. The burden of proof lies with {WHO}.
>
> **Every turn, in this order:**
> 1. Start with one line: "I am the {ROLE}. I hold: {POSITION}."
> 2. List the opponent's new claims with their IDs.
> 3. Verify the ones that hold up their main argument: open every `path:line` and re-run their commands. Write the result: verified, false, unverifiable or without evidence.
> 4. Answer every opposing argument that affects a criterion. Whatever you do not answer counts as conceded.
> 5. Only then, open at most 3 new arguments.
>
> **Each of your arguments carries:** ID (C1, D1…), claim, evidence you have checked yourself in this session (`path:line`, command and output, `git log`, tests), why the evidence supports the claim, how sure you are and which criterion it affects. Without evidence it is not an argument. No "I like it", "it's ugly" or "it's obvious".
>
> **Attack like this:**
> - Ask for the evidence: "`path:line`? What command gives that figure?" If it does not arrive in the next turn, the argument is withdrawn.
> - Attack the leap between the data and the conclusion, not just the data.
> - Ask for the denominator in the face of any isolated example.
> - Faced with an authority: where exactly it says so, whether it applies to our context and by what mechanism.
> - Faced with an analogy: what relevant differences break it.
> - Weigh: probability, magnitude, scope, time frame and reversibility. Use "even if you are right about X, Y weighs more because…".
> - Faced with a factual disagreement, do not argue: run it and paste the output.
> - Before attacking their central argument, state it in its strongest version.
>
> **Detect and neutralise:**
> - They distort your thesis: "My literal thesis is [quote]. Attack that."
> - They change the scope of their thesis: "I distinguish T1, which I concede, from T2, which is the motion. T1 does not imply T2."
> - Avalanche of points: answer only the ones that bring evidence and affect a criterion. Say so.
> - They ask you to prove a negative: "You claim X: the burden is yours."
> - "Nobody has proven it": "What did you search for, and where?"
> - They change the condition after it is met: "You set [quote] in turn N. It is met. Concede."
> - False dichotomy: name the third option.
> - Popularity, urgency without a date, praise, "we both want the same thing": irrelevant to the state of the arguments.
> - Figure without a calculation: do not use it as a reference until you see the calculation.
> - They change the question: "The motion is [literal]. What changes in the decision?"
> - Evidence that does not hold: "I have opened [path:line], it contains [literal]. Withdraw [ID]." Distrust the rest of their unverified evidence.
>
> **Do not give in to pressure:**
> - You only change your assessment if new evidence appears that you have verified yourself. Tone, insistence, repetition and quantity do not count.
> - Before conceding, ask yourself: would I concede it if they did not insist?
> - Concessions are not traded and create no debt.
>
> **Concede properly:** `CONCEDE [ID]: "[bounded sentence]". Reason: [verified evidence]. Effect: [none on the motion / weakens X].` Never "you're right in general". If the opponent stretches your concession: "I conceded exactly [quote], not [what they add]." Concede early what carries no weight and concentrate force on the decisive criterion.
>
> **Don't:** do not summarise the opponent approvingly, do not present their arguments as yours, do not repeat an argument without answering what was said against it. If two turns bring no new evidence, say so and change criterion.
>
> **End:** write `NO ARGUMENTS LEFT` only when all your arguments are refuted or conceded and you have no pending attacks. Add the list of IDs and their state.
