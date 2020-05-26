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

# # World maps
# > Visualising projections and estimations on maps
#
# - permalink: /covid-world-maps/
# - image: images/world_map.png
# - toc: false
# - sticky_rank: 0
# - hide: false

# > Important: This dashboard contains the results of a predictive model that was not built by an epidemiologist.

# +
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
Markdown(f"***Based on data up to: {helper.cur_date}***")

#hide
geo_helper = covid_helpers.GeoMap
df_geo = geo_helper.make_geo_df(df_all, cases_filter=1000, deaths_filter=20)
fig = geo_helper.make_map_figure(df_geo)

#hide
df_geo['affected_ratio.change.monthly.rate'] = (df_geo['affected_ratio.est.+7d'] - 
                                                df_geo['affected_ratio.est']) * 30 / 7

# +
#hide
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['infection_rate'], 'Transmission rate<br>percent (blue-red)',
                    colorscale='Bluered', scale_max=10, percent=True,
                    subtitle='Transmission rate: over 5% (red) spreading, under 5% (blue) recovering',
                    err_series=df_geo['growth_rate_std']),
                geo_helper.button_dict(
                    df_geo['infection_rate'], 'Transmission rate<br>percent',
                    colorscale='YlOrRd', scale_max=33, percent=True,
                    subtitle='Transmission rate (related to R0)',
                    err_series=df_geo['growth_rate_std']),
                geo_helper.button_dict(
                    df_geo['Cases.new.per100k.est'], 'Recent cases<br>estimated per 100k',
                    colorscale='YlOrRd',
                    subtitle='Estimated recent cases in last 5 days per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.new.est'], 'Recent cases<br>(estimated)',
                    colorscale='YlOrRd',
                    subtitle='Estimated recent cases in last 5 days'),
                geo_helper.button_dict(
                    df_geo['Cases.new.per100k'], 'Recent cases<br>reported per 100k',
                    colorscale='YlOrRd',
                    subtitle='Reported recent cases in last 5 days per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.new'], 'Recent cases<br>(reported)',
                    colorscale='YlOrRd',
                    subtitle='Reported recent cases in last 5 days'),
            ],
            direction="down", bgcolor='#efe9da',
            pad={"r": 10, "t": 10},
            showactive=False, x=0.07, xanchor="left", y=1.1, yanchor="top"),            
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['affected_ratio.est'], 'Affected percent<br>(Current)', 
                    colorscale='Bluyl', percent=True,
                    subtitle='Estimated current affected population percentage'),
                geo_helper.button_dict(
                    df_geo['affected_ratio.est.+14d'], 'Affected percent<br>(in 14 days)', 
                    colorscale='Bluyl', scale_max=25, percent=True,
                    subtitle='Projected affected population percentage in 14 days',
                    err_series=df_geo['affected_ratio.est.+14d.err']),
                geo_helper.button_dict(
                    df_geo['affected_ratio.est.+30d'], 'Affected percent<br>(in 30 days)', 
                    colorscale='Bluyl', scale_max=25, percent=True,
                    subtitle='Projected affected population percentage in 30 days',
                    err_series=df_geo['affected_ratio.est.+30d.err']),
                geo_helper.button_dict(
                    df_geo['affected_ratio.change.monthly.rate'], 
                    title='Affected percent<br>montly change rate', 
                    colorscale='Bluyl', scale_max=10, percent=True,
                    subtitle='Current affected population percentage monthly change rate',
                    err_series=df_geo['affected_ratio.est.+30d.err']),
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
            direction="down", bgcolor='#dceae1',
            pad={"r": 10, "t": 10},
            showactive=False, x=0.29, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['needICU.per100k'], 'ICU need<br>(current)',
                    colorscale='Sunsetdark', scale_max=10,
                    subtitle='Estimated current ICU need per 100k population'),
                geo_helper.button_dict(
                    df_geo['needICU.per100k.+14d'],  'ICU need<br>(in 14 days)',
                    colorscale='Sunsetdark', scale_max=10,
                    subtitle='Projected ICU need per 100k population in 14 days',
                    err_series=df_geo['needICU.per100k.+14d.err']),
                geo_helper.button_dict(
                    df_geo['needICU.per100k.+30d'],  'ICU need<br>(in 30 days)',
                    colorscale='Sunsetdark', scale_max=10,
                    subtitle='Projected ICU need per 100k population in 30 days',
                    err_series=df_geo['needICU.per100k.+30d.err']),
                geo_helper.button_dict(
                    df_geo['icu_capacity_per100k'], 'Pre-COVID<br>ICU Capacity', 
                    colorscale='Blues',
                    subtitle='Pre-COVID ICU capacity per 100k population'),
            ],
            direction="down", bgcolor='#efdaee',
            pad={"r": 10, "t": 10},
            showactive=False, x=0.515, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['Deaths.total.per100k'], 'Deaths<br>per 100k', colorscale='Reds',
                    subtitle='Total deaths per 100k population'),
                geo_helper.button_dict(
                    df_geo['Deaths.total'], 'Deaths<br>Total', colorscale='Reds',
                    subtitle='Total deaths'),
                geo_helper.button_dict(
                    df_geo['Deaths.new.per100k'], 'Recent deaths<br>per 100k', colorscale='Reds',
                    subtitle='Recent deaths in last 5 days per 100k population'),
                geo_helper.button_dict(
                    df_geo['Deaths.new'], 'Recent deaths<br>total', colorscale='Reds',
                    subtitle='Recent deaths in last 5 days'),
                geo_helper.button_dict(
                    df_geo['lagged_fatality_rate'], 'Fatality rate %<br>(lagged)', 
                    colorscale='Reds', scale_max=20, percent=True,
                    subtitle='Reported fatality rate (relative to reported cases 8 days ago)'),
            ],
            direction="down", bgcolor='#efdbda',
            pad={"r": 10, "t": 10},
            showactive=False, x=0.69, xanchor="left", y=1.1, yanchor="top"),
    ]);

