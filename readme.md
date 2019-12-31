# Exceedance calculator
Calculate exceedance and warning level from discharge values. 
Created for implementation as part of ClimaCell WRF-hydro workflow

### Usage:
```python
from main import exceedance_calculator
exceedance_filename = "path/to/CSV/file"
warning_levels = exceedance_calculator(exceedances_filename=exceedances_filename, discharges=discharges_series) 
```

### Test:
`python -m pytest`

#### Exceedances file structure:
- CSV file, one header line.
- One line per station 
- Stations ID column's name must be "stn_id".
- One column per exceedance probability value.
- Exceedance columns names must have pattern: `^[0-9]*_percent`
- Exceedance columns values must be numeric.
- example: 

stn_id | 1_percent | 2_percent | 5_percent | 10_percent | 20_percent | 50_percent
--- | :---: | :---: | :---: | :---: | :---: | :---: |
61000 | 320 | 120 | 60 | 22 | 16 | 10
60190 | 29.52564 | 350 | 125 | 78 | 31 | 21.5 | 12


#### probability --> warning level mapping: 
Probability of Exceedance | Flood Index
--- |:---:|
No flow | 0
&gt;50% (every year)  | 1
50-20% (every 1-5 years) | 2
20-10% (every 5-10 years) | 3
10-5% (every 10-20 years) | 4
5-2% (every 20-50 years) | 5
<2% (over 50 years) | 6
