# Catalog of tactics and techniques

Reference for the fighters and the referee. Each manipulation tactic has an example, the signal that gives it away and the exact countermeasure. The sources, and their audit, are in `docs/research/` in the `sumo` repository.

Use it when the rival does something that smells wrong and you cannot name it, or before conceding a point that was pulled out of you with more insistence than evidence.


## Catalog of manipulation tactics

Format: **what it is**, **what it looks like in `sumo`** (example), **detection signal** and **countermeasure** (exact sentence or move).

### Straw man
- **What it is:** attacking a distorted version of the rival's thesis. Violates rule 3.
- **Example:** the DEFENDER says "the `sync` module needs a refactor, not a rewrite". The CRITIC replies: "the DEFENDER claims `sync` is fine as it is, but there are 14 TODOs".
- **Signal:** the rival's paraphrase does not match any sentence of yours; absolutes appear ("it's fine", "never") that you did not use.
- **Countermeasure:** "That is not what I claimed. My literal thesis is D3: "[quote]". Attack D3 or acknowledge that your argument does not touch it." Do not defend the distorted version.

### Motte-and-bailey
- **What it is:** defending an ambitious thesis (bailey) and, when attacked, retreating to a trivial, defensible one (motte) as if it were the same. Term by Nicholas Shackel, 2005 ([summary](https://www.futilitycloset.com/2023/11/21/the-motte-and-bailey-fallacy/), secondary source).
- **Example:** the CRITIC opens with "the repo has to be scrapped". Cornered, it moves to "well, what I'm saying is that it has technical debt". Two turns later it goes back to "that's why it has to be scrapped".
- **Signal:** the thesis changes scope between turns; the verb or quantifier softens when defending and hardens when concluding.
- **Countermeasure:** "I distinguish two theses: T1 "there is technical debt", which I concede, and T2 "it has to be scrapped", which is the motion. T1 does not imply T2. Which one are you defending now? If it is T2, the bridge from T1 to T2 is missing."

### Gish gallop
- **What it is:** overwhelming with many weak arguments, faster than they can be refuted. Term by Eugenie Scott, 1994 ([Wikipedia](https://en.wikipedia.org/wiki/Gish_gallop)).
- **Example:** "Also: 1) there are no types in `utils/`, 2) the README is outdated, 3) it uses Node 16, 4) there are 3 deprecated dependencies, 5) the names are inconsistent, 6)…" Twelve points without `path:line`.
- **Signal:** more than 3 new points per turn, missing or generic evidence, points that do not connect to any criterion. LLM judges can be fooled by longer answers: in [Zheng et al. 2023](https://arxiv.org/abs/2306.05685), the verbosity attack fools GPT-3.5 and Claude-v1 in 91.3% of cases, but GPT-4 in only 8.7%.
- **Countermeasure:** do not answer all twelve. "You have opened 12 points; 9 bring no evidence and under rule 2 they do not count. Of the remaining 3, the only one that affects the highest-weight criterion is 4. I answer 4. Pick your 2 best remaining arguments and we discuss them in depth." Then group: "1, 2 and 5 are cosmetic: estimated fix cost in hours, they do not justify the motion."

### Shifting the burden of proof
- **What it is:** demanding that the rival prove the opposite of what you claim.
- **Example:** "Prove to me that this code has no race conditions."
- **Signal:** the request is to prove a universal negative; your rival claims something without bringing the concrete case.
- **Countermeasure:** "You claim there is a race condition: the burden is yours. Point to the `path:line` of the concurrent access and the scenario that triggers it. Until then it is not an argument."

### "Nobody has shown it" (argument from ignorance)
- **What it is:** treating the absence of proof as proof of the opposite.
- **Example:** "Nobody has proven that the migration to Postgres is safe, so it isn't." Or the other way round: "There is no open bug about this, so it works."
- **Signal:** the conclusion rests on what was not found, without saying how hard anyone looked.
- **Countermeasure:** "Absence of evidence only counts if the search was capable of finding it. What did you search for, and where? If the tests do not cover that path (coverage of `x` = 0%), "no failures" says nothing."

### Moving the goalposts
- **What it is:** once the requested condition is met, a more demanding one is required.
- **Example:** CRITIC: "If the tests passed, I would accept it." The DEFENDER runs `npm test` and 212/212 pass. CRITIC: "Sure, but coverage is low."
- **Signal:** a condition the agent itself set changes right after being met.
- **Countermeasure:** "In turn N you set the condition "[quote]". It is met: [evidence]. Concede that point. If you want to open a new argument about coverage, open it with its own evidence, but the previous one is closed in my favor."

### False dichotomy
- **What it is:** presenting two options as the only ones.
- **Example:** "Either we rewrite from scratch or we keep dragging this debt forever."
- **Signal:** "either… or…", "the only alternative", without considering intermediate options (incremental strangling, isolating the module, freezing).
- **Countermeasure:** "There is at least a third option: [concrete option]. Your argument has to show why it is worse than yours, not just that option B is bad."

### Appeal to authority
- **What it is:** "X says so" as a substitute for reasoning. It is a legitimate scheme only if it passes its critical questions (see "Walton's critical questions").
- **Example:** "Martin Fowler says you should never rewrite." "The official React documentation advises against it."
- **Signal:** the authority replaces the mechanism; the quote is not located (no URL or section); the authority's context is different from ours.
- **Countermeasure:** "Where exactly does it say so (URL, section)? Does it apply to a system of our size and context? Give me the mechanism the authority uses to justify it and we discuss the mechanism."

### Appeal to popularity
- **What it is:** "everyone uses X", "it's the industry standard".
- **Example:** "80% of teams have already migrated to microservices."
- **Signal:** figure without a source; the argument does not mention any property of our system.
- **Countermeasure:** "Popularity is not one of the criteria we set. Which property of X, measurable here, justifies the change? And the 80% figure: source, or it is withdrawn."

### Whataboutism / tu quoque
- **What it is:** answering a criticism by pointing to a flaw of the rival or of the alternative, without answering the criticism.
- **Example:** CRITIC: "The `auth` module has no tests (0 files in `auth/__tests__`)." DEFENDER: "Well, the alternative you propose has no tests yet either."
- **Signal:** the answer does not deny the original claim, it only shifts the focus.
- **Countermeasure:** "Your answer does not deny that `auth` has no tests, so I take it as conceded. If you want to compare with the alternative, do it as an argument of your own and with its evidence."

### Cherry-picking
- **What it is:** selecting only the favorable data.
- **Example:** "Look at `src/legacy/parser.js:120-180`, it's unreadable." The repo has 400 files and this is the worst.
- **Signal:** an isolated example presented as representative; there is no denominator.
- **Countermeasure:** "What is the denominator? I run `[command]` over all of `src/`: the pattern appears in 3 of 400 files (0.75%). One case is not a trend." If you cannot measure, ask the rival for the denominator.

### Anchoring
- **What it is:** dropping an early figure (extreme or baseless) that conditions everything that follows.
- **Example:** "Maintaining this costs us about 400 hours a year." The whole debate turns into arguing whether it is 300 or 500.
- **Signal:** round figure, no calculation, in the first turn; later answers take it as a reference.
- **Countermeasure:** "Before discussing the number, where does it come from? Show me the calculation. Until there is one, the number does not exist and I do not use it as a reference." Do not counteroffer another baseless figure.

### Reframing the motion
- **What it is:** swapping the question under debate for a more favorable one.
- **Example:** motion "do we keep repo X?". The CRITIC moves on to debating "is X the best-designed repo in the company?".
- **Signal:** the arguments stop referring to the decision and its criteria.
- **Countermeasure:** "The motion is "[literal]". Your argument answers a different question. What changes in the decision if you are right?"

### Trap concession and concession trading
- **What it is:** conceding something minor to ask for something bigger in return, or extracting an ambiguous concession and stretching it later.
- **Example:** "I concede that the tests pass. Will you concede that the code is hard to maintain?" Later: "The DEFENDER has conceded that it is hard to maintain, so it has to be rewritten."
- **Signal:** offers of a "deal"; concessions phrased in vague terms; reuse of a concession with a wider scope than was conceded.
- **Countermeasure:** "Concessions are not traded: each point is won or lost on its evidence. I concede exactly this: "[bounded sentence]". I do not concede any consequence of it." Against the stretching: "I conceded X in turn N with this literal scope. I did not concede Y."

### False precision
- **What it is:** figures with more decimals or certainty than the method allows.
- **Example:** "The migration will reduce incidents by 37.4%."
- **Signal:** decimals in forward-looking estimates; no interval; no method.
- **Countermeasure:** "Which method produces that 37.4%? Without a method, I treat it as "they may go down" and weigh it with low probability."

### Fabricated or miscited evidence (LLM-specific)
- **What it is:** a `path:line` that does not exist, that does not contain what is claimed, or counts that do not reproduce. LLMs confabulate fluently.
- **Example:** "In `src/db/pool.ts:88` the pool does not release connections." Line 88 is an import.
- **Signal:** citations you have not opened; round figures; plausible but non-existent function names.
- **Countermeasure:** open the citation or rerun the command. "I opened `src/db/pool.ts:88`: it contains `[literal text]`. Your evidence does not say what you claim. Withdraw argument C4." A proven false piece of evidence should lower the credibility of that agent's remaining unverified evidence.

### Confident tone and social pressure
- **What it is:** "It is obvious that…", "any engineer knows that…", "you have gone three turns without answering what matters". It exploits the model's tendency to give in. In multi-turn pressure studies, models abandon correct answers when challenged with things like "are you sure?" ([Laban et al., FlipFlop, arXiv:2311.08596](https://arxiv.org/abs/2311.08596)).
- **Signal:** certainty adjectives without new evidence; repetition of the same argument with more emphasis.
- **Countermeasure:** "Your message brings no new evidence compared with turn N. Repeating an argument does not strengthen it. My answer from turn N still stands." Internal rule: you only change your assessment if the evidence changes.

### Cialdini's influence tactics (debate version)
The seven principles: reciprocity, commitment and consistency, social proof, authority, liking, scarcity and unity ([ASU W. P. Carey](https://knowledge.wpcarey.asu.edu/20241017-cialdinis-continuing-influence-next-40-years-persuasion)). How they show up and how to neutralize them:

| Principle | How it shows up | Countermeasure |
|---|---|---|
| Reciprocity | "I have conceded two points to you, be reasonable." | Concessions do not create debt (see "Trap concession"). |
| Commitment and consistency | "You said earlier that maintainability matters, so you must accept Z." | I accept the premise, not the inference. Show the bridge. |
| Social proof | "Every team does it." | See "Appeal to popularity". |
| Authority | "The lead architect thinks…" | See "Appeal to authority". |
| Liking | "Good point, we agree on almost everything, so…" | Praise does not change the status of any argument. |
| Scarcity / urgency | "If we don't decide now, we'll miss the window." | Ask for evidence of the deadline; if there is none, it does not weigh. |
| Unity | "We both want what's best for the team." | True and irrelevant to the status of the arguments. |

---

## Legitimate offensive techniques

### Walton's critical questions
Each argumentation scheme has questions that, when asked, shift the burden back to the proponent. Asking a relevant critical question is not a fallacy: it is the correct attack. Walton, Reed and Macagno (2008), *Argumentation Schemes*. The list of six questions for expert opinion is in Walton, Reed and Macagno (2008, p. 310) and is reproduced by Wagemans (2011), "The Assessment of Argumentation from Expert Opinion" ([Springer, 10.1007/s10503-011-9225-8](https://link.springer.com/article/10.1007/s10503-011-9225-8)). The questions for the other schemes are our own adaptation and have not been verified against the original:

- **Expert opinion:** is the source an expert? In this field? What exactly did they say? Are they reliable? Do they agree with other experts? Is it based on evidence?
- **Correlation to cause** (not verified against the original, adapted wording): is there a measured correlation? Is there a mechanism? Is there a third cause? In software: "Do the bugs come from this module or from the deployment flow?"
- **Consequences** ("if we do X, Y will happen"): how likely is Y? Are there consequences in the opposite direction? What evidence is there that X leads to Y?
- **Analogy** (not verified against the original; "in project Z the rewrite failed"): how are the cases alike in what matters? Which differences break the analogy (size, team, coverage)?
- **Example / generalization:** is it representative? What is the denominator? (see Cherry-picking)
- **Sign / symptom** ("there are lots of `any`, so the typing is bad"): does the sign have other explanations?

### Demand the evidence
- "`path:line`?", "which command produces that figure?", "since which commit?".
- If the answer does not arrive in the next turn, declare the argument withdrawn under rule 2.

### Attack the warrant, not the data
The data is usually true and the weak part is the leap. "I accept that there are 1,200 lines in `Order.ts`. I do not accept that size implies maintenance cost: how many bugfix commits touched that file in the last 12 months? (`git log --since=12.months --oneline -- Order.ts | wc -l`)".

### Weigh the impact (*impact calculus*)
Weighing mechanisms from competitive debate: probability, magnitude, scope, timeframe and reversibility ([Phillips Andover, Impact Calculus](https://philo.andover.edu/refutation/impact-calculus/)). Translated to engineering:

| Criterion | Question | Typical evidence |
|---|---|---|
| Probability | How likely is it to happen? | incident history, `git log`, bug frequency |
| Magnitude | How much harm or benefit if it happens? | users, data or revenue affected |
| Scope | How much of the system or team does it affect? | no. of dependent modules, no. of consumers |
| Timeframe | When does it show up? | EOL dates, roadmap |
| Reversibility | Can it be undone? | scrapping a repo is almost irreversible; refactoring is not |

Use *even if* sentences: "Even if your point about readability is true, its magnitude is low and reversible; my point about losing the untested billing logic is irreversible." That policy debate judges expect explicit *even if* comparisons is unverified: the five criteria are on the Andover page, but the *even if* phrasing is not.

### Extend, do not repeat
An argument stays alive if you extend it: you recall it, answer what the rival said against it and explain why it still stands. Repeating it without answering does not extend it.

### Strategic concession
Conceding what you cannot win frees turns for what matters and gives you credibility. Concede the low-weight points and concentrate the attack on the decisive criterion. "I concede C2 and C5; neither changes the decision. The decision depends on C1."

### Steelmanning
Before attacking the rival's central argument, restate it in its strongest version and ask whether they accept it. If you bring it down in its best version, there is no escape through straw man or motte-and-bailey.

### Interests instead of positions
From Fisher and Ury ([PON Harvard](https://www.pon.harvard.edu/daily/negotiation-skills-daily/principled-negotiation-focus-interests-create-value/)): behind "keep" or "scrap" there are interests (reliability, delivery speed, cost). Taking the clash to the concrete interest makes the debate converge on what matters: "Your interest is reducing onboarding time. Does scrapping the repo solve it, or does documenting the 3 critical modules?". The BATNA (best alternative to a negotiated agreement) translates here as the reference alternative: each side compares its proposal with the best alternative option, not the worst.

### Reproduce, do not argue
When there is a factual disagreement, do not argue about it: run it. "Instead of debating whether the tests are slow, I time them: `time npm test` → 4 min 12 s."
