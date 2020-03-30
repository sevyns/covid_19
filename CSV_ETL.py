import pandas as pd

## Data source from hosted source - see paths
## Data Repo location: https://github.com/CSSEGISandData/COVID-19

rd_conf_path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
rd_death_path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
rd_recovered_path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'


csv_local_write_path = 'covid_19_complete.csv'
rdc = pd.read_csv(rd_conf_path)
rdd = pd.read_csv(rd_death_path)
rdr = pd.read_csv(rd_recovered_path)

rdc_dates = rdc.columns[4:]
rdd_dates = rdd.columns[4:]
rdr_dates = rdr.columns[4:]

# Reshape and concat
conf_df_long = rdc.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],value_vars=rdc_dates, var_name='Date', value_name='Confirmed')
deaths_df_long = rdd.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=rdd_dates, var_name='Date', value_name='Deaths')
recv_df_long = rdr.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],  value_vars=rdr_dates, var_name='Date', value_name='Recovered')
full_table = pd.concat([conf_df_long, deaths_df_long['Deaths'], recv_df_long['Recovered']],axis=1, sort=False)
full_table.head()

#Rename columns
full_table.columns = ['StateProvince','RegionCountry','Lat','Long','Date','Confirmed','Deaths','Recovered']
full_table.columns
full_table.groupby(['StateProvince'],as_index=False).agg({'Date':'count'})

# Write Results
full_table.to_csv (csv_local_write_path, index=False)

# Logic below from https://github.com/imdevskp/covid_19_jhu_data_web_scrap_and_cleaning/blob/master/data_cleaning.ipynb
# removing county wise data to avoid double counting
## Not sure about this logic... commenting out for now
# full_table = full_table[full_table['Province/State'].str.contains(',')!=True]
# In [9]:
# full_table.to_csv('covid_19_clean_complete.csv', index=False)