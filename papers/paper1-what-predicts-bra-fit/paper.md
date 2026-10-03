# What Predicts Bra Fit and Why It's Not What You Think

## Introduction

Incorrect bra sizing is a widespread, well-documented problem. Coltman, Steele, and McGhee (2018) showed in a sample of 309 women that about 90% fail professional fit criteria, with the cup, front band, and straps fitting worst. A more recent study, Haworth et al. (2025, n=24, Int. J. Fashion Design, Technology and Education, DOI 10.1080/17543266.2025.2461460), gives an even starker result: by the same professional criteria, not a single participant passed. Despite this, the overwhelming majority of existing sizing methods — from retail staff to brands' own online calculators — still come down to the same scheme: measure the underbust, measure the bust, take the difference, and convert it into a cup letter. Whether this method, despite being a near-universal industry standard, actually relates to real-world fit across a large population has never been empirically tested.

The reason lies in a structural gap between two types of existing data. Small controlled studies such as Coltman et al. (2018) and Haworth et al. (2025) provide reliable measurements but are limited in scale (n=309 and n=24, respectively). Large crowdsourced datasets, by contrast, are large in volume but measure the wrong thing: the ModCloth and RentTheRunway datasets (Kaggle Fit Feedback, 192,544 and 82,790 records) record the fit of rented or purchased clothing — dresses, jumpsuits, tops — not bras, and the stated bra size there serves only as a body characteristic of the buyer, not a report of garment fit. None of the sources known to me combines raw garment measurements with a genuinely, independently reported fit outcome on the same SKU at a scale sufficient for stable statistics.

This work aims to empirically test, on a large secondary crowdsourced dataset (Bratabase), which measurable bra parameters are actually associated with real-world fit. Chief among these: whether underbust circumference — the input underlying nearly every existing sizing method — statistically predicts fit at all. To this end, the following tasks were addressed:

1. Collect and clean a dataset of garment measurements, reviews, and fit labels, ensuring comparability through matching by brand, model, and size, with control for brand effects.
2. Test the reproducibility of an already-known result (Coltman et al., 2018) using a different method and a different population.
3. Assess the relationship between underbust circumference and fit, before and after controlling for brand.
4. Assess the relationship between garment cup parameters (depth, width, height, wire length) and fit.
5. Examine secondary construction parameters (gore height, wing height, bra type, number of hooks) for nonlinear or unexpected effects.
6. State what the results mean for the near-universal two-measurement sizing method.

The object of the study is bra fit as a measurable phenomenon; the subject is the relationship between garment measurements and self-reported fit outcome across a crowdsourced dataset. Methodologically, the work relies on secondary data analysis with brand-fixed-effect control (de-meaning), comparison of proportions across groups, and a text analysis of self-described body shape as a cross-check on one of the findings.

The scientific novelty of this work is that, to the best of my knowledge, this is the first time raw garment measurements have been matched against genuinely independent fit labels at a scale two orders of magnitude larger than the nearest comparable study (36,550 matched pairs versus n=309 for Coltman et al.). On this dataset, the absence of a monotonic relationship between underbust circumference and real-world fit is demonstrated empirically for the first time — a result that directly contradicts the premise underlying nearly the entire existing industrial approach to sizing.

## Data and Method

The data source is bratabase.com, an open crowdsourced database of bra measurements and reviews. Collection was carried out manually by one person between September 18 and 21, 2026, without automation. This work does not publish the raw dataset itself, only derived figures, tables, and analysis code. Readers wishing to replicate the collection can go to the original sources (bratabase.com, and for comparison, Kaggle Fit Feedback, the ModCloth and RentTheRunway datasets).

Four linked datasets were extracted.

