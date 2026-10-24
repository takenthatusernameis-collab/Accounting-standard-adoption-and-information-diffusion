# ACCTCLOCK — Iteratively Improving Research and Validation Prompt
Version: 1.3
Prepared: 2026-10-24
Status: Research guidance v1.3 — adaptive feasibility tiers; D-032 free-only route; hypothesis not validated; research-only.

## Mission
Independently test ACCTCLOCK: accounting-standard adoption can change information, comparability, and the speed investors incorporate reported information, potentially producing conditional, time-limited equity-return drift. Determine whether a precisely specified, implementable rule has reproducible positive expected net returns after realistic costs. Do not try to confirm the story or maximize a backtest; reject it quickly if evidence fails.

This file is a prompt and protocol, not evidence that a test has run or an edge exists.

## Authority, scope, and safety
1. Work only in this strategy-specific repository unless the user explicitly authorizes another repository.
2. Do not place, route, or imply live trades; do not connect to brokerage accounts or create live deployment workflows.
3. Do not edit upstream hypothesis-factory repositories, unrelated projects, or live trading systems.
4. Follow D-032 below. Use only genuinely free, legally accessible public sources and no-cost software. Do not use paid vendors, paid API tiers, subscriptions, free trials that convert to paid plans, or services requiring payment details. Do not ask the user to purchase or provision paid access. Public-source collection is authorized subject to source terms and rate limits. Do not trigger GitHub Actions or live/paper-trading workflows.
5. Preserve an immutable record of the original hypothesis and each version. Never silently change the thesis, universe, sample, entry time, holding period, filters, costs, or acceptance criteria to rescue a failing result.
6. If essential data or permission is unavailable, keep the affected confirmatory test blocked and report the blocker. Do not stop the entire research program: apply the adaptive research-gate policy below and complete a permitted feasibility, measurement or separately versioned exploratory task. Never claim completion based on a plan alone.



## Current operating directive — D-032 (2026-10-22; supersedes D-031 paid-provider direction and earlier A1–A5 waiting)

The maintainer explicitly directs the campaign away from all paid services. This decision supersedes D-031 wherever it proposes paid market-data providers. Do not ask the user to revisit A1–A5 or ask them to buy/provision vendor access. Execute all permitted free-source work immediately, in parallel where independent.

- **Zero-spend rule:** no paid data vendors, subscriptions, trials requiring payment details, paid APIs, paid research platforms, paid cloud services, or purchases. Do not trigger a paid endpoint or make a request that could incur a charge. No account creation or payment-method entry to unlock a trial. Do not bypass access controls, rate limits, or terms of service.
- **Public filings and event evidence:** use SEC EDGAR and issuer filings; IFRS Foundation and standard-setter publications; EUR-Lex; FCA/UK National Storage Mechanism and issuer/regulatory filing portals; national Officially Appointed Mechanisms (OAMs); official exchange and company announcements; World Bank WGI and other openly published government/institutional datasets. Follow published terms, rate limits, and access rules. Cache source material outside the repository when redistribution terms are unclear; commit provenance, hashes, and legally redistributable derived artifacts.
- **Free price-data discovery:** first inventory openly downloadable exchange/regulator datasets, official historical files, and public datasets with explicit redistribution terms. Then assess free public endpoints or downloadable archives (for example Stooq or Yahoo Finance only where their access terms permit the intended use) as candidate sources, not guaranteed complete sources. Do not assume they retain delisted securities, point-in-time identifiers, corporate actions, or terminal/delisting returns. No source is accepted until coverage is measured and documented by event, jurisdiction, security status, and date.
- **Existing code:** scripts/price_provider_client.py and tests/test_price_provider_client.py were built for a now-superseded paid route. Do not invoke their paid-provider paths. Either leave them inert and clearly mark them superseded, or refactor only if needed to support a documented free source; never pass credentials or call a paid endpoint. Offline tests must be run in an actual repository environment before claiming they pass.
- **Coverage honesty:** daily adjusted close is not a substitute for a delisting return. Preserve inactive/delisted names where the free source supports them. Do not drop firms, impute zero terminal returns, or claim CRSP-grade coverage without evidence. If no lawful free source can meet a required field, record a quantified coverage gap and stop the affected return analysis.
- **Research gates:** publish event counts, treatment-firm counts, source coverage, missingness, and point-in-time feasibility before opening outcome-period returns. Frozen thresholds of at least 12 independent clusters and 200 treatment firms remain binding. Do not count firms as independent events, count EU member states as independent cohorts where treatment is shared, lower thresholds, or inspect PH-1 outcomes before the once-only feasibility gate. The currently expected PH-1 event count is below threshold; if confirmed, report **inconclusive-by-construction** and do not run or tune the outcome test.
- **No-go boundaries:** no live/paper trading, brokerage connection, deployment, costly background run, paid request, or GitHub Actions workflow run. Do not modify frozen hypotheses, specifications, preregistrations, sample rules, thresholds, or outcomes in place.

