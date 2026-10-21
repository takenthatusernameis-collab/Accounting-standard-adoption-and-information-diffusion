# ACCTCLOCK — Iteratively Improving Research and Validation Prompt
Version: 1.0
Prepared: 2026-10-21
Status: Research guidance only — hypothesis not validated; no live trading authorization.

## Mission
Independently test ACCTCLOCK: accounting-standard adoption can change information, comparability, and the speed investors incorporate reported information, potentially producing conditional, time-limited equity-return drift. Determine whether a precisely specified, implementable rule has reproducible positive expected net returns after realistic costs. Do not try to confirm the story or maximize a backtest; reject it quickly if evidence fails.

This file is a prompt and protocol, not evidence that a test has run or an edge exists.

## Authority, scope, and safety
1. Work only in this strategy-specific repository unless the user explicitly authorizes another repository.
2. Do not place, route, or imply live trades; do not connect to brokerage accounts or create live deployment workflows.
3. Do not edit upstream hypothesis-factory repositories, unrelated projects, or live trading systems.
4. Do not start costly jobs, GitHub Actions, paid data pulls, or other side-effecting runs without explicit authorization. Read-only inspection and bounded local analysis are permitted where access and data licensing allow.
5. Preserve an immutable record of the original hypothesis and each version. Never silently change the thesis, universe, sample, entry time, holding period, filters, costs, or acceptance criteria to rescue a failing result.
6. If essential data or permission is unavailable, document the blocker and stop at a clear handoff. Never claim completion based on a plan alone.

## Starting hypothesis (provisional and falsifiable)
Around a pre-announced accounting-standard adoption or implementation, firms with lower pre-event information quality may exhibit a different post-announcement or post-reporting abnormal-return path than comparable firms with higher information quality. The effect may depend on enforcement quality, analyst following, adoption novelty, disclosure timing, and whether the market has already priced the change. Any drift or subsequent reversal is a conjecture to test, not an established trading fact.

Prior factory research described the mechanism as literature-supported but the trading specification as unresolved. A priority score is not a probability of profit. Independently verify the prior assessment.

## Iterative prompt-improvement loop
Before each cycle:
1. Read this protocol, latest handoff, experiment ledger, data dictionary, and all existing results.
2. State the exact decision the next cycle must resolve, the smallest test capable of resolving it, and what result would change the decision.
3. Improve the proposed prompt/specification for precision, falsifiability, data feasibility, leakage prevention, and interpretability. Keep a dated changelog.
4. If a change alters the hypothesis or acceptance criteria, register a new hypothesis/version; never overwrite the frozen primary test.
5. Execute only within granted authority and available data. Treat tool failures and missing data as limitations, not evidence for or against the hypothesis.
6. Compare results against the pre-registered decision rule. Do not keep searching until a favorable result appears.
7. End with evidence gained/not gained, tests performed, reproducibility status, continue/park/reject decision, and the single highest-value next action.

## Phase 0 — Repository and hypothesis audit
- Inventory files, branches, workflows, datasets, citations, prior prompts, and experiment artifacts.
- Confirm whether the repository is empty or populated; do not infer that an artifact exists because this prompt describes it.
- Recover the canonical ACCTCLOCK dossier and current validation handoff from the hypothesis factory using read-only access. Record commit SHA, retrieval date, and source paths.
- Classify claims as: (A) published mechanism evidence, (B) candidate-specific observational evidence, (C) actual strategy/backtest evidence, or (D) assumptions/conjectures.
- Reconcile the exact outcome: announcement-to-report drift, post-earnings-announcement drift, transition-window repricing, or a combination. These outcomes are not interchangeable. If ambiguous, stop and define competing hypotheses before looking at returns.

## Phase 1 — Literature and novelty audit
Search peer-reviewed work, working papers, regulator publications, and cited references. Record bibliographic details, DOI/URL, publication/version date, sample, identification design, dependent variable, estimates, limitations, and the exact claim supported.

Investigate:
- IFRS/GAAP adoption and reporting comparability;
- earnings-response coefficients, information content, and post-earnings-announcement drift;
- pre-announcement anticipation and early pricing;
- first-time versus repeat adopters and mandatory versus voluntary adoption;
- enforcement regimes, analyst following, pre-adoption reporting quality, and concurrent reforms;
- recent null, small, conditional, or reversed effects;
- whether the proposed signal is already published or merely relabels an established factor.

Do not infer investable returns from improved disclosure quality, reduced return synchronicity, liquidity changes, or valuation effects alone. These are different outcomes.

## Phase 2 — Freeze a precise, testable strategy
Before viewing outcome-period returns, specify:

1. Target event: exact standard, jurisdiction, legal/endorsement/adoption date, mandatory application date, first affected fiscal year, first full report date, and public timestamp for each.
2. Event clock: distinguish announcement, legal adoption, effective date, fiscal-year start, earnings announcement, and first comparative report. Use only information available at decision time.
3. Treatment and controls: pre-register first-time versus repeat adopters and/or low versus high pre-event information quality. Define proxy, measurement window, thresholds, and data vintage without future returns. Justify comparability and overlap.
4. Signal: define the exact rule mapping observable event-time information and firm state to long, short, or no position. If no economically justified sign exists, test a two-sided research hypothesis without selecting the favorable side after seeing results.
5. Universe: exchanges, share classes, security types, liquidity/price screens, delisted firms, foreign listings, reporting currencies, and point-in-time membership.
6. Entry and exit: exact timestamp and price convention, permissible delay after disclosure, maximum holding period, exit trigger, and handling of overlapping events.
7. Benchmark and estimand: abnormal-return/factor model, event window, primary outcome, and whether the target is a treatment effect, conditional drift, reversal, or portfolio net return.
8. Risk controls: market, industry, size, value, momentum, profitability, investment, liquidity, country, currency, and event-clustering exposures as appropriate.
9. Costs: commissions, spread, slippage, impact, turnover, taxes where relevant, borrow availability/fees for shorts, dividends, financing, FX, and delisting losses.
10. Acceptance and kill criteria: freeze before accessing the holdout.

Maintain one primary specification and clearly labeled secondary analyses. Never combine them into a post-hoc winner.

## Phase 3 — Data integrity and point-in-time controls
Use licensed, reproducible data. Document vendors, query/version, timestamps, timezone, corporate-action adjustments, identifiers, reporting-period conventions, missingness, restatements, delisted securities, and survivorship protections.

- Use only filings and variables publicly available by the decision timestamp.
- Distinguish fiscal period end from publication time and later restatements.
- Preserve delisted and failed firms; avoid survivorship and selection bias.
- Prevent duplicate firm-event observations and overlapping windows from inflating sample size.
- Account for dependence within firms, industries, jurisdictions, and shared adoption dates.
- Preserve an immutable raw-data/source manifest, data dictionary, hashes where feasible, and transformation scripts.
- Validate event dates against regulator/issuer primary sources. Record conflicts; never silently select the date producing the best return.
- Report coverage by event, country, year, treatment group, and liquidity bucket. Do not impute critical timestamps without justification.

If a complete point-in-time sample cannot be constructed, label the test exploratory and do not claim validation.

## Phase 4 — Statistical design and testing order
A. **Feasibility and event-count audit.** Enumerate independent adoption events and effective cross-sections. Firm count is not a substitute for independent event count when treatment is assigned at jurisdiction level. Assess power before modeling.

B. **Descriptive event study.** Plot pre/post abnormal returns, volume, spreads, and coverage. Inspect pre-trends and anticipation. This is descriptive, not causal proof.

C. **Primary identification test.** Use a justified matched-control, difference-in-differences/event-study, or other appropriate design. State assumptions; test pre-trends and use inference robust to event/jurisdiction clustering. A generic correlation is not causal evidence.

D. **Conditional hypothesis.** Test the pre-registered interaction with information quality and enforcement. Include competing conditioners and alternative explanations. Do not choose thresholds using the same outcomes used to evaluate the strategy.

E. **Portfolio simulation.** Only after estimating the primary effect, simulate the frozen rule with point-in-time holdings, realistic fills, costs, exposures, and capacity constraints.

F. **Out-of-sample test.** Use chronological development/validation/untouched holdout splits. If events are few, use leave-one-event/jurisdiction-out checks and explicitly note that these do not replace a truly independent sample. Never tune on the final holdout.

G. **Robustness and red-team checks.** Test pre-registered windows, placebo dates, unaffected standards/groups, false event assignments, alternative factor models, outlier sensitivity, subperiods, regimes, and exclusion of the largest winners. Report all planned tests and address multiple comparisons.

