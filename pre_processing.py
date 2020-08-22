import json
import pandas as pd
import pycountry

def import_data(): 
   with open('WeeklyWholesaleMarketPrices.json', encoding = "utf8") as f:
    d = json.load(f)

   data_main = pd.json_normalize(d["WeeklyWholesaleMarketPrices_PrixHebdomadaireMarcheGros"])

   data_english = data_main[['Date', 'CentreEn_CentreAn', 'CmdtyEn_PrdtAn', 'VrtyEn_VrteAn', 'GradeEn_CtgryAn', 
   'Cntry_Pays', 'ProvState_ProvEtat', 'LowPrice_PrixMin', 'HighPrice_PrixMax', 
   'PkgTypeEn_EmpqtgAn', 'PkgQty_QtePqt', 'PkgWt_PdsPqt', 'UnitMsrEn_QteUnitAn', 
   'PkgSizeEn_TaillePqtAn']]

   return (data_english)

def get_location_full_names(data): 
   
   data['country_name'] = data.apply(get_country_name, axis = 1)

   states = {
      'AK': 'Alaska',
      'AL': 'Alabama',
      'AR': 'Arkansas',
      'AS': 'American Samoa',
      'AZ': 'Arizona',
      'CA': 'California',
      'CO': 'Colorado',
      'CT': 'Connecticut',
      'DC': 'District of Columbia',
      'DE': 'Delaware',
      'FL': 'Florida',
      'GA': 'Georgia',
      'GU': 'Guam',
      'HI': 'Hawaii',
      'IA': 'Iowa',
      'ID': 'Idaho',
      'IL': 'Illinois',
      'IN': 'Indiana',
      'KS': 'Kansas',
      'KY': 'Kentucky',
      'LA': 'Louisiana',
      'MA': 'Massachusetts',
      'MD': 'Maryland',
      'ME': 'Maine',
      'MI': 'Michigan',
      'MN': 'Minnesota',
      'MO': 'Missouri',
      'MP': 'Northern Mariana Islands',
      'MS': 'Mississippi',
      'MT': 'Montana',
      'NA': 'National',
      'NC': 'North Carolina',
      'ND': 'North Dakota',
      'NE': 'Nebraska',
      'NH': 'New Hampshire',
      'NJ': 'New Jersey',
      'NM': 'New Mexico',
      'NV': 'Nevada',
      'NY': 'New York',
      'OH': 'Ohio',
      'OK': 'Oklahoma',
      'OR': 'Oregon',
      'PA': 'Pennsylvania',
      'PR': 'Puerto Rico',
      'RI': 'Rhode Island',
      'SC': 'South Carolina',
      'SD': 'South Dakota',
      'TN': 'Tennessee',
      'TX': 'Texas',
      'UT': 'Utah',
      'VA': 'Virginia',
      'VI': 'Virgin Islands',
      'VT': 'Vermont',
      'WA': 'Washington',
      'WI': 'Wisconsin',
      'WV': 'West Virginia',
      'WY': 'Wyoming'
   }

   prov_terr = {
      'AB': 'Alberta',
      'BC': 'British Columbia',
      'MB': 'Manitoba',
      'NB': 'New Brunswick',
      'NL': 'Newfoundland and Labrador',
      'NT': 'Northwest Territories',
      'NS': 'Nova Scotia',
      'NU': 'Nunavut',
      'ON': 'Ontario',
      'PE': 'Prince Edward Island',
      'QC': 'Quebec',
      'SK': 'Saskatchewan',
      'YT': 'Yukon'
   }

   data_canada = pd.DataFrame(data[data['country_name'] == "Canada"])
   data_canada['prov/state_name'] = data['ProvState_ProvEtat'].map(prov_terr)

   data_usa = pd.DataFrame(data[data['country_name'] == "United States"])
   data_usa['prov/state_name'] = data['ProvState_ProvEtat'].map(prov_terr)

   data_international = pd.DataFrame(data[(data['country_name'] != "Canada") & (data['country_name'] != "United States")])
   data_international['prov/state_name'] = ''

   data = pd.concat([data_canada, data_usa, data_international])

   return(data)

def get_country_name(data):

   list_alpha_2 = [i.alpha_2 for i in list(pycountry.countries)]

   if (len(data["Cntry_Pays"]) == 2 and data["Cntry_Pays"] in list_alpha_2):
      return pycountry.countries.get(alpha_2 = data["Cntry_Pays"]).name
   else: 
      return 'invalid'

def get_regions(data):

   canada_regions = {
    'AB': 'West',
    'BC': 'West',
    'MB': 'West',
    'NB': 'East',
    'NL': 'East',
    'NT': 'West',
    'NS': 'East',
    'NU': 'West',
    'ON': 'East',
    'PE': 'East',
    'QC': 'East',
    'SK': 'West',
    'YT': 'West'
   }

   us_regions = {
         'AK': 'North',
         'AL': 'Southeast',
         'AR': 'Southeast',
         'AS': 'International',
         'AZ': 'Southwest',
         'CA': 'Southwest',
         'CO': 'Central',
         'CT': 'Northeast',
         'DC': 'Northeast',
         'DE': 'Northeast',
         'FL': 'Southeast',
         'GA': 'Southeast',
         'GU': 'International',
         'HI': 'International',
         'IA': 'Central',
         'ID': 'Northwest',
         'IL': 'Central',
         'IN': 'Central',
         'KS': 'Central',
         'KY': 'Central',
         'LA': 'Southeast',
         'MA': 'Northeast',
         'MD': 'Northeast',
         'ME': 'Northeast',
         'MI': 'Northeast',
         'MN': 'Minnesota',
         'MO': 'Northeast',
         'MP': 'International',
         'MS': 'Southeast',
         'MT': 'Northwest',
         'NA': 'International',
         'NC': 'Southeast',
         'ND': 'Northeast',
         'NE': 'Central',
         'NH': 'Northeast',
         'NJ': 'Northeast',
         'NM': 'New Mexico',
         'NV': 'Southwest',
         'NY': 'Northeast',
         'OH': 'Northeast',
         'OK': 'Central',
         'OR': 'Northwest',
         'PA': 'Northeast',
         'PR': 'International',
         'RI': 'Northeast',
         'SC': 'Southeast',
         'SD': 'Central',
         'TN': 'Southeast',
         'TX': 'Southwest',
         'UT': 'Southwest',
         'VA': 'Southeast',
         'VI': 'International',
         'VT': 'Northeast',
         'WA': 'Northwest',
         'WI': 'Northeast',
         'WV': 'Northeast',
         'WY': 'Central'
   }
   
   data_canada = pd.DataFrame(data[data['country_name'] == "Canada"])
   data_canada['region'] = data['ProvState_ProvEtat'].map(canada_regions)

   data_usa = pd.DataFrame(data[data['country_name'] == "United States"])
   data_usa['region'] = data['ProvState_ProvEtat'].map(us_regions)

   data_international = pd.DataFrame(data[(data['country_name'] != "Canada") & (data['country_name'] != "United States")])
   data_international['region'] = ''

   data = pd.concat([data_canada, data_usa, data_international])

   return(data)

def pre_processing():
   data = import_data()
   data = get_location_full_names(data)
   data = get_regions(data)
   data.to_csv('Imported Data.csv')

pre_processing()
