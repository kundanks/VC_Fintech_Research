***Time series example
clear
capture log close

cd "C:\Users\Kundan\Documents\Brandeis\StataCourse\Day 7"

***Simple time trend regression
import delimited regression.csv, clear
describe
correlate gdp_per_capita deal_amount
correlate deal_amount gdp_per_capita population hpi unemployment_rate

pwcorr deal_amount gdp_per_capita population hpi unemployment_rate
graph matrix deal_amount gdp_per_capita population hpi unemployment_rate, half msize(vsmall) scale(0.8) title("Correlation Plot (`val')") (lfit deal_amount gdp_per_capita)
graph matrix deal_amount gdp_per_capita population hpi unemployment_rate, by(deal_amount) scale(0.5) half msize(vsmall) scale(vsmall)
regress gdp_per_capita deal_amount

*******************************
twoway (lfit deal_amount gdp_per_capita) (scatter deal_amount gdp_per_capita), xscale(log)
regress deal_amount gdp_per_capita
twoway (lfitci deal_amount gdp_per_capita) (scatter deal_amount gdp_per_capita), note(R-squared=.0916)

***********************************
import delimited regression_1126.csv, clear

foreach val in "San Francisco, CA" "San Jose, CA" "Boston, MA-NH" "New York, NY" "Chicago, IL" "San Diego, CA" "Los Angeles-Long Beach, CA" "Washington, DC-MD-VA-WV" "Seattle-Bellevue-Everett, WA" "Dallas, TX" {
import delimited regression_1126.csv, clear
keep if msa == "`val'"
twoway (lfit deal_amount gdp_per_capita) (scatter deal_amount gdp_per_capita), title("Deal Amount by GDP Per Capita (`val')") xtitle("GDP Per Capita") ytitle("Deal Amount")  xlabel(,labsize(small)) ylabel(,labsize(small))
graph export "`val'_GDP.png", replace

twoway (lfit deal_amount population) (scatter deal_amount population), title("Deal Amount by Population (`val')") xtitle("Population (Thousands)") ytitle("Deal Amount")  xlabel(,labsize(small)) ylabel(,labsize(small))
graph export "`val'_Population.png", replace

twoway (lfit deal_amount hpi) (scatter deal_amount hpi), title("Deal Amount by HPI (`val')") xtitle("HPI") ytitle("Deal Amount")  xlabel(,labsize(small)) ylabel(,labsize(small))
graph export "`val'_HPI.png", replace

twoway (lfit deal_amount unemployment_rate) (scatter deal_amount unemployment_rate), title("Deal Amount by Unemployment Rate (`val')") xtitle("Unemployment Rate") ytitle("Deal Amount") xlabel(,labsize(small)) ylabel(,labsize(small))
graph export "`val'_Unemployment_Rate.png", replace
}

foreach val in "San Francisco, CA" "San Jose, CA" "Boston, MA-NH" "New York, NY" "Chicago, IL" "San Diego, CA" "Los Angeles-Long Beach, CA" "Washington, DC-MD-VA-WV" "Seattle-Bellevue-Everett, WA" "Dallas, TX" {
import delimited regression_1126.csv, clear
keep if msa == "`val'"
display("`val'")
correlate deal_amount gdp_per_capita population hpi unemployment_rate
}

foreach val in "San Francisco, CA" "San Jose, CA" "Boston, MA-NH" "New York, NY" "Chicago, IL" "San Diego, CA" "Los Angeles-Long Beach, CA" "Washington, DC-MD-VA-WV" "Seattle-Bellevue-Everett, WA" "Dallas, TX" {
import delimited regression_1126.csv, clear
keep if msa == "`val'"
display("`val'")
graph matrix deal_amount gdp_per_capita population hpi unemployment_rate, half msize(vsmall) scale(0.8) title("Correlation Plot (`val')")
graph export "`val'_Correlation.png", replace
}

foreach val in "San Francisco, CA" "San Jose, CA" "Boston, MA-NH" "New York, NY" "Chicago, IL" "San Diego, CA" "Los Angeles-Long Beach, CA" "Washington, DC-MD-VA-WV" "Seattle-Bellevue-Everett, WA" "Dallas, TX" {
import delimited regression_1126.csv, clear
keep if msa == "`val'"
display("`val'")
xtreg deal_amount gdp_per_capita population hpi unemployment_rate, re
}

use https://www.ssc.wisc.edu/sscc/pubs/files/dates.dta, clear

drop year1
gen year1=date(year,"YYYY/MM/DD")
gen year1 = date(year, "M/D/YYYY")
format year %td
year1 = year

describe

import delimited regression_1126.csv, clear
encode msa, gen(msa1)
encode year, gen(year1)
xtset msa1 year1
list
describe
xtreg deal_amount gdp_per_capita population hpi unemployment_rate, fe

areg deal_amount gdp_per_capita population hpi unemployment_rate, absorb(year1)