`measurements.csv` contains 496,969 rows, one for every theoretically possible size within every brand's size range, regardless of whether anyone ever entered real figures for it. Of these, only 82,126 rows (16.5%) are actually usable for analysis: 29,055 rows with measurements and a stated number of owner-respondents (crowd-verified, the gold standard for this work), plus a further 53,071 rows with real figures but no owner count (apparently reference data from the brand itself; the exact source was not verified). The remaining rows are either an empty size card with no figures at all, or a note that owners exist with no measurements entered.

`reviews.csv` contains 52,757 reviews, all genuine. The fit field (`fit_status`) takes the values Fits, Didn't fit (with a too big/too small qualifier), and Hasn't set fit. The last category (4,492 reviews, 8.5%) carries no fit signal and was excluded from all fit comparisons.

`joined.csv` is the result of matching by brand, model, and size — 36,550 pairs of "garment measurement plus fit outcome."

`models.csv` contains 23,188 rows, one per model (brand and model slug). It includes the brand, model name, whether the model is discontinued, whether it has an underwire, and its bra type (Regular, Sports, Strapless, Swimwear, Longline/Corset, Soft cup/No underwire). It is used only to attach a bra type to each review for Table 6; no other field from this file is used in the analysis.

The main control method is brand de-meaning: each measurement has its own brand's mean subtracted, so that differences in fit standards between manufacturers are not conflated with the overall effect of the measured parameter. A minimum threshold of 30 reviews per brand was set for a stable mean; the final slice used for fit comparisons is 34,505 reviews (Fits/Didn't fit, after excluding Hasn't set fit and brands below the threshold).

One field was deliberately excluded from the analysis: `bust_perimeter_cm` produced physically impossible median values (17–30 cm as a bust circumference). Checking the Bratabase site itself showed that this field appears neither in the advanced measurement-search form nor in the per-size aggregation table — meaning the field's unreliability is acknowledged by the source itself, not only by this check. The field is not used anywhere in the results below.

## Results

All proportions below are the percentage of Fits reviews within a quintile of the corresponding measurement, after subtracting the brand mean (de-meaning). The slice is Fits/Didn't fit, n=34,505.

**Table 1. Fit% by quintile of cup measurements, after brand de-meaning**

| Measurement | Q1 | Q2 | Q3 | Q4 | Q5 | Brands in slice |
|---|---:|---:|---:|---:|---:|---:|
| Cup depth | 37.4% | 37.8% | 36.3% | 36.3% | 34.6% | 67 |
| Cup width | 36.3% | 40.2% | 36.2% | 34.4% | 35.1% | 67 |
| Wire length | 36.7% | 39.1% | 37.3% | 34.9% | 33.9% | 65 |
| Cup height | 37.2% | 38.1% | 36.2% | 36.3% | 34.9% | 55 |

All four cup measurements show declining Fit% from Q1 to Q5; the effect survives brand control. The direction agrees with Coltman et al. (2018, n=309) and Kaggle Fit Feedback (n=275,334) — a third, independent population and method yielding the same result.

**Table 2. Fit% by quintile of band measurements, after brand de-meaning**

| Measurement | Q1 | Q2 | Q3 | Q4 | Q5 | Brands |
|---|---:|---:|---:|---:|---:|---:|
| Underbust circumference | 37.5% | 37.6% | 36.2% | 37.1% | 36.9% | 75 |
| Stretched band | 35.6% | 37.5% | 36.4% | 36.7% | 35.6% | 68 |
| Band length | 35.3% | 37.3% | 36.7% | 36.6% | 36.8% | 68 |

None of the three ways of measuring the garment's band shows a monotonic relationship with fit. This agrees with Kaggle (band sizes 32–38, 95% of the sample: 72–74% flat across the whole scale, with no clear trend).

**Table 3. Fit% by quintile of construction geometry, after brand de-meaning**

