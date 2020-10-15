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

# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []

    graph_two.append(
      go.Bar(
      x = ['a', 'b', 'c', 'd', 'e'],
      y = [12, 9, 7, 5, 1],
      )
    )

    layout_two = dict(title = 'Chart Two',
                xaxis = dict(title = 'x-axis label',),
                yaxis = dict(title = 'y-axis label'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    graph_three.append(
      go.Scatter(
      x = [5, 4, 3, 2, 1, 0],
      y = [0, 2, 4, 6, 8, 10],
      mode = 'lines'
      )
    )

    layout_three = dict(title = 'Chart Three',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label')
                       )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    
    graph_four.append(
      go.Scatter(
      x = [20, 40, 60, 80],
      y = [10, 20, 30, 40],
      mode = 'markers'
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