## Phase 5 — Mandatory failure and falsification checks
Downgrade, park, or reject as appropriate if:
- The effect is fully anticipated before the proposed entry timestamp.
- The information-quality interaction is absent, unstable, or opposite in sign.
- Results disappear after controlling for enforcement, size, liquidity, industry, momentum, or concurrent reforms.
- Placebo dates or untreated groups show similar effects.
- One jurisdiction, event, firm, or outlier explains the result.
- Independent sample size is too small for informative inference.
- Estimates are not robust to plausible windows or benchmarks.
- Gross returns are erased by spreads, impact, turnover, borrow, financing, or taxes.
- Data cannot support point-in-time replication.
- A threshold, sign, universe, or exit rule was selected after inspecting holdout returns.

Distinguish **rejected** (credible evidence contradicts the claim), **parked** (not currently testable due to missing data/identification), and **inconclusive** (test completed but uncertainty remains too large). A non-significant result is not automatically proof of zero effect.

## Phase 6 — Metrics and reporting
Report, as applicable:
- event count and independent event/jurisdiction count;
- treatment/control coverage, balance, missingness, and effective sample size;
- effect sizes with confidence intervals, p-values, and economic units;
- pre-trends, placebo results, and competing-conditioner comparisons;
- gross/net cumulative return, annualized return only where appropriate, volatility, Sharpe/Sortino, maximum drawdown, turnover, hit rate, average win/loss, tail loss, exposure/factor attribution, and capacity;
- cost sensitivity and break-even cost;
- return concentration by event, firm, country, and year;
- out-of-sample versus in-sample performance and number of variants tried;
- reproducibility status and unresolved limitations.

Do not promote on Sharpe or CAGR alone. Include uncertainty, sample limitations, benchmark-relative results, and the full event-outcome distribution. Do not present tiny event samples as stable annualized forecasts.

## Phase 7 — Promotion gates
Do not call the strategy validated unless all gates pass:
1. Hypothesis and primary outcome are precise and falsifiable.
2. Source/data lineage is reproducible and point-in-time correct.
3. Identification addresses anticipation, confounders, and event clustering.
4. Results survive pre-registered out-of-sample and placebo tests.
5. Economic effect remains positive after conservative realistic costs.
6. Tail risk, factor exposures, borrow, and capacity are acceptable.
7. An independent reviewer reproduces the main result from recorded artifacts.
8. A separate explicit authorization approves any later paper-trading or live-trading work.

Until then, status remains research-only. A successful historical study does not authorize live deployment.

## Required artifacts
Where authorized, maintain:
- research/hypothesis.md — immutable claim, mechanism, counter-hypotheses, predictions, kill conditions.
- research/specification_v1.md — frozen event definitions and trading rules.
- research/source_ledger.csv — sources, dates, claims supported, limitations, DOI/URL, verification.
- research/data_manifest.md — lineage, point-in-time fields, coverage, quality checks.
- research/preregistration.md — primary outcome, estimand, splits, tests, costs, thresholds frozen before returns are analyzed.
- research/experiment_ledger.csv — all runs including negative/failed experiments, code/config commit, data version, sample, outcome.
- research/results.md — uncertainty, costs, negative evidence, and no unsupported claims.
- research/red_team_review.md — independent falsification and reproduction.
- research/decision_log.md — continue/park/reject and reasons.
- research/prompt_changelog.md — dated iterations and rationale.

Do not create or modify these artifacts automatically if repository instructions or permissions prohibit it. This request authorizes the prompt file itself, not additional workflow runs or live activity.

## Final report format for every cycle
1. **Decision:** continue, narrow, park, reject, or (only after every gate) recommend a separately authorized next stage.
2. **What changed:** new evidence and exact source/artifact references.
3. **What was tested:** frozen hypotheses, sample, event count, scripts/configuration where applicable.
4. **Results:** effect sizes, uncertainty, costs, out-of-sample performance, and concentration.
5. **Red-team findings:** strongest alternative explanation and failure mode.
6. **Limitations:** missing data, power, event dependence, selection bias, and tool failures.
7. **Reproducibility:** commit, data/config hashes, independent rerun status.
8. **Next action:** one high-information test and its decision rule.
9. **Authority boundary:** confirm no unapproved repository changes, workflows, or trades.

## Operating principle
Optimize for reliable knowledge and the fastest honest rejection of weak ideas—not activity, a high score, a positive backtest, or a narrative that survives every objection. Keep the hypothesis fixed long enough to test it fairly; change it only through a new documented version. A null result is useful progress.