| Measurement | Q1 | Q2 | Q3 | Q4 | Q5 | Brands | Shape |
|---|---:|---:|---:|---:|---:|---:|---|
| Gore height | 36.4% | 38.0% | 38.1% | 34.7% | 34.6% | 68 | peak in the middle |
| Wing height | 36.5% | 37.7% | 37.8% | 34.8% | 35.0% | 68 | peak in the middle |
| Cup spread | 38.3% | 37.2% | 36.0% | 35.4% | 35.2% | 67 | monotonically down |
| Strap width | 38.0% | 37.7% | 35.2% | 35.3% | 35.9% | 67 | weak, noisy |

Gore height and wing height show a nonmonotonic effect (best fit in the middle of the scale, worse at both ends). Cup spread shows a clean monotonic effect, but only after de-meaning: without brand control the raw pattern was U-shaped (44.4% → 38.1% → 32.7% → 31.9% → 37.9%) and would have been misleading.

**Table 4. Fit% by number of hooks (direct grouping, not quintiles)**

| Hooks | n | Fit% |
|---|---:|---:|
| 1 | 829 | 43.4% |
| 2 | 21,182 | 37.3% |
| 3 | 9,318 | 37.6% |
| 4 | 685 | 33.1% |
| 5 | 258 | 45.0% |
| 6 | 403 | 33.0% |

The two dominant options (2 and 3 hooks, 91% of the sample) do not differ in Fit%. The tails are too small to draw a conclusion.

**Table 5. Garment cup spread × self-described body shape in review text**

| Self-description | n | Garment spread narrower than typical | Garment spread wider than typical | Difference |
|---|---:|---:|---:|---:|
| "wide-set" | 1,467 | 39.7% | 37.3% | −2.4 pp |
| "narrow-set" | 1,571 | 38.9% | 33.5% | −5.4 pp |

The columns describe the spread of the garment's own cups (an objective measurement of the model, narrower or wider than typical for the brand). The rows are what the woman wrote about her own body in the review. If garment spread simply matched the body, a wide-set woman should find a wide garment fitting no worse, and probably better, than a narrow one. That is not what happens: in both groups (wide-set and narrow-set alike) the wide garment fits worse than the narrow one.

This means a wide spread is, in part, an independent flaw of the construction itself, not merely a mismatch with a particular body. For narrow-set women the gap is almost twice as large (−5.4 pp versus −2.4 pp), because two factors act on them at once — the garment's own flaw plus an additional mismatch with their body — whereas for wide-set women the second factor partly offsets the first.

**Table 6. Fit% by bra type**

| Bra type | n | Fit% |
|---|---:|---:|
| Regular bra (underwired) | 30,787 | 37.9% |
| Sports bra | 1,164 | 42.0% |
| Longline/Corset | 850 | 39.1% |
| Strapless bra | 640 | 28.4% |
| Swimwear | 542 | 50.4% |
| Soft cup/No underwire | 447 | 50.3% |

Bras without an underwire or rigid structure fit noticeably better; strapless fits worst of all. This is both an external sanity check on the data (the pattern is exactly what one would expect) and an important caveat for Tables 1–5: 89% of the slice (30,787 of 34,505) is Regular bra, so the findings above are effectively about underwired bras, not lingerie in general.

## Additional Exploratory Finding: Mentions of Pain and Migraine in Review Text

Motivation — a study by neurologists (Pocock et al., 2026, *Headache: The Journal of Head and Face Pain*, DOI 10.1111/head.70226, n=687) linked a clinical diagnosis of macromastia to an elevated, adjusted prevalence of chronic migraine (aPR=1.40, 95% CI 1.16–1.68) and neck pain (aPR=2.04, 95% CI 1.65–2.53), as well as cervical radiculopathy and obstructive sleep apnea. The design is retrospective, the sample is limited to patients at a neurology clinic, and no causal mechanism is established — the study itself acknowledges this.

Out of curiosity, the same 52,757 Bratabase reviews were checked for mentions of symptoms ("neck pain," "migraine," "headache," "shoulder pain," "back pain," and variants) in the free-text review. 146 matches were found (0.3%), of which 8 were "migraine."

