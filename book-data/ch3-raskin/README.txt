Raskin identification cards data pack (Chapter 3)
Public Economics for Developing Countries, Chapter 3, Evidence Spotlight
"A card for a rice subsidy that leaked".

SOURCE. One CSV file, values unchanged, cut from the replication package of
Banerjee, Abhijit, Rema Hanna, Jordan Kyle, Benjamin A. Olken, and Sudarno
Sumarto. 2018. "Tangible Information and Citizen Empowerment: Identification
Cards and Food Subsidy Programs in Indonesia." Journal of Political Economy
126(2): 451-491. doi:10.1086/696226. File used: combined_pooled.dta in the
authors' package (linked from Benjamin Olken's MIT web page). Cite the
article, not this pack.

ROWS. 9,312 rows: one for each household in each of the two surveys used
for the paper's Table 3 (about 2 and 8 months after the cards were mailed),
the analysis sample only. Eligible households in bottom-decile villages who
were not mailed a card are excluded, as in the paper.

COLUMNS
  hhid_pooled    household identifier
  hhea           village identifier (572 villages; cluster by this)
  kec_id         subdistrict identifier
  kab_id         district identifier
  wave           survey: 1 = about 2 months after the cards, 2 = about 8 months
  t2treatment    arm of an earlier targeting experiment (strata = t2treatment x kec_id)
  eligible       1 = on the official eligibility list, 0 = not on it
  treatment      1 = card village (any card arm), 0 = control village
  CTL            1 = control village
  B10            1 = cards mailed only to the bottom 10 percent of households
  PRC            1 = card also printed the copay price
  ENH            1 = public information arm (list of eligible households made public)
  samplea, sampleb, samplec, sample1cs1, sample2cs1, sample3cs1
                 sample indicators used as controls in the paper's regressions
  t2trm1, t2trm2, t2trm3   earlier-experiment arm dummies (absorbed by the strata)
  weight_fs_CvC  survey weight used in the paper's Table 3
  bought_last2m  1 = bought Raskin rice in the period asked about
  amtraskin      Raskin rice bought per month (kg)
  price_hh       price paid for Raskin rice (rupiah per kg)
  subsidy_rcvd   subsidy received per month (rupiah): (market price - price paid) x kg,
                 averaged over the months asked about; 0 if nothing was bought

CHECK VALUES (the chapter's Rebuild-it steps; run in Python and R)
  Step 0  9,312 rows; eligible 5,693, ineligible 3,619; 572 villages, 378 card villages
  Step 1  eligible, weighted by weight_fs_CvC, one row with no subsidy dropped:
          control 28,604.6, card 35,845.5, gap 7,240.9 rupiah (25.3%)
  Step 2  ineligible: control 18,753.9, card 19,265.4, gap 511.5
  Paper's regression (optional): subsidy_rcvd on treatment, stratum fixed
          effects (t2treatment x kec_id), the sample indicators, weights,
          clustered by hhea: eligible 7,455.1 (SE 1,327.9); ineligible 525.8 (1,034.6)