# + [markdown] execution={"iopub.execute_input": "2020-05-01T12:16:14.297479Z", "iopub.status.busy": "2020-05-01T12:16:14.226157Z", "iopub.status.idle": "2020-05-01T12:16:14.457572Z", "shell.execute_reply": "2020-05-01T12:16:14.457201Z"} papermill={"duration": 0.238524, "end_time": "2020-05-01T12:16:14.457650", "exception": false, "start_time": "2020-05-01T12:16:14.219126", "status": "completed"} tags=[]
# # World map (choose column)
# > Includes only countries with at least 1000 reported cases or at least 20 reported deaths.
#
# - Per country model [trajectories plots in main notebook](/pages/covid-progress-projections/#Interactive-plot-of-Model-predictions)
# - Recent cases and recent deaths refer to cases or deaths in the last 5 days.

# + execution={"iopub.execute_input": "2020-05-01T12:16:14.297479Z", "iopub.status.busy": "2020-05-01T12:16:14.226157Z", "iopub.status.idle": "2020-05-01T12:16:14.457572Z", "shell.execute_reply": "2020-05-01T12:16:14.457201Z"} papermill={"duration": 0.238524, "end_time": "2020-05-01T12:16:14.457650", "exception": false, "start_time": "2020-05-01T12:16:14.219126", "status": "completed"} tags=[]
#hide_input
# from IPython.display import HTML
# HTML(fig.to_html())
fig.show()

# + [markdown] execution={"iopub.execute_input": "2020-05-01T12:16:14.297479Z", "iopub.status.busy": "2020-05-01T12:16:14.226157Z", "iopub.status.idle": "2020-05-01T12:16:14.457572Z", "shell.execute_reply": "2020-05-01T12:16:14.457201Z"} papermill={"duration": 0.238524, "end_time": "2020-05-01T12:16:14.457650", "exception": false, "start_time": "2020-05-01T12:16:14.219126", "status": "completed"} tags=[]
# > Tip: The map is zoomable and draggable. Hover for detailed information.

# + [markdown] execution={"iopub.execute_input": "2020-05-01T12:16:14.297479Z", "iopub.status.busy": "2020-05-01T12:16:14.226157Z", "iopub.status.idle": "2020-05-01T12:16:14.457572Z", "shell.execute_reply": "2020-05-01T12:16:14.457201Z"} papermill={"duration": 0.238524, "end_time": "2020-05-01T12:16:14.457650", "exception": false, "start_time": "2020-05-01T12:16:14.219126", "status": "completed"} tags=[]
# ## Appendix
# <a id='appendix'></a>
# [See appendix in main notebook](/pages/covid-progress-projections/#appendix)
