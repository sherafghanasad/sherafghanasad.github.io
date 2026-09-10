# Colombia state-capacity data pack (chapter 1, Evidence Spotlight and Data problem 27)

Two plain CSV files re-exported, values unchanged, from the replication
file of Acemoglu, García-Jimeno and Robinson, "State Capacity and Economic
Development: A Network Approach," *American Economic Review* 105(8), 2015
(`State_Capacity_Network_Work.mat`, 1,019 municipalities). The original
package, with the authors' code and data dictionary, is at
sherafghanasad.com/go/ch1-agjr. Column names follow the study's data
dictionary. Any of Stata, R, Python, or MATLAB reads these files.

## agjr-colombia.csv — one row per municipality (1,019 rows)

| column | study source | meaning |
|---|---|---|
| dane_code | DaneCodes | municipality identifier |
| department | DD | department name |
| dept_capital | Dc | 1 if the department capital |
| notary_offices, telecom_offices, post_offices, health_centers, health_posts, schools, libraries, fire_stations, jails, public_instrument_offices, tax_offices | S cols 6, 7, 8, 11, 12, 13, 14, 15, 16, 18, 19 | the eleven locally run agency types, counts in 1995; blank where the study has no count |
| municipal_employees | S col 1 | municipality public employees |
| primary_enrollment, secondary_enrollment | Yg cols 1, 2 | enrollment rates 1992–2002 (shares; primary can exceed 1) |
| infant_mortality | Yg col 3 | infant mortality rate |
| aqueduct_coverage, sewage_coverage, electricity_coverage | Yg cols 4, 5, 6 | coverage in 2002, percent |
| vaccination_coverage | Yg col 7 | vaccination coverage in 2002, share (multiply by 100 for percent) |
| not_poor_1993, not_poor_2005 | Yg cols 8, 9 | share of people above the poverty line, percent |
| life_quality_index | Yg col 10 | life-quality index 2004 |
| tax_per_capita_2002 | Yg col 15 | per-capita tax collection 2002 |
| crown_employees_1794 | C col 1 | total crown employees in the 1794 register |
| crown_employees_nonmilitary_1794 | C col 2 | non-military crown employees, 1794 |
| colonial_state_index | C col 3 | the study's colonial state presence index |
| colonial_city | C col 4 | 1 if the town held city status under the crown |
| royal_road_distance | R | distance to the royal roads |
| literacy_1918, schooling_1918, vaccination_1918 | YH cols 1, 2, 3 | the 1918 outcomes used as placebos |
| longitude, latitude, area_sqkm, elevation_m, rainfall_mm, distance_coast_km, distance_magdalena_km | G cols 1, 2, 3, 4, 5, 12, 10 | geography the study holds fixed |
| highway_distance_m, population_1995, pop_density_1995, urban_share_1995, malaria_incidence, oil_producer | Xs cols 1, 2, 3, 4, 8, 10 | other controls |
| land_agri_share, land_mountain_share | L cols 9, 14 | land quality and terrain |
| slaves_share_1843, encomienda_1560, gold_mine_1560, foundation_year, population_1843 | H cols 1, 5, 6, 7, 8 | colonial and pre-colonial history |

## agjr-neighbors.csv — one row per ordered pair of neighbors (5,592 rows)

`dane_code, neighbor_dane_code`: municipality and one of its neighbors, from
the study's adjacency matrix. Every pair appears twice (once in each
direction), so a merge on `neighbor_dane_code` followed by a mean by
`dane_code` gives each municipality's average over its neighbors.

## Check values (Spotlight steps and Data problem 27)

- Agency count = the eleven agency columns added plainly (a blank drops the
  municipality): 976 municipalities remain; mean 21.6, median 10.
- not_poor_2005: median 57.3. Correlation of log(1 + agencies) with
  not_poor_2005: 0.40.
- Group means by agency count (fewer than 8; 8–9; 10–12; 13–19; 20–39; 40 or
  more): not_poor_2005 51.1, 53.6, 55.4, 59.6, 61.6, 71.6;
  100 × vaccination_coverage 41.8, 44.1, 45.6, 47.1, 49.1, 50.8.
- crown_employees_1794: 865 zeros; maximum 3,844 (Bogotá). Median agency
  count with five or more crown employees: 39; with fewer: 10.
- The map next door (average crown employees over neighbors; municipalities
  with a complete agency count): no staffed neighbor, n = 344, median
  agencies 10, mean not_poor_2005 56.3; the rest split into thirds by that
  average: median agencies 10, 10, 11 and mean not_poor_2005 56.1, 54.9,
  58.3. Raw group means do not show the neighbor effect: that is why the
  Spotlight's Panel B is read from the paper's estimates, not rebuilt.

## If you try an instrumental-variables regression

The pack has what a two-stage least squares needs: own and neighbors'
agencies, neighbors' 1794 crown employees, colonial state index and
royal-road distance (average them over the neighbors file), and the
controls above. What you will find:

- The first stage for the *neighbors'* state is strong: neighbors' log
  agencies on neighbors' 1794 presence, holding own presence and
  department fixed, F(3) about 71 (n = 976). Relevance, seen.
- The first stage for a municipality's *own* state is weak: own log
  agencies on the same instruments, F(3) about 3. Own and neighbors' log
  agencies correlate at about 0.30, so the lever reaches own state only
  faintly in a single equation.
- A plain 2SLS therefore gives own-effect estimates that swing in sign
  and size with the control set. The study identifies the own effect
  through its network model, in which every municipality's capacity
  responds to every neighbor's at once, estimated as a system. That is
  why the chapter's Panel B is read from the paper rather than rebuilt,
  and why the honest exercise is the first stage, the placebo outcomes,
  and the reasons a single equation cannot do the rest.

Built by `04-Figures-Data/the-state/scripts/agjr-csv-pack.py` (2026-09-10).
Redistributed for teaching with attribution to the authors; cite the
article, not this pack.
