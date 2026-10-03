# Bra Fit Research

An independent, non-commercial research project on bra sizing: what actually
predicts fit, and why the near-universal two-measurement method (underbust +
bust, convert the difference to a cup letter) is not well supported by data.

This started as personal curiosity — reading patents, standards, and the
academic literature on breast anthropometry and bra fit, then testing what
holds up against real data. It is not a product and not a commercial venture.

## Papers

- **[What Predicts Bra Fit, and Why It's Not What You Think](papers/paper1-what-predicts-bra-fit/paper.md)**
  — a secondary analysis of ~35,000 crowdsourced bra reviews matched with
  real garment measurements. Underbust circumference does not predict fit;
  cup geometry does.

- **A Quantum of Unmercy: Why Bra Sizing Cannot Be Transferred Between
  Brands** — in progress. Covers the sizing engine, the verified per-brand
  formula registry, and why the same cup letter means a different volume at
  different brands.

## Data

The underlying datasets (Bratabase measurements and reviews) are not
redistributed here — see the "Data and Method" section of the paper for why.
To assemble comparable data yourself: [bratabase.com](https://bratabase.com)
for the primary source, and for comparison,
[Clothing Fit Dataset for Size Recommendation](https://www.kaggle.com/datasets/rmisra/clothing-fit-dataset-for-size-recommendation)
on Kaggle (the ModCloth and RentTheRunway data). Each paper's `analysis/`
folder has the code used to produce its tables (see each paper for exactly
which ones), but not the raw data it ran on.

## License

Two separate licenses apply:
- **Code** (`analysis/` folders): MIT — see [LICENSE](LICENSE).
- **Papers** (text, figures, tables): CC BY 4.0 — see [papers/LICENSE](papers/LICENSE).

Both are free to reuse; the condition is attribution.

## Declaration of AI Use

The author used Claude (Anthropic) to assist with computational analysis and
code implementation. The tool was used under the author's direction. All
findings and figures were independently verified by the author, who takes
full responsibility for the content of this work.

## Contact

I'm open to questions and ideas for collaboration. Open an issue in this repository.
