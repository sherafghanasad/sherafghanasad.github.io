Where the smoke stays: crop fires by district and month (Chapter 4)
Public Economics for Developing Countries, Chapter 4, Data problem 19.

SOURCE. One CSV file summed from the cell-month panel in the replication
package of Dipoppa, Gemma, and Saad Gulzar. 2024. "Bureaucrat Incentives
Reduce Crop Burning and Child Mortality in South Asia." Nature 634:
1125-1131. doi:10.1038/s41586-024-08046-z. Package: Code Ocean,
doi:10.24433/CO.6383087.v1 (data CC0). File used:
data_2012_2022_downup.dta. Cite the article, not this pack. The cells are
summed by district, month and smoke group; no value is changed.

ROWS. 48,890 rows: one for each district, month (September 2012 to August
2022), and smoke group, for Pakistan's Punjab and five Indian states and
territories (Punjab, Haryana, Uttar Pradesh, Delhi, Bihar).

COLUMNS
  country      India or Pakistan
  province     Punjab (Pakistan), Punjab (India), Haryana, Uttar Pradesh, Delhi, Bihar
  district     district name (two names repeat; group by distr_id)
  distr_id     district identifier (207 districts, 36 in Pakistan's Punjab)
  year, month  calendar year and month of the fires
  smoke_stays  1 = the cells whose smoke the month's usual wind carries mostly over
               their own district; 0 = mostly out of it (the authors' downup_dummy)
  fires        satellite fire detections in those cells that month
  cells        number of cell-months summed (cells are small squares of land)
  mean_fires   fires / cells

CHECK VALUES
  48,890 rows; 207 districts; 17,979,600 cell-months; 2,121,263 fires.
  Fires per cell-month, all rows: smoke stays 0.1116, smoke leaves 0.1245.
  Pakistan's Punjab, October and November: stays 0.1484, leaves 0.1240.