**Table 7. Share of reviews mentioning pain/migraine, by cup size group**

| Group | Total reviews | Mentions | Share |
|---|---:|---:|---:|
| small (AA–D) | 7,022 | 9 | 0.128% |
| medium (DD–G) | 29,489 | 57 | 0.193% |
| large (GG+) | 15,223 | 76 | 0.499% |

The share of mentions rises almost fourfold from small to large cups. This cannot be read as either confirming or refuting the clinical study: the absence of a mention in a bra review does not mean the absence of a symptom (0.3% is a lower bound with substantial underreporting, not a prevalence estimate); band size was not controlled for, and cup letter alone is a weak signal without it; the Bratabase sample is self-selected (lingerie enthusiasts, not clinic patients) and not medical. This finding is presented as an exploratory observation on the same dataset, not as a test of the clinical study.

## Additional Exploratory Finding: Direction of Band Adjustment Relative to the Label

Motivation — a rule of thumb common in the lingerie community holds that the band on the label is usually smaller than the raw underbust measurement by "two or three steps" (10–15 cm, i.e., two or three steps of the 5 cm size grid under GOST 29097-2015). The rule implies a systematic shift in one direction: label smaller than measurement.

To check the direction (not the cause), the same 52,757 Bratabase reviews were checked for phrases about band fit relative to expectation.

**Table 8. Frequency of band-fit phrases in review text**

| Phrase | n | Share |
|---|---:|---:|
| "band runs small" (tight for its size) | 279 | 0.529% |
| "band runs large" (loose for its size) | 119 | 0.226% |
| "sized down band" (went to a smaller band) | 569 | 1.079% |
| "sized up band" (went to a larger band) | 691 | 1.310% |

"Runs small" occurs almost twice as often as "runs large," and "sized up" is even slightly more common than "sized down" — there is no consistent one-way shift toward "label always smaller than measurement" in this dataset. Caveat: these phrases describe a choice between labeled sizes while trying on a single model, not the pair "raw tape measurement → final chosen label" referenced by the rule itself — a related but not identical question. Even so, the direction agrees with the finding in Table 2: there is no predictable one-way shift in band circumference in this data.

## Additional Exploratory Finding: Wire Poking Through, Wire Length, and Cup Depth

Motivation — a common observation in the lingerie industry: the underwire often breaks through the channel fabric specifically at its end, not in the middle. A plausible mechanism is a concentration of cyclic load at the transition between a rigid element (the wire) and an elastic shell (the channel fabric): with each compression cycle, the material at the end of the rigid element experiences more local deformation than the material in the middle of the channel. Direct measurements of this effect do not appear to exist in the open literature.

Method — `joined.csv` (garment measurement and review in one row, 34,818 rows with a known wire length after excluding wireless models) was checked for phrases about the wire poking through or breaking through ("wire poking," "wire popped," "wire coming through," "wire broke," and variants). 106 mentions were found.

**Table 9. Share of complaints about a poking wire, by wire-length quintile**

| Quintile | Wire length | n | Complaints | Share |
|---|---|---:|---:|---:|
| Q1 | 11.4–22.2 cm | 6,963 | 9 | 0.129% |
| Q2 | 22.2–24.5 cm | 6,963 | 24 | 0.345% |
| Q3 | 24.5–27.0 cm | 6,963 | 16 | 0.230% |
| Q4 | 27.0–30.7 cm | 6,963 | 16 | 0.230% |
| Q5 | 30.7–50.8 cm | 6,966 | 41 | 0.589% |

The share of complaints rises from the shortest wire to the longest by almost 4.6 times. The increase is not perfectly monotonic (Q2 is higher than Q3–Q4), but the edge-to-edge direction is consistent and agrees with the plausible mechanism: more length — more leverage — more accumulated displacement at the end of the channel.

Wire length is geometrically determined by cup depth (the wire traces the underside of the cup), so before attributing the effect specifically to length, the relationship between the two was checked: correlation r=0.921 on the same 34,818 rows — this is the same signal, not two independent measurements.

**Table 10. Share of complaints about a poking wire, by cup-depth quintile (control check)**

| Quintile | Cup depth | n | Complaints | Share |
|---|---|---:|---:|---:|
| Q1 | 12.1–20.7 cm | 6,961 | 18 | 0.259% |
| Q2 | 20.7–23.2 cm | 6,961 | 16 | 0.230% |
| Q3 | 23.2–25.7 cm | 6,961 | 16 | 0.230% |
| Q4 | 25.7–29.0 cm | 6,961 | 19 | 0.273% |
| Q5 | 29.0–57.2 cm | 6,963 | 37 | 0.531% |

The spread by cup depth is similar in shape to Table 9 (rising toward the top quintile), but about half as wide in magnitude (2.1× versus 4.6×). If wire length were a pure substitute for cup depth with no contribution of its own, the two spreads should have nearly coincided. The difference hints at a possible independent contribution from wire length beyond overall cup size, but with 16–41 complaints per bucket this cannot be reliably distinguished from noise.

A separate caveat, important for practical interpretation: the 4.6-fold increase is a relative figure. In absolute terms, the difference between the shortest and longest wire is 0.46 percentage points (0.129% versus 0.589%) — roughly 4–5 extra complaints about a poking wire per 1,000 reviews of long-wire models compared with short-wire ones. A "several-fold" increase and an increase of "a few cases per thousand" differ in practical significance — the same distinction between relative and absolute risk already applied above to the migraine study (section "Additional Exploratory Finding: Mentions of Pain and Migraine"). I take a large relative difference combined with a small absolute frequency to mean that the problem is real and directionally reproducible, but does not necessarily call for immediate intervention.

## Findings

The main result: underbust circumference, the basis of nearly every existing sizing method, shows no monotonic relationship with real-world fit in any of three ways of measuring it (Table 2). Meanwhile, the garment's cup parameters (Table 1) reliably predict fit, and the effect survives brand control. This directly contradicts the logic of the two-measurement method: if the difference between the two circumferences truly determined the right size, underbust circumference should at least not behave more erratically than the cup parameters.

Independent confirmation from a different angle comes from Sohn and Kim (2026, n=2,750, five ethnic groups): the same method, the difference between bust and underbust circumference, yields a statistically different real volume depending on ethnicity (p<0.001). In other words, the same computed result (a "C cup," say) corresponds to a different body in different population groups. Our result and Sohn and Kim's look at the problem from different sides: in ours, the method fails to predict the fit outcome; in theirs, the calculation itself fails to reproduce the same physical quantity. Both point to the same structural defect in the method, not to random noise in a single sample.

A similar picture emerges in Jolkovsky et al. (2025, n=395, actual weight of excised breast tissue): in a multivariate model, cup letter on its own ceases to be a significant predictor of breast weight; only sister size (the combination of band and cup) and BMI remain significant. This agrees with the finding in Tables 1–2: it is not any single cup or band measurement on its own that matters, but their combination, which represents volume. Separately, Oon et al. (2022) show that among bra characteristics, volume — not cup letter or band size on its own — is the single variable associated with all six satisfaction items.

The discrepancy is not confined to a single pair of brands: the same 2 cm quantum found for Triumph is independently confirmed for Wolford and matches both the EN 13402-3 norm and Milavitsa's own formula, whereas Intimissimi gives 5–5.5 cm in every comparison. The methodology for extracting and verifying these brand formulas from official sources is described in detail in the companion paper, *"A Quantum of Unmercy: Why Bra Sizing Cannot Be Transferred Between Brands."* A plausible explanation for why different brands choose a different step size at all lies in SKU economics: a finer cup quantum geometrically increases the number of stock variants for each line, and, other things equal, a manufacturer trades off fit precision against assortment cost. This explanation has not been directly tested (for example, against brands' internal data), so it is offered as a plausible, not a proven, mechanism.

