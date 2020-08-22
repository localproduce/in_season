import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

def get_dates():
   #today = pd.datetime.today()
   today = pd.to_datetime("today")
   date_range_max = today - relativedelta(years = 1) + relativedelta(days = 14)
   date_range_min = today - relativedelta(years = 1) - relativedelta(days = 14)
   date_range = [date_range_min, date_range_max]
   return(date_range)

def get_nearest_centre(province):

   province_center = {
      "Alberta": "Alberta",
      "Saskatchewan": "Regina",
      "British Columbia": "Vancouver",
      "Manitoba": "Winnipeg",
      "Newfoundland": "St.John's",
      "Nova Scotia": "St.John's",
      "Prince Edward Island": "St. John's",
   }

   try: 
      center = province_center[province]
   except KeyError: 
      center = "Country"

   return(center)

def get_input_region(province):
   canada_regions = {
    'Alberta': 'West',
    'British Columbia': 'West',
    'Manitoba': 'West',
    'New Brunswick': 'East',
    'Newfoundland': 'East',
    'Northwest Territories': 'West',
    'Nova Scotia': 'East',
    'Nunavut': 'West',
    'Ontario': 'East',
    'Prince Edward Island': 'East',
    'Quebec': 'East',
    'Saskatchewan': 'West',
    'Yukon': 'West'
   }

   try: 
      region = canada_regions[province]
   except KeyError: 
      region = "West"

   return(region)

def get_in_season(data, province, date_range): 

   data['Date'] = pd.to_datetime(data['Date']).dt.tz_localize(None)
   date_min = date_range[0]
   date_max = date_range[1]

   #All produce available between two dates in nearest distribution centre
   center = get_nearest_centre(province)
   region = get_input_region(province)

   if (center == "Alberta"):
      center1 = "Wholesale-" + "Calgary"
      center2 = "Wholesale-" + "Edmonton"
      data = data.loc[(data['Date'].between(date_min, date_max)) & 
                     ((data['CentreEn_CentreAn'] == center1) | (data['CentreEn_CentreAn'] == center2))]
   elif (center == "Country"):
      data = data.loc[(data['Date'].between(date_min, date_max))]
   else: 
      center = "Wholesale-" + get_nearest_centre(province)
      data = data.loc[(data['Date'].between(date_min, date_max)) & (data['CentreEn_CentreAn'] == center)]

   #Get local produce
   data = data.loc[(data['region'] == region)]
   data['produce_name'] = data['CmdtyEn_PrdtAn'] + " " + data['VrtyEn_VrteAn']
   data['count'] = data.groupby(by = 'produce_name')['produce_name'].transform('count')
   data = data.sort_values(by=['count'], ascending = False)
   in_season = list(dict.fromkeys(zip(data.CmdtyEn_PrdtAn, data.VrtyEn_VrteAn)))

   print(in_season)
   return(in_season)

def in_season_main(province):
   data = pd.read_csv('Imported Data.csv')
   backlog_date_range = get_dates()
   in_season = get_in_season(data, province, backlog_date_range)


##TO RUN:
#in_season_main("Alberta")