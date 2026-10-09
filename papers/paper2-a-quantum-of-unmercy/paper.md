# A Quantum of Unmercy: Why Bra Sizing Cannot Be Transferred Between Brands

## Contents

- [Introduction](#introduction)
- [Related Work](#related-work)
- [Self-Measurement: Where Precision Is Lost](#self-measurement-where-precision-is-lost)
- [Engine Architecture](#engine-architecture)
- [Brand Registry](#brand-registry)
- [One Band, Different Cup Quanta](#one-band-different-cup-quanta)
- [Why Different Brands Choose Different Steps](#why-different-brands-choose-different-steps)
- [Dormant Data, an Honest Boundary for Inclusion](#dormant-data-an-honest-boundary-for-inclusion)
- [What Scanning Showed, and What Remains Unanswered](#what-scanning-showed-and-what-remains-unanswered)
- [Limitations](#limitations)
- [Conclusion](#conclusion)
- [Data and Code](#data-and-code)
- [References](#references)

## Introduction

In the companion paper, *What Predicts Bra Fit, and Why It's Not What You Think*, it was shown on 34,505 reviews that the difference between underbust and bust circumference, which underlies almost every existing sizing method, does not predict actual fit. Cup parameters, by contrast, do. This raises an open question: if the two-measurement method is empirically unsupported, what could serve as a better-grounded alternative, and does one actually exist in a tested, not merely assumed, form?

There is a second, independent problem. Even where brands publish their own, more complex sizing formulas, these formulas do not agree with one another. A direct comparison of two real official size charts on the same band, EU70, shows a cup-letter discrepancy of up to 8 cm between brands, growing linearly in both directions from a single coincidental point of agreement. The cause is not noise at the edges of the tables: Triumph and Wolford use a cup step of exactly 2 cm per letter, matching the EN 13402-3 norm and Milavitsa's own formula, whereas Intimissimi uses a step of 5–5.5 cm per letter. This amounts to two different physical quanta, not one standard with rounding at the edges. A matching band scheme (the same EU65–EU110 range, in steps of 5) does not guarantee a matching cup scheme.

No tool known to me solves both problems at once: none shows a size with a quantified uncertainty band instead of false precision, and none simultaneously maintains a registry of brand formulas verified against primary sources.

This work sets out to build and document such an engine: a volume core with an uncertainty band, a registry of real brand formulas, and a direct empirical demonstration of the mechanism behind why a cup letter does not transfer between brands. To this end, the following tasks were addressed:

1. Design a volume core that converts body measurements into size candidates with an uncertainty band, instead of a single falsely precise number.
2. Assemble and document a registry of brand formulas, each verified against the brand's primary source, with a confidence/completeness label per brand.
3. Empirically demonstrate the difference in cup quantum by comparing official size charts of two or more brands on the same band (a directly verifiable comparison).
4. Explain why a scan is structurally superior to a tape measure for the geometric/construction signal, with a measured failure rate for tape on synthetic data.
5. Assess the limitations of the approach: the reliability of self-measurement, uncalibrated coefficients, a small validated sample, and who this could realistically help.

The object of this study is the process of converting body measurements into a bra size recommendation. The subject is the combination of quantified uncertainty, a verified brand registry, and the mechanism that makes transferring a letter between brands physically unworkable.

Methodologically, the work rests on extracting and verifying brand formulas from primary sources (not aggregators), direct pairwise comparison of brands' official size charts on the same band, and synthetic stress-testing of the geometric signal on a large sample of artificial profiles.

The scientific novelty lies in combining, for the first time, quantified uncertainty instead of false precision, a registry of only verified (not assumed) brand formulas, and a direct empirical demonstration that a shared band scheme does not guarantee a shared cup scheme.

## Related Work

The closest working tool in spirit is [ABraThatFits.org](https://abrathatfits.org), a server-side calculator that performs a real calculation. Tested against a real subject's data: the result (30DD UK) did not match either Intimissimi's recommendation (32C) or her own habitual size (32D). The two-step cup discrepancy is not explained by a simple sister-size shift and remains an unresolved mismatch, not an error in this work's own arithmetic.

Before publishing the engine's code, a freedom-to-operate check was carried out, to see whether some existing patent already covers this specific sizing method. Two patents turned out to be the closest in subject matter: US10018466B2, "Bra fitting method" (Van de Velde NV), and US10238155B2, "Bra engineering" (Laurie Braverman). Neither turned out to be an obstacle, but for different reasons. The first patent's sole independent claim is tied to a specific method of visualizing the result, building three graphs of a strictly defined kind; this work's engine produces its output differently and does not fall under the patent's wording. The second patent's all six claims describe the physical construction of the garment itself (cut, inserts, closures), not a method of calculating size – the patent protects the bra as an object, and does not intersect with this work's software component at all. Separately, a Cornell University patent (US12333595B2, Pei, Fan, Ashdown, granted 2025-06-17) describes a method of fitting a bra from the shape of the breast as captured by a 3D scan (surface convexity/concavity), rather than from linear measurements.

Industry-wide standards differ in detail but do not contradict the overall picture. GOST 29097-2015 defines size designation through underbust circumference and cup volume. EN 13402-3:2017, in its informative Table A.9, gives a bra grid: band 60–125 cm in steps of 5, the same step as the familiar EU size grid – brands have little room to diverge here. Cups AA–H, cup step 2 cm, but the standard explicitly states that these intervals "may vary by market and company." That is, even the closest thing to an official reference does not require a single quantum. So, in the absence of a strict requirement, the divergence between brands (detailed below) violates nothing.

Calibration of band sensitivity (BAND_SENSITIVITY) relies on Chan et al. (2019) – real data on tissue resection in reduction mammaplasty, converted into centimeters via the AU size convention for age. The calibration is confirmed by only one study, on bands AU12–18, and cannot be considered final. An earlier, independent confirmation of the same principle – that a given cup letter is not uniform across bands – comes from McGhee & Steele (2011); only the abstract of this paper is available, not the full text. According to the abstract: breast volume of 104 women, measured by water displacement, against their actually fitted bra size, range 125–1900 ml.

## Self-Measurement: Where Precision Is Lost

The most direct way to obtain volume not from an already-known size, but from body shape, is a 3D scan. The first testable question: can a body simply be scanned to get a working estimate, without resorting to self-measurement by tape at all?

A scanning attempt of our own was made and documented as an experiment: `scan_tools.py` reads a point cloud in the Scaniverse (PLY) format and estimates volume by the convex-hull method over horizontal slices – deliberately the simplest method available. The file reads correctly, and landmarks (waist and bust) and volume are extracted. The bust landmark carries a known caveat: it is the best clean candidate along the profile, not a guaranteed peak circumference. If arm contamination begins below the true peak, the number comes out lower than the real value. This does not amount to a "scan → finished size" pipeline. It was a test of basic feasibility.

A separate, more general problem is the mechanics of self-measurement as such. A person cannot see their own back, cannot check from the side whether the tape sits level, and is not trained in the protocol. The companion paper already gives a direct quantitative measure of this gap: in Haworth et al. (2025, n=24), subjective fit reports matched a professional fitter's objective assessment in only 51% of cases – and that was the fit of a finished garment, not taking a measurement from scratch, i.e., an easier task than the one facing someone measuring themselves.

One concrete example of why even careful instrumental measurement does not save the day is the dart angle – a geometric signal that determines the cup's construction class. It is computed as the difference between the base radius and the lower arc length. For most women these two quantities are close to each other, meaning the angle is computed as the difference of two nearly equal numbers. Two independent tape pulls (each with roughly 6–8% noise) amplify this difference many times over. A run on 2000 synthetic profiles showed a 36.2% false-positive rate against a 5.7% true rate. For this signal, tape is not "less accurate" – it is structurally unfit, regardless of how carefully the measuring person does the job.

One might suppose that, since tape fails here, the eye or touch, backed by experience, could make up for it. Killaars et al. (2026, Aesthetic Plastic Surgery) tested exactly this: how accurately experienced plastic surgeons and laypeople judge by eye which side of the breast is larger, compared against an objective 3D measurement (VECTRA). Surgeons' accuracy was 53.8% (Cohen's kappa 0.08, barely distinguishable from zero); laypeople's was 48.6% (kappa −0.07, worse than chance). The authors explicitly state that no clear threshold of asymmetry perception was found at all – even with a large objective difference, the breasts were often perceived as symmetrical.

All of this points, from different directions, to the same conclusion. Self-measurement is unreliable overall (Haworth); tape is instrumentally unable to capture the geometric signal (dart angle); and visual/tactile judgment fails even among trained specialists (Killaars). Neither training, nor care, nor experience closes this gap. Only a tool that provides direct shape coordinates – a scan – can close it. This also suggests a softer reading of the companion paper's finding. It may be that the industry standard of "two measurements" did not arise from manufacturer indifference, but from the fact that two simple linear measurements are roughly the ceiling of what an untrained person can reliably take on their own. The companion paper already showed that these two measurements do not predict fit, and this explains why the industry got stuck on them in the first place.

## Engine Architecture

At the core is the body passport (`BodyPassport`) – a data structure that accepts physical body measurements. Required fields: band (underbust circumference), a volume estimate, and upper-body geometric measurements (height from the base of the neck to the nipple, breast base width, intermammary distance, shoulder slope). Optional fields are collected separately: bust circumference in three positions (standing/bent forward/supine), base radius and lower arc length for the dart angle, asymmetry, and self-reported size.

These fields are not all equal in role and use. The main numeric result (`sister_ladder`) – three size candidates representing the same volume distributed differently between band and cup – is built from just two quantities: band and breast volume estimate. The volume estimate is obtained one of two ways: entered directly by hand, or computed from a self-reported size via Chan et al.'s (2019) quadratic formulas. The geometric measurements (height, base width, intermammary distance, shoulder slope, circumferences in three positions) do not enter this calculation at all.

However, these fields are not useless. They feed into two other, narrower decisions. The dart angle (from base radius and lower arc length) determines the cup's construction class, but is only computed if the measurement method is a scan. On a tape measurement, this signal is not built at all, for the same reason already discussed above: tape cannot reliably capture this quantity. The difference between the standing and bent-forward circumferences, if measured and if it exceeds the noise floor of two independent tape pulls (combined ≈11.3%, derived from the already-documented noise of a single pull), adds a directional, non-numeric note about construction to the recommendation. This is an example of including previously unused data without inventing a threshold for an effect on fit that does not exist in the literature.

A separate layer forms the list of caveats, assembled from the body passport's actual state: a buffer for stretchable material, cyclical volume variation, shape versus volume, a band outside the calibrated range, the coarseness of a tape-only estimate without a scan, protocol mismatches with a specific brand, the unavailability of the geometric signal from tape, and the statistical improbability of a claimed perfect symmetry (drawing on Killaars et al., cited above). This is what distinguishes the tool from an ordinary calculator that outputs a single number without context of reliability.

The output layer is kept separate from the calculation layer. Internally, the engine computes in millimeters and milliliters; the raw math is never exposed outward. Only candidates translated into familiar letters are shown, marked with "≈" if the letter has not been confirmed directly by the person.

The brand registry is a separate, growing layer on top of the core: `lookup_brand` (brand query, passport) returns a result with one of four status labels – "exact match" / "nearest" / "band only, no cup" / "no data." A shared sister-size calculation is not used across all brands. Architecturally, this is a direct consequence of the finding discussed in the next section: the assumption that a matching band scheme implies a matching cup scheme was tested and refuted. The registry therefore never extrapolates a result from one brand onto another, and stores only what has been verified against each specific brand's primary source.

## Brand Registry

The registry is built on one rule: a brand's formula is used only if it has been verified by me against a primary source – the brand's own website, calculator, or official size chart – and is never extrapolated from another brand by analogy, even when the band scheme matches. The test registry currently holds five brands, each with its own level of data completeness: Intimissimi (full formula, band and cup, confirmed in a fitting room), Wolford (full formula, a two-dimensional band×cup grid), Milavitsa (full formula using the classical difference method), Ewa Michalak (full formula with three input measurements and a matrix), and La Perla (band only – the brand has not published a cup formula, flagged as a limitation of the source).

Verifying against a primary source meant reproducing its edge cases word for word. For Milavitsa, rounding is done upward even if the distance to two neighboring grid values is exactly equal. For Wolford, an edge case arose in our own data: on a real subject's body, the distance to two neighboring cup letters (70A and 70B) came out exactly equal, so both options had to be returned as equally likely rather than arbitrarily picking one.

Different brands require different measurements, not just different formulas. Ewa Michalak's formula is explicitly built for a bust circumference taken bent forward, whereas most other sources (and this work's general body measurement protocol) use the circumference taken standing upright. The registry interface's first version passed the same measurement, standing circumference, to every brand, which for Ewa Michalak produced a silent error: a recommendation of 75AA instead of the correct 75A, computed separately on the same body with the same code given the correct input. The error was not visible from the outside – both numbers looked like a plausible result. After the fix, each brand's function pulls exactly the passport fields its own protocol requires, and explicitly returns a rejection if a needed field is missing, instead of silently substituting something similar.

The practical point of this discipline is not an abstract notion of "accuracy," but the fact that without it the error stays invisible. Had the interface kept passing Ewa Michalak the standing circumference, the result (75AA) would have looked entirely plausible – nothing in the number itself would have revealed that it was computed from the wrong input. Verification against the primary source, and respect for a specific brand's protocol, is what turns a plausible-but-wrong answer into one that is actually correct for that specific brand, rather than a generic, averaged estimate.

## One Band, Different Cup Quanta

This finding emerged while testing a specific hypothesis. The assumption seemed plausible: since many brands use the same band scheme (EU65–EU110, step 5 – independently confirmed across five sources), the cup could likely also be closed by analogy, without collecting each brand's formula separately. The test became possible as soon as two genuine official cup charts on the same band turned up – Triumph and Intimissimi, both EU70.

Result: at letter C the discrepancy was 1 cm – a single coincidental point. From there it grows linearly in both directions: at letter A, −8 cm; at letter F, +8 cm. The cause is not noise at the edges of the tables but different cup steps as such: Triumph's step is exactly 2 cm per letter (the same norm as EN 13402-3 and Milavitsa's own formula), while Intimissimi's is 5–5.5 cm per letter. These are two different physical quanta, not one standard with rounding at the edges.

The same test, with a different pair of brands – Wolford against Intimissimi – gave the same result: Wolford also uses a 2 cm step. Separately, through its own formula, the 2 cm step had already been confirmed for Milavitsa. In sum: three brands, Triumph, Wolford, and Milavitsa, independently converge on a 2 cm step, the same one found in the EN 13402-3 standard. Only Intimissimi uses a different step, 5–5.5 cm, under an identical band scheme across all four. The hypothesis of segmentation by band-grid type failed the test. A matching band scheme does not guarantee a matching cup scheme, and transferring one brand's formula to another without that brand's own data does not hold up.

## Why Different Brands Choose Different Steps

A plausible explanation lies in SKU (Stock Keeping Unit) economics, the classical operations-management dilemma between assortment precision and the cost of holding inventory. To test the claim, the economics were modeled on real data.

Demand was drawn from a real, large, and – crucially – non-lingerie source: the Kaggle "Clothing Fit Dataset for Size Recommendation" (ModCloth + RentTheRunway, already used in the companion paper), which gives 250,545 self-reported bra sizes from ordinary clothing shoppers – a population not self-selected for fit difficulty, unlike lingerie communities (Bratabase, r/ABraThatFits), which on inspection turned out to be skewed toward rare, large cup sizes. In this data the picture is the opposite, and expected: the top sizes are 34B, 34C, 34D, 36C, 36D – ordinary, common combinations.

On this real demand distribution, two scenarios were modeled for a single style/color at an annual demand of 10,000 units (an illustrative order-of-magnitude assumption, not a confirmed figure for any specific brand): a coarse quantum – a standard mass-market grid (4 bands × 4 cups, 16 SKUs) – and a fine quantum – the 159 band/cup combinations actually observed in the same data.

Result:

1. **Capital tied up in safety stock.** By the square root law (Maister, 1976, Harvard Business School – originally derived for centralizing warehouses by number of geographic locations; applied here by analogy to SKU count, not as a direct reproduction of the original study's conditions), required capital grows as √(N), meaning √(159/16) ≈ 3.15 times more capital for the fine quantum, for the same level of service.
2. **Minimum order quantity.** At a conservative MOQ of 100 units (the lower bound of the 50–100 range cited by the industry source argusapparel.com), 141 of the 159 fine-quantum SKUs (89%) fall below the minimum run – meaning they must either not be stocked at all, or ordered in a quantity that knowingly exceeds demand. The resulting forced surplus is 12,825 units per year – more than the entire modeled annual demand for the style. In the coarse scenario, only 1 of 16 SKUs falls below MOQ, an extremely rare combination.
3. **Unit cost.** At a real supplier's price tiers (seamapparel.com: \$18–30 per unit for runs up to 200, down to \$7–11 for runs of 1000+), the weighted average unit cost is \$13.79 for the fine quantum versus \$11.40 for the coarse one – 21% more expensive due to small batch sizes.

Three independent effects point in the same direction: a fine quantum is not just abstractly more expensive – it systematically creates a surplus of unsellable stock on the shelf, on a scale comparable to demand itself. Reproducible code for this calculation is published alongside the paper.

SKU economics does not mean the industry simply abandons the gaps between sizes; built-in engineering partially compensates for them. Existing patents confirm this directly: US9883702B2 (Mast Industries, 2018) describes a fabric with zonal elastic modulus – different tension in different parts of the same cup/wing; US9289017B2 (2016) describes a molded cup with three inserts of different stiffness across the neckline/underarm/center zones. Together with sister sizing (one volume, different band/cup pairs – the same logic as this work's volume core), this gives brands a real tool for closing part of the gap between coarse grid steps without increasing the number of SKUs.

That this tool does not close the gap entirely is not necessarily a matter of insufficient engineering on brands' part. Sister sizes only work if a buyer is willing to try a combination other than her "usual" letter, which requires understanding that cup and band are interdependent, not fixed independently. There is no direct quantitative measure of this willingness, but it is indirectly consistent with the already-cited gap between self-report and objective assessment (Haworth et al., 2025, 51% agreement): if a person does not always accurately judge a garment she is already wearing, it is unlikely she will confidently switch to an unfamiliar size combination on her own. This points to a gap in consumer education, not to brand indifference toward construction.

## Dormant Data, an Honest Boundary for Inclusion

The body passport collected bust circumference in three positions from the start – standing, bent forward, supine – but for a while none of them affected the recommendation at all.

The difference between the standing and bent-forward circumference is a plausible signal of tissue mobility under its own weight. The temptation was obvious: find a number, above which this difference means a firmer bra construction is needed. A direct published threshold of this kind (difference in centimeters or percent → degree of sag → construction requirements) could not be found in the available literature, despite a dedicated search.

Instead of an effect threshold, a more modest boundary was used: not "how much does this affect fit," but "is this even distinguishable from measurement noise." The file already had documented error for a single tape pull (around 6–8%, found during an independent check of the dart-angle geometric signal). For the difference between two independent pulls (standing and bent forward), this error combines in quadrature: √(0.08² + 0.08²) ≈ 11.3%. A signal below this threshold is indistinguishable from random hand tremor while measuring and is not flagged at all. Above it, it is noted as "plausible, not proven in magnitude," accompanied by practical, non-numeric advice: check fit not only standing, but also after moving around or later in the day.

Checking against two real bodies gave an honest, unforced result. For one subject the difference was 13% – above the noise floor, the note was added. For the other it was 3.6%, below the floor, and the engine added nothing. This is not a shortcoming. For the second case, there genuinely is nothing to say given this data, and admitting that is more honest than crafting wording that creates the appearance of a signal where none exists.

This discipline generalizes beyond this one specific measurement. Data that is collected but not used is worth revisiting as new questions arise, but it should only be brought into a decision through a boundary that can actually be justified (here, "distinguishable from noise"), not through an imagined connection to an outcome that was never actually measured.

## What Scanning Showed, and What Remains Unanswered

The `scan_tools.py` technical test confirmed that a point cloud in the Scaniverse (PLY) format reads correctly, and that landmarks and a rough volume estimate can be extracted from it. It was never the aim of this test to develop a full scanning software suite. The specific hypothesis was tested: whether this data path is workable at all, and whether it provides something tape does not. The answer to both questions is yes, and the test accomplished exactly what it was meant to.

Capture posture is not standardized. The body's position during the scan – standing naturally, arms held at the sides or slightly away from the body for camera access, with or without support – affects how breast tissue settles under its own weight, the same phenomenon that already showed spread between the standing/bent-forward/supine circumferences in the main measurement protocol. Which posture gives a measurement suitable for sizing (as opposed to merely any reproducible measurement) remains an open question, not resolved by this work or, as far as available sources show, by anyone else publicly.

The convex-hull method is structurally blind to concavities. The algorithm used in the test (horizontal slices, convex hull) cannot, by definition, capture concave regions of the surface – the fold under the breast, the gap between the breasts. It bridges these areas with a flat plane, which systematically overestimates volume exactly where individual differences (spread, nipple height – both already encountered in the companion paper) matter most for fit. This is a structural property of the method, which was stated from the outset to be a floor, not a target algorithm.

Self-capture mechanics are no easier than self-measurement mechanics. Capturing a 3D scan of one's own body alone – holding the phone, seeing one's own back and sides, maintaining stable lighting – is at least as hard as the task already discussed in the self-measurement section, and in some cases requires assistance or a tripod that may not be at hand. A scan removes the problem of instrumental measurement accuracy, but not the problem of executing the protocol by oneself.

Real body scans obtained during this work are not published or distributed in any form. Only the processing code is published.

Taken together, this is not a reason to abandon the approach – quite the opposite. It has already been shown concretely that a scan structurally solves two problems that neither tape (dart angle) nor a trained eye (Killaars et al.) can solve; the advantage is demonstrated, not abstract, on specific failures of the alternatives. At the same time, the cost of entry at current technology levels is low: the test itself was carried out using a free consumer app (Scaniverse) with no specialized equipment. The barrier to entry is methodological, not technological – standardizing posture, protocol, and the handling of concavities. This makes the direction promising: once the open questions above are resolved, the scan-based approach is economically justified not only for bespoke tailoring but potentially for the end consumer as well. Standardizing the method, not the availability of the technology, is what currently separates today's technical test from a working tool.

## Limitations

There is no independent way to compute volume from body shape. This is a central limitation of the entire work. The volume calculation does not use the geometric measurements collected (height, base width, intermammary distance, shoulder slope); the volume is derived either directly, or from an already-known size via Chan et al.'s (2019) formulas. Until an independent scan pipeline is built, the engine offers nothing fundamentally new, for a person without an already-known size, compared with simply asking what she already knows.

Small validated sample. The brand registry and the volume core have been checked against two real bodies with a known, confirmed fit outcome, not against a representative group. The directional findings (cup predicts better than band, the quantum differs between brands) rest on separate, larger-scale sources; but the direct check – "the engine recommended, the person tried it on, it fit" – has been done only twice, not on a statistically significant sample.

Uncalibrated band-sensitivity coefficient. BAND_SENSITIVITY = 3.7 is a real calibration from Chan et al. (2019), but from a single study and a narrow band range (AU12–18, roughly 73–92 cm). Outside this range the formula extrapolates linearly without verification; it should be trusted less there, and this is explicitly reflected in the report's uncertainty band.

The SKU economic model is realistic, but not confirmed from inside the industry. The calculation in the cup-quantum section is built on real demand (250,545 self-reported sizes) and a real supplier's price tiers (seamapparel.com), but not on specific brands' internal cost and margin data. It is a well-grounded, reproducible order-of-magnitude estimate.

There are still few verified brand formulas – this is not a matter of lacking data. The raw data on brands is in fact large (measurements of many brands drawn from Bratabase, ANSUR II, ModCloth/RentTheRunway), but these are raw garment measurements, not brands' actual sizing formulas. The registry in the strict sense (brand → formula, verified against a primary source) currently holds five entries. A brand's absence from the registry means "the formula has not yet been found and verified."

Datasets are not published, for the same reason as in the companion paper: derived figures and analysis code are shared, not the raw data from Bratabase, ModCloth, RentTheRunway, or ANSUR II.

## Conclusion

1. An identical band scheme across different brands does not guarantee an identical cup scheme. A direct comparison of official charts showed that Triumph, Wolford, and Milavitsa use a 2 cm cup step (matching EN 13402-3), while Intimissimi uses 5–5.5 cm, under an identical band range for all. Transferring one brand's formula to another without independent verification is a mistaken assumption.
2. Public size-comparison tables and calculators cannot structurally solve this problem, because there is no single cup quantum that such a table could be built on. Any universal size-equivalence table is, at best, an average that will be wrong for a specific brand exactly to the extent that its quantum differs from the average.
3. SKU economics is confirmed on real data. At real demand (250,545 self-reported sizes, ModCloth/RentTheRunway) and a real supplier's price tiers, a fine quantum requires roughly three times more capital for safety stock (square root law, by analogy), leaves 89% of SKUs below the minimum order quantity, and raises unit cost by 21%. Patents show that brands partially compensate for this through engineering (zonal elasticity, molded cup zones, sister sizing). The residual gap is plausibly tied not to engineering laziness, but to consumer education.
4. Verifying a brand formula against its primary source must include not just the formula itself, but the measurement protocol it assumes. A real bug that was found and fixed (Ewa Michalak receiving a standing circumference instead of the required bent-forward one) showed that an error of this kind stays plausible-looking, not self-evident.
5. Tape structurally cannot provide the geometric signal for construction (dart angle – a 36.2% false-positive rate on synthetic data), and visual or tactile judgment fails even among trained surgeons (Killaars et al., 2026: accuracy at chance level). A scan solves both problems structurally, not just incrementally, and demonstrates this at a low barrier to entry. What remains open are methodological, not technological, questions.
6. The central limitation of the entire work: there is still no way to independently compute volume from body geometry. The geometric measurements collected are used only for construction-related, not size-related, decisions; for a person without an already-known size, the engine does not yet offer much more than asking her what she already knows.
7. Despite striking failures at large sizes, brands' current sales matrix overall covers the demand of most buyers. There is hardly any conspiracy among manufacturers against the rest. Buyers often lack a clear understanding of what affects fit and how to choose correctly, and there is no accessible intermediary, an advisor or a tool, bridging complex knowledge and a simple decision, at scale. This is a solvable problem in principle, not a structural dead end.
8. Taken together, these findings point to a realistic, not inflated, scope of application. The difficulty of honest measurement makes the approach poorly suited to mass unsupervised self-use, and much better suited to settings where a trained person takes the measurement for a specific body for a specific garment – mainly bespoke tailoring, and, in the longer run, after and if a scan protocol is standardized, potentially the end consumer directly.

## Data and Code

This work does not publish body scans or third-party raw datasets. Code is published: `sku_economics_simulation.py` (the cup-quantum economic model) and `scan_tools.py` (reading PLY files, estimating volume by the convex-hull method over horizontal slices). Both reproduce the figures given in the text when run on the same source data. For independently assembling comparable data: [bratabase.com](https://bratabase.com), an open database of bra measurements and reviews (manually collected, not automated); the Kaggle ["Clothing Fit Dataset for Size Recommendation"](https://www.kaggle.com/datasets/rmisra/clothing-fit-dataset-for-size-recommendation) (the ModCloth and RentTheRunway datasets), the source of demand for the economic model; Kaggle's ["ANSUR II"](https://www.kaggle.com/datasets/saifsagor/ansur-ii) (an anthropometric survey of U.S. Army personnel), mentioned in the Limitations section as a source of raw measurements, not used in the final model due to the lack of a separate underbust-circumference field; and brands' official websites (Milavitsa, Wolford, Triumph, Intimissimi, Ewa Michalak), the primary source used to verify the registry's formulas.

An open question, not resolved within this work: there is a preliminary observation (so far a single real case, not proof) that in the budget lingerie segment, positive reviews may systematically fail to match what an honest body-based calculation would show. A plausible explanation is given by Barry Schwartz's (2004) Paradox of Choice: less choice, and rarer, less deliberated purchases, lower the cognitive load of the decision and thereby raise subjective satisfaction independent of the objective quality of the choice. Testing this requires accumulating further real cases; it is not established by a single observation.

## References

1. Chan, M., Lonie, S., Mackay, S., MacGill, K. (2019). Reduction Mammaplasty: What Cup Size Will I Be? *Plastic and Reconstructive Surgery – Global Open*, 7(6), e2273. https://doi.org/10.1097/GOX.0000000000002273
2. Gordon, C.C., Blackwell, C.L., Bradtmiller, B., Parham, J.L., Barrientos, P., Paquette, S.P., Corner, B.D., Carson, J.M., Venezia, J.C., Rockwell, B.M., Mucher, M., Kristensen, S. (2015). 2012 Anthropometric Survey of U.S. Army Personnel: Methods and Summary Statistics. Technical Report NATICK/TR-15/007, U.S. Army Natick Soldier Research, Development and Engineering Center.
3. Haworth, L., Sinclair, J., May, K., Janssen, J., Selfe, J., Chohan, A. (2025). Highlighting the need for change through an analysis of bra fit quality. *International Journal of Fashion Design, Technology and Education*, 19(2), 205–214. https://doi.org/10.1080/17543266.2025.2461460
4. Killaars, R.C., Janssen, D.G.E., Piatkowski de Grzymala, A.A. (2026). Breast Volume Measurements and Objectivations for Determination of Symmetry: A Retrospective Study in a Large Study Population. *Aesthetic Plastic Surgery*, 50(17), 7059–7065. https://doi.org/10.1007/s00266-026-06058-w
5. Maister, D. (1976). Centralisation of Inventories and the "Square Root Law". *International Journal of Physical Distribution*, 6(3), 124–134. https://doi.org/10.1108/eb014366
6. McGhee, D.E., Steele, J.R. (2011). Breast volume and bra size. *International Journal of Clothing Science and Technology*, 23(5), 351–360. https://doi.org/10.1108/09556221111166284
7. Schwartz, B. (2004). *The Paradox of Choice: Why More Is Less*. New York: Ecco.

**Standards:**

1. GOST 29097-2015. Corset articles. Dimensions.
2. EN 13402-3:2017. Size designation of clothes – Part 3: Measurements and intervals.

**Patents:**

1. Pei, J., Fan, J., Ashdown, S.P. Optimizing bra sizing according to the 3D shape of breasts. US Patent No. 12,333,595 B2, granted 2025-06-17. Assignee: Cornell University.
2. Martinet, N., Yip, S.H. Portion of bra and bra having zones of varying elastic moduli. US Patent No. 9,883,702 B2, granted 2018-02-06. Assignee: Mast Industries (Far East) Limited.
3. Raven, G., Mines, D., Roach, M., Scott, R. Pad for a brassiere cup. US Patent No. 9,289,017 B2, granted 2016-03-22. Assignee: Chico's Brands Investments, Inc.
4. Laan, D.J., de Rijck, R., Bal, M.F.J., Dotremont, S.M., Van Der Biest, G.J., Vermeire, L.R. Bra fitting method. US Patent No. 10,018,466 B2, granted 2018-07-10. Assignee: Van de Velde NV.
5. Braverman, L. Bra engineering. US Patent No. 10,238,155 B2, granted 2019-03-26.

**Industry sources (pricing and MOQ, cup-quantum section):**

1. seamapparel.com – manufacturing price tiers by batch size (checked while preparing this paper).
2. argusapparel.com – minimum order quantity (MOQ) range (checked while preparing this paper).