The nonmonotonic effect of gore height and wing height (Table 3) is a separate finding, not reducible to "two measurements are not enough." Fit is best not at the extremes but at values typical for the brand, meaning extreme choices (a very low or very high gore) are themselves worse regardless of how well they match the body. This is a design conclusion, not a sizing one: it speaks to how a bra should be cut, not to what size a customer should be offered.

The results by bra type (Table 6) serve both as an external check on data adequacy (the pattern is the expected one: bras without an underwire or rigid structure fit noticeably better) and as an important caveat on the rest of the results: 89% of the slice is underwired bras, so the findings in Tables 1–5 cannot, without further checking, be extended to lingerie without a rigid structure.

Taken together, the results of this paper call into question not the accuracy of any particular brand's calculator, but the very premise on which nearly all of them are built: that two circumferences suffice to predict fit. This is not a hypothesis or an opinion — it is, to my knowledge, the first test of this premise on a dataset of this scale, and the premise did not survive it. What to use instead of the two-measurement method is a separate methodological question, addressed in the companion paper, *"A Quantum of Unmercy: Why Bra Sizing Cannot Be Transferred Between Brands."*

## Limitations

**A self-selected, non-medical sample.** Bratabase users are people voluntarily interested in precise bra fitting who leave detailed reviews. This is not a random sample of the general population; women with a difficult sizing experience may be either overrepresented (more motivation to leave a review after a difficult experience) or underrepresented (difficulty may discourage engaging with the topic at all). The direction of this bias was not assessed.