The next step is to run a free-source inventory and data-feasibility audit, execute existing offline tests if the repository environment is available, reconcile current panel counts from committed builders, and provide a source-backed handoff. Network/DNS failures are environment limitations, not provider failures or evidence for/against the hypothesis.

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

Do not create or modify these artifacts automatically if repository instructions or permissions prohibit it. The original prompt-file request authorized the prompt file only. D-031 additionally authorizes read-only public-source collection and a pre-outcome feasibility audit; it still does not authorize paid purchases or unspecified charges, GitHub Actions runs, trading or live activity.

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




## Adaptive research-gate policy v1 — default for future work

**Purpose:** prevent repeated feasibility deadlocks without turning weaker evidence into a stronger claim. This policy changes the default way the agent makes progress; it does not rewrite frozen experiments.

### 1. Keep two tracks separate
- **Confirmatory track:** preserve the currently registered hypothesis, sample minimums, history minimums, universe definition, parameter grid, costs, holdout boundaries and acceptance criteria. Never change them in place or retroactively reclassify old evidence.
- **Exploratory track:** when the trigger below is met, automatically create a new uniquely identified version with the smallest feasible change. It may answer a narrower or lower-powered question, but its status must be `EXPLORATORY_ONLY` or `INCONCLUSIVE`; it cannot validate, replace or unlock the frozen confirmatory track.

### 2. Trigger for adaptive relaxation
Start the exploratory track after either (a) three materially distinct, documented attempts spanning at least two independent source families or methodological routes fail to advance the same feasibility gate, or (b) a durable structural impossibility is evidenced by source coverage, terms, schema or sample counts. A repeat of the same failed endpoint is not a distinct attempt. Record route, date, observed response/coverage, exact unmet requirement and why retries are unlikely to help. Do not keep looping on a known failure.

### 3. Relax the least damaging feasibility constraint first
Consider, one at a time: use a smaller *explicitly defined* eligible population; use the verified historical overlap rather than demanding a market-cap rank that is not essential to the mechanism; shorten history for a clearly labeled pilot; reduce grid breadth by testing a frozen anchor first; or run a descriptive/measurement feasibility study before estimating outcomes. Choose based on the estimand and data-generating process, not on which choice improves returns. If more than one dimension changes, state and justify each change in a new version before calculating its outcomes.

### 4. Hard safeguards are never relaxed
No look-ahead, fabricated or forward-filled observations, invented fills, silent sample exclusions, outcome-informed parameters/costs, hidden multiple-testing, reuse of an inspected holdout as fresh confirmation, misleading performance labels, breach of source terms, paid services or compute where prohibited, or live/paper trading. Synthetic fixtures are software tests, never market evidence. A current market-cap snapshot must never be labeled historical point-in-time truth. Do not open an originally sealed holdout to rescue progress; any relaxed study needs a new ID, explicit estimand and correctly labeled data vintage.

### 5. Reporting and promotion
Report all attempted routes and failures, coverage/missingness, sample and independent-cluster counts, changed assumptions, uncertainty, all tried variants, costs and reasons for exclusions. Report effect sizes descriptively if calculable, but do not describe underpowered inference as confirmation. A green workflow or passing tests proves only what the tests cover. Promotion requires the original confirmatory gates on admissible data, a sealed evaluation, complete multiple-testing correction and independent recomputation. If the alternative remains infeasible, say so and move to another independent task.

**Default execution rule:** once the trigger is met, do not merely write another blocker memo. Within the repository's existing authorization, complete the next bounded, no-cost exploratory task and preserve the original blocked status. Do not obtain new permissions, spend money, trigger prohibited workflows, or alter frozen result artifacts to make this possible.


### ACCTCLOCK-specific constraints
- The timing-cohort minimum, 200-treatment-firm minimum, price/delisting-return requirement, original event clocks and registered PH-1 outcome protection remain frozen for the confirmatory arm. This policy does not authorize opening PH-1 when its gate fails, computing its outcome returns early, reducing its minimums in place, or relabeling an underpowered result as confirmation.
- The currently documented state has 12 verified timing cohorts, zero admitted treatment firms against >=200, and no verified free delisted/terminal-return coverage. This qualifies for an adaptive **return-free** feasibility track now: continue permitted primary-source harvesting, coverage/count audits, power calculations based on pre-outcome inputs, identity-linkage validation and freely available source discovery; report the precise admission/coverage gap. Do not use paid sources, provision credentials, trigger paid requests, or ask for purchase; D-032 remains binding.
- If a distinct, defensible exploratory estimand can be registered without opening or reusing the protected PH-1 outcomes, create a new version and state the smaller population and reduced inferential scope. Otherwise, maintain PARKED/INCONCLUSIVE and use source-independent validation or hypothesis-design work. The fact that a threshold is difficult to meet is not, by itself, evidence that the scientific threshold is wrong.

**Prompt changelog note:** v1.3 adds a tiered feasibility policy only. It does not amend `research/hypothesis_v1.3.md`, registered `research/preregistration_v1.1.md`–`v1.4.md`, or any historic result. Any future experiment or estimand change requires its own preregistration and immutable artifacts.
