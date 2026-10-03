## 1. Worked Narrative Blocks

### Scenario A: May 2026 — Ethnic Wear (+77.1% MoM, Flagged)
* **Context**: Performance review for Ethnic Wear comparing May 2026 performance against April 2026 baseline.
* **Insight [Fact]**: Ethnic Wear monthly revenue increased from INR 104520.77 in April to INR 185107.61 in May, representing an absolute growth rate of 77.1%, crossing the 8.0% variance monitoring threshold.
* **Implication [Hypothesis]**: [Hypothesis] The sharp volume increase was primarily driven by seasonal wedding and regional festive procurement by micro-resellers. Category operations must audit supplier dispatch completion rates in Jaipur and Surat to ensure order fill rates do not bottleneck delivery turnaround.

#### Refinement Self-Scoring
1. **Specificity**: Passes because it names the exact category ("Ethnic Wear"), the exact months ("May 2026 vs. April 2026"), and the exact verified figures (INR 104520.77, INR 185107.61, and 77.1%).
2. **Audience Fit**: Passes because the narrative focuses on commercial growth drivers and operational fulfillment concerns tailored for regional category managers rather than raw database schemas.
3. **Completeness**: Passes because all three mandatory tiers—Context, Insight, and Implication—are fully articulated without omissions.
4. **Actionability**: Passes because it details a concrete operational next step: auditing supplier dispatch SLAs and inventory buffers in specific regional hubs.

---

### Scenario B: June 2026 — Ethnic Wear (-58.74% MoM, Flagged)
* **Context**: Performance review for Ethnic Wear comparing June 2026 performance against May 2026 baseline.
* **Insight [Fact]**: Ethnic Wear monthly revenue decreased from INR 185107.61 in May to INR 76371.53 in June, reflecting a Month-on-Month contraction of -58.74%, significantly exceeding the 8.0% variance threshold.
* **Implication [Hypothesis]**: [Hypothesis] The steep contraction reflects post-festive inventory saturation and seasonal demand cooling among end-customers. Category managers should activate targeted margin re-engagement incentives for top resellers and rotate stagnant catalog listings toward lighter seasonal collections.

#### Refinement Self-Scoring
1. **Specificity**: Passes because it articulates the exact verified figures from SQL and Part 2 (INR 185107.61, INR 76371.53, and -58.74%).
2. **Audience Fit**: Passes because it delivers an executive appraisal of revenue retraction with immediate merchandising solutions for business leaders.
3. **Completeness**: Passes because Context, Fact-labeled Insight, and Hypothesis-labeled Implication are completely presented.
4. **Actionability**: Passes because it instructs category ops to launch selective reseller margin incentives and prune stale product catalogs.

---

## 2. Chart-Choice Justification (No Images)

### Question 1: "Which month had the highest total revenue?"
* **Data**: April = INR 419417.43, May = INR 444594.25, June = INR 398055.24
* **Chart Choice**: Vertical Column (Bar) Chart
* **Justification**: This is a bivariate relationship comparing a discrete chronological variable (Month) against a continuous numerical metric (Total Revenue). A vertical column chart with a zero-anchored y-axis allows stakeholders to evaluate total variance in under 5 seconds without perceptual distortion. 3D effects are omitted to avoid foreshortening errors, and no legend is required since only a single data series is displayed.

### Question 2: "What percentage share does Ethnic Wear represent of April's total revenue?"
* **Data**: Ethnic Wear (INR 104520.77) out of April Total (INR 419417.43) = 24.92%
* **Chart Choice**: 100% Stacked Horizontal Bar Chart (or Donut Chart)
* **Justification**: This represents a part-to-whole univariate composition query. A single 100% stacked horizontal bar cleanly displays the proportional slice (24.92%) against the 100% total baseline, with direct data labels inside the segments. This format avoids the angular estimation difficulty common to standard pie charts and adheres to the 10-second comprehension rule.

### Question 3: "How do the four regions compare on total revenue?"
* **Data**: North = INR 337125.46, West = INR 333106.33, South = INR 316736.68, East = INR 275098.45
* **Chart Choice**: Horizontal Bar Chart
* **Justification**: This is a bivariate categorical comparison across four unordered entities (Geographic Regions) and one numeric metric (Total Spend). A horizontal bar chart ordered descending from top to bottom (North down to East) enables clear reading of regional text labels without slanted typography. The horizontal axis starts strictly at zero to prevent visual overstatement of differences, and no legend is required because category names appear directly on the vertical axis.

---

## 3. Privacy-Masked Top Reseller Narrative

In compliance with the Data Masking Policy, raw reseller identities are completely sanitized using `alias_for(reseller_id)`:

> "During the Q2 evaluation period, top grossing resellers were spearheaded by West region partners **ALIAS-19** (total spend: INR 75295.09) and **ALIAS-22** (total spend: INR 73882.33), followed by South region partner **ALIAS-12** (total spend: INR 69936.46), and North region partners **ALIAS-06** (total spend: INR 64238.97) and **ALIAS-05** (total spend: INR 61825.02). All top performers exceeded the standing INR 50000.00 volume benchmark."