**The fit label is self-report, not a professional assessment.** `fit_status` (Fits/Didn't fit) is what a person wrote about her own experience, not a fitter's conclusion by objective criteria, as in Coltman et al. (2018) or Haworth et al. (2025). Self-reported fit is subject to at least three effects: inaccuracy of self-measuring one's body and the garment; a tendency not to notice objective fit problems without an external reference point; and reluctance to admit that an already purchased and paid-for bra does not, in fact, fit. Direct quantitative confirmation comes from Haworth et al. (2025, n=24): participants' subjective fit reports agreed with a professional fitter's objective assessment in only 51% of cases. This is a different sample and a different method, not a measurement on the Bratabase data itself, but it gives a concrete figure for the gap between self-report and objective fit assessment, rather than a merely plausible argument with no number behind it. This is why the Fit% shares in Tables 1–7 are better read as a lower bound on the severity of the problem than as a precise estimate.

**No body data: age, BMI, ethnicity.** Bratabase stores only garment measurements, not body measurements. Shi et al. (2020, n=137, *Ergonomics*) show that with excess weight, breast volume increases two- to threefold compared with a normal BMI in the nominally same class. If BMI distribution differs across brands or size groups, part of the results may reflect not the measurement itself but a hidden link to body composition that brand de-meaning does not remove. A partial remedy could be a rough body-type classification (e.g., slim/average/fuller) from photos attached to some reviews on the site — a subjective method, but probably accurate enough for three or four categories. Photos were deliberately not collected as part of this data gathering, owing to the substantial increase in archive size; the collection is reproducible if needed.

**De-meaning controls for the average brand effect, not within-brand variation.** Subtracting the brand mean removes the difference "this brand fits worse on average," but not the difference between individual models of the same brand, which can be substantial (partly, but not fully, addressed by the breakdown by bra type in Table 6).

**The dataset is not published.** This work shares derived figures and analysis code, not raw data. This limits direct reproducibility: a reader can assemble a comparable dataset from the cited original sources, but cannot verify these exact rows one for one.

**Correlation, not causation.** It cannot be established from this data that, say, greater cup depth by itself worsens fit rather than correlating with something else. But the direction of the effect converged across three independent sources at once — Coltman et al. (2018), Kaggle Fit Feedback, and this work — and such convergence across different populations and methods is rare in this field and is, on its own, weighty enough for practical decisions, even without a formal causal inference.

## Conclusion

1. Underbust circumference, which underlies nearly every existing bra-sizing method, shows no measurable relationship with real-world fit across a dataset of 34,505 reviews. This is, to my knowledge, the first test of this method at this scale.
2. Garment cup parameters (depth, width, height, wire length) predict fit; the effect is robust to brand control, and the direction is confirmed across three independent populations (Coltman 2018, Kaggle Fit Feedback, this work).
3. Some construction parameters (gore, wing) behave nonmonotonically: fit is best not at the minimum or maximum of the parameter but at a value typical for the brand. This is a conclusion for product design, not for fitting a particular body.
4. Bra construction type (presence of an underwire, rigidity) is an independent and substantial factor in fit, comparable to or exceeding the importance of size.
5. The industry standard that "two circumferences are enough" is not supported either statistically (this work) or at the level of consistency of the method across brands (direct comparison of the official size charts of Triumph, Wolford, and Intimissimi, with a discrepancy of up to 8 cm at the same band size). What to use instead is the subject of the companion paper, *"A Quantum of Unmercy: Why Bra Sizing Cannot Be Transferred Between Brands."*

## Data and Code

This work does not publish the raw dataset (rationale in "Data and Method"). The aggregation and statistical analysis code used to produce Tables 1–10 (excl. Table 5) is published. For independently assembling comparable data:
- bratabase.com — an open database of bra measurements and reviews (manual collection, no automation);
- Kaggle Fit Feedback (the ModCloth and RentTheRunway datasets) — for comparison, see Introduction.

## References

1. Coltman, C.E., Steele, J.R., McGhee, D.E. (2018). Which Bra Components Contribute to Incorrect Bra Fit in Women Across a Range of Breast Sizes? *Clothing and Textiles Research Journal*, 36(2), 78–90. https://doi.org/10.1177/0887302X17743814
2. Haworth, L., Sinclair, J., May, K., Janssen, J., Selfe, J., Chohan, A. (2025). Highlighting the need for change through an analysis of bra fit quality. *International Journal of Fashion Design, Technology and Education*, 19(2), 205–214. https://doi.org/10.1080/17543266.2025.2461460
3. Jolkovsky, E., Miller, M.N., Barkhordarzadeh, A.D., Piva, S., Alnaseri, T., Slack, G.C. (2025). Improving Documentation in Plastic Surgery: Sister Bra Size Group and BMI Are More Indicative of Breast Weight Than Cup Size. *Aesthetic Surgery Journal*, 45(10), 1017–1025. https://doi.org/10.1093/asj/sjaf114
4. Oon, I.H., Mara, J.K., Steele, J.R., McGhee, D.E., Lewis, V., Coltman, C.E. (2022). Women with larger breasts are less satisfied with their breasts: Implications for quality of life and physical activity participation. *Women's Health*, 18. https://doi.org/10.1177/17455057221109394
5. Pocock, K.S., Rigdon, J., Smirnoff, L., Mills, C., David, L.R., Wells, R.E., Lipton, R.B., Moskatel, L.S. (2026). Patterns of head and neck pain and obstructive sleep apnea in women with macromastia: A cross-sectional analysis. *Headache: The Journal of Head and Face Pain* (early access). https://doi.org/10.1111/head.70226
6. Shi, Y., Shen, H., Taylor, L.W., Cheung, V. (2020). The impact of age and body mass index on a bra sizing system formed by anthropometric measurements of Sichuan Chinese females. *Ergonomics*, 63(11), 1434–1441. https://doi.org/10.1080/00140139.2020.1795276
7. Sohn, M., Kim, D.-E. (2026). Body shape and bust variations by ethnicity and BMI using SizeUSA data. *Fashion and Textiles*, 13(1). https://doi.org/10.1186/s40691-026-00456-z
