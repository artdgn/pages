# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# + [markdown] papermill={"duration": 0.013695, "end_time": "2020-03-27T06:31:15.895652", "exception": false, "start_time": "2020-03-27T06:31:15.881957", "status": "completed"} tags=[]
# # World maps
# > Visualising projections and estimations on maps
#
# - comments: true
# - author: <a href=https://github.com/Junikab/>Junikab</a>, <a href=https://github.com/artdgn/>artdgn</a>
# - permalink: /covid-world-maps/
# - image: images/world_map.png
# - toc: false
# - sticky_rank: 1
# - hide: false
# -

# > Important: This dashboard contains the results of a predictive model that was not built by an epidimiologist.

# + papermill={"duration": 0.330834, "end_time": "2020-03-27T06:31:16.261108", "exception": false, "start_time": "2020-03-27T06:31:15.930274", "status": "completed"} tags=[]
#hide
import pandas as pd
import covid_helpers

helper = covid_helpers.OverviewData
df_all = helper.table_with_projections()
# -

#hide
df_all.columns.sort_values()

#hide_input
from IPython.display import Markdown
Markdown(f"***Based on data up to: {pd.to_datetime(helper.dt_today).date().isoformat()}***")

#hide
geo_helper = covid_helpers.GeoMap
df_geo = geo_helper.make_geo_df(df_all, cases_filter=2000, deaths_filter=20)
fig = geo_helper.make_map_figure(df_geo);

#hide
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['needICU.per100k'], 'ICU need<br>(current)', 
                    colorscale='Sunsetdark', scale_max=10,
                    subtitle='Estimated current ICU need per 100k population'),
                geo_helper.button_dict(
                    df_geo['needICU.per100k.+14d'],  'ICU need<br>(in 14 days)', 
                    colorscale='Sunsetdark', scale_max=10,
                    subtitle='Projected ICU need per 100k population in 14 days'),
                geo_helper.button_dict(
                    df_geo['needICU.per100k.+30d'],  'ICU need<br>(in 30 days)', 
                    colorscale='Sunsetdark', scale_max=10,
                    subtitle='Projected ICU need per 100k population in 30 days'),
                geo_helper.button_dict(
                    df_geo['icu_capacity_per100k'], 'ICU Capacity', colorscale='Blues',
                    subtitle='ICU capacity per 100k population'),
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True, x=0.07, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['affected_ratio.est'], 'Affected percent<br>(Current)', 
                    colorscale='Bluyl', percent=True,
                    subtitle='Estimated current affected population percentage'),
                geo_helper.button_dict(
                    df_geo['affected_ratio.est.+14d'], 'Affected percent<br>(in 14 days)', 
                    colorscale='Bluyl', scale_max=25, percent=True,
                    subtitle='Projected affected population percentage in 14 days'),
                geo_helper.button_dict(
                    df_geo['affected_ratio.est.+30d'], 'Affected percent<br>(in 30 days)', 
                    colorscale='Bluyl', scale_max=25, percent=True,
                    subtitle='Projected affected population percentage in 30 days'),
                geo_helper.button_dict(
                    df_geo['Cases.total.per100k.est'], 'Total cases<br>estimated per 100k', 
                    colorscale='YlOrRd',
                    subtitle='Estimated total cases per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.total.est'], 'Total cases<br>(estimated)', colorscale='YlOrRd',
                    subtitle='Estimated total cases'),
                geo_helper.button_dict(
                    df_geo['Cases.total.per100k'], 'Total cases<br>reported per 100k', 
                    colorscale='YlOrRd',
                    subtitle='Reported total cases per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.total'], 'Total cases<br>(reported)', colorscale='YlOrRd',
                    subtitle='Reported total cases'),
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True, x=0.24, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['infection_rate'], 'Infection rate<br>percent (blue-red)',
                    colorscale='Bluered', scale_max=10, percent=True,
                    subtitle='Infection spread rate: over 5% (red) spreading, under 5% (blue) recovering'),
                geo_helper.button_dict(
                    df_geo['infection_rate'], 'Infection rate<br>percent', 
                    colorscale='YlOrRd', scale_max=33, percent=True,
                    subtitle='Infection spread rate (related to R0)'),
                geo_helper.button_dict(
                    df_geo['Cases.new.per100k.est'], 'New cases<br>estimated per 100k', 
                    colorscale='YlOrRd',
                    subtitle='Estimated new cases in last 5 days per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.new.est'], 'New cases<br>(estimated)', 
                    colorscale='YlOrRd',
                    subtitle='Estimated new cases in last 5 days'),
                geo_helper.button_dict(
                    df_geo['Cases.new.per100k'], 'New cases<br>reported per 100k', 
                    colorscale='YlOrRd',
                    subtitle='Reported new cases in last 5 days per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.new'], 'New cases<br>(reported)', 
                    colorscale='YlOrRd',
                    subtitle='Reported new cases in last 5 days'),
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True, x=0.45, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['Deaths.total.per100k'], 'Deaths<br>per 100k', colorscale='Reds',
                    subtitle='Total deaths per 100k population'),
                geo_helper.button_dict(
                    df_geo['Deaths.total'], 'Deaths<br>Total', colorscale='Reds',
                    subtitle='Total deaths'),
                geo_helper.button_dict(
                    df_geo['Deaths.new.per100k'], 'New deaths<br>per 100k', colorscale='Reds',
                    subtitle='New deaths in last 5 days per 100k population'),
                geo_helper.button_dict(
                    df_geo['Deaths.new'], 'New deaths<br>total', colorscale='Reds',
                    subtitle='New deaths in last 5 days'),
                geo_helper.button_dict(
                    df_geo['lagged_fatality_rate'], 'Fatality rate %<br>(lagged)', 
                    colorscale='Reds', scale_max=20, percent=True,
                    subtitle='Reported fatality rate (relative to reported cases 8 days ago)'),
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True, x=0.66, xanchor="left", y=1.1, yanchor="top"),
    ])

# # World map (choose column)
# > Includes only countries with at least 2000 reported cases or at least 20 reported deaths.
#
# For details per country see [main notebook](/pages/covid-progress-projections/)

# > Tip: Select columns to show on map to from the dropdown menus. The map is zoomable and draggable.

#hide_input
from IPython.display import HTML
HTML(fig.to_html())

# ## Appendix
# <a id='appendix'></a>
# [See appendix in main notebook](/pages/covid-progress-projections/#appendix)
