import pandas as pd
import plotly.graph_objs as go
import numpy as np
from collections import OrderedDict
import requests

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

# Excluding China and India.
asian_countries = OrderedDict([('Cambodia', 'KHM'), ('Hong Kong', 'HKG'), ('Indonesia', 'IDN'), ('Japan', 'JPN'), ('Laos', 'LAO'),
                              ('Malaysia', 'MYS'), ('Myanmar', 'MMR'), ('Nepal', 'NPL'), ('Philippines', 'PHL'), ('Singapore', 'SGP'),
                              ('Taiwan', 'TWN'), ('Thailand', 'THA'), ('Vietnam', 'VNM')])

def return_figures(countries=asian_countries):
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    # Set asian_countries as default.
    if not bool(countries):
      countries = asian_countries
    
    # Format country codes to use in url address.
    country_codes = list(countries.values())
    country_codes = [x.lower() for x in country_codes]
    country_codes = ':'.join(country_codes)    
    
    # World Bank trade-related indicators.
    # TX.VAL.MRCH.XD.WD = Export value index (2000 = 100)
    # IC.EXP.CSBC.CD = Cost of export
    # GC.TAX.EXPT.ZS = Taxes on exports (% of tax revenue)
    # BN.GSR.GNFS.CD = Net export (BoP)
    indicators = ['TX.VAL.MRCH.XD.WD ', 'IC.EXP.CSBC.CD', 'GC.TAX.EXPT.ZS', ' BN.GSR.GNFS.CD']
    
    data_frames = []
    urls = []

    for indicator in indicators:
      url = 'http://api.worldbank/org/v2/countries/' + country_codes + '/indicators/' + indicator + '?date=2000:2018&per_page=1000&format=json'
      urls.append(url)

      try:
        r = requests.get(url)
        data=r.json()[1]
      except:
        print('Could not load data ', indicator)
      
      for idx, value in enumerate(data):
        value['indicator'] = value['indicator']['value']
        value['country'] = value['country']['value']
      
      data_frames.append(data)

    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    
    graph_one = []
    df_one = pd.DataFrame(data_frames[0])
    df_one.columns = ['country', 'year', 'export_value_idx']
    country_list = df_one['country'].unique().tolist()

    for country in country_list:
      x_val = df_one[df_one['country'] == country].year.tolist()
      y_val = df_one[df_one['country'] == country].export_value_idx.tolist()
      graph_one.append(
        go.Scatter(
        x = x_val,
        y = y_val,
        mode = 'lines',
        name = country
        )
      )

    layout_one = dict(title = 'Annual Export Value Trend',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Export Value Index (2000 = 100)'),
                )

# second chart plots 2018 cost to export by country.   
    graph_two = []
    df_two = pd.DataFrame(data_frames[1])
    df_two.columns = ['country', 'year', 'cost_of_export_usd']
    df_two = df_two[df_two['year'] == 2018]
    
    x_val = df_two['country'].unique().tolist()
    y_val = df_two['cost_of_export_usd'] 

    graph_two.append(
      go.Bar(
      x = x_val,
      y = y_val,
      )
    )

    layout_two = dict(title = '2018 Cost of Exports in U.S. Dollars',
                xaxis = dict(title = 'Country',),
                yaxis = dict(title = 'USD'),
                )


# third chart plots 2018 taxes on export as percentage of revenue
    graph_three = []
    df_three = pd.DataFrame(data_frames[2])
    df_threee.columns = ['country', 'year', 'export_taxes']
    df_three = df_three[df_three['year'] == 2018]
    
    x_val = df_three['country'].unique().tolist()
    y_val = df_three['export_taxes']
    graph_three.append(
      go.Scatter(
      x = x_val,
      y = y_val,
      mode = 'bars'
      )
    )

    layout_three = dict(title = '2018 Export Taxes as Percentage of Sales',
    
                xaxis = dict(title = 'Country'),
                yaxis = dict(title = '% - Revenue')
                       )
    

for country in country_list:
    x_val = df_one[df_one['country'] == country].year.tolist()
    y_val = df_one[df_one['country'] == country].export_value_idx.tolist()

# fourth chart shows annual trend of balance of payments (net exports) for each country
    graph_four = []
    df_four = pd.DataFrame(data_frames[3])
    df_four.columns = ['country', 'year', 'bal_of_pmts']
    
    for country in country_list:
      x_val = df_four[df_four['country'] == country].year.tolist()
      y_val = df_four[df_four['country'] == country].bal_of_pmts.tolist()
      graph_four.append(
        go.Scatter(
        x = x_val,
        y = y_val,
        mode = 'lines'
        )
      )

    layout_four = dict(title = 'Chart Four',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures
