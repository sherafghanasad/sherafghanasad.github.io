Surat emissions market data pack (Chapter 4)
Public Economics for Developing Countries, Chapter 4, Evidence Spotlight
"A market for smoke in Surat".

SOURCE. One CSV file cut from the replication package of
Greenstone, Michael, Rohini Pande, Nicholas Ryan, and Anant Sudarshan. 2025.
"Can Pollution Markets Work in Developing Countries? Experimental Evidence
from India." Quarterly Journal of Economics 140(2): 1003-1060.
doi:10.1093/qje/qjaf009. Package: Harvard Dataverse, doi:10.7910/DVN/PDFDKR
(data licensed CC BY 4.0 per the package's LICENSE.txt; this pack is shared
under the same terms). File used: Rule0_Panel (the authors' plant-month
particulate mass, their rule-0 series). Cite the article, not this pack.
Changes from the authors' file: plant identifiers recoded 1-292 in shuffled
order; a phase label and the cap per market plant added; nothing else.

ROWS. 7,008 rows: one for each of the 292 plants that reported monitor data
(156 market, 136 control) in each of 24 months, April 2019 to March 2021.

COLUMNS
  plant             plant identifier (1-292)
  arm               market or control (assigned at random)
  month             YYYY-MM; each month runs from the 16th to the 15th, so
                    2019-12 runs from 16 December 2019 to 15 January 2020;
                    2021-03 holds data to 3 April 2021 only (about 19 days)
  phase             before market, mock trading, market live, or trading halted
                    (COVID-19: months 2020-03 to 2020-09; Diwali: 2020-11;
                    2020-10 was mock trading)
  pm_kg             particulate matter emitted that month, kilograms. BLANK when
                    a chimney sent no data for the month. Never read blank as 0.
  log_pm_kg         natural log of pm_kg
  main_sample       1 for the 13 months the study's main estimates use
  cap_per_plant_kg  the market cap divided equally among the 162 market plants
                    (1,728 / 1,235 / 1,111 / 1,049 kg); blank outside main_sample

CHECK VALUES (the chapter's Rebuild-it steps)
  Step 0  7,008 rows; 292 plants, 156 market and 136 control
  Step 1  main_sample = 1, blank pm_kg dropped, mean by month and arm:
          2019-12 gives 937.9 kg (market) and 1,211.9 kg (control);
          the market mean is below the control mean in all 10 "market live" months
  Step 2  each plant's mean pm_kg over its main-sample months:
          market 1,022 kg, control 1,397 kg, gap 375 (27 percent of control)
  Paper (Table III): log emissions -0.193 (SE 0.076) without filling missing
          months; -0.282 (0.075) and -0.316 (0.057) with the two filling rules
