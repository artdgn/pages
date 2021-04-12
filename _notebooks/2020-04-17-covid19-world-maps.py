# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
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

covid_data = covid_helpers.CovidData()
df_all = covid_data.table_with_projections()
# -

#hide
df_all.columns.sort_values()

#hide_input
from IPython.display import Markdown
Markdown(f"*Based on data up to*: ***{covid_data.cur_date}***")

#hide
geo_helper = covid_helpers.GeoMap
df_geo = geo_helper.make_geo_df(df_all, cases_filter=1000, deaths_filter=20)
def hover_text_func(r: pd.Series):
    return (
        "<br>"
        f"Cases (reported): {r['Cases.total']:,.0f} (+<b>{r['Cases.new']:,.0f}</b>)<br>"
        f"Cases (estimated): {r['Cases.total.est']:,.0f} (+<b>{r['Cases.new.est']:,.0f}</b>)<br>"
        f"Affected percent: <b>{r['affected_ratio.est']:.1%}</b><br>"
        f"Transmission rate: <b>{r['transmission_rate']:.1%}</b> ± {r['transmission_rate_std']:.1%}<br>"
        f"Deaths: {r['Deaths.total']:,.0f} (+<b>{r['Deaths.new']:,.0f}</b>)<br>"
    )
fig = geo_helper.make_map_figure(
    df_geo,
    col='transmission_rate',
    err_col='transmission_rate_std',
    colorbar_title='%',
    subtitle='Transmission rate: red spreading (>5%), blue recovering (<5%)',
    hover_text_func=hover_text_func,
    scale_max=10,
    colorscale='Bluered',
)

#hide
df_geo['affected_ratio.change.monthly.rate'] = (df_geo['affected_ratio.est.+7d'] - 
                                                df_geo['affected_ratio.est']) * 30 / 7
df_geo['icu_estimation_error'] = df_geo['needICU.per100k'] / df_geo['owid_icu_per_100k']

#hide
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['transmission_rate'], 'Transmission rate<br>percent (blue-red)',
                    colorscale='Bluered', scale_max=10, percent=True,
                    subtitle='Transmission rate: red spreading (>5%), blue recovering (<5%)',
                    colorbar_title='%',
                    err_series=df_geo['transmission_rate_std']),
                geo_helper.button_dict(
                    df_geo['transmission_rate'], 'Transmission rate<br>percent',
                    colorscale='YlOrRd', scale_max=33, percent=True,
                    subtitle='Transmission rate (related to R0)',
                    colorbar_title='%',
                    err_series=df_geo['transmission_rate_std']),
                geo_helper.button_dict(
                    df_geo['Cases.new.per100k.est'], 'Recent cases<br>estimated per 100k',
                    colorscale='YlOrRd',
                    colorbar_title='Cases / 100k',
                    subtitle='Estimated recent cases in last 5 days per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.new.est'], 'Recent cases<br>(estimated)',
                    colorscale='YlOrRd',
                    colorbar_title='Cases',
                    subtitle='Estimated recent cases in last 5 days'),
                geo_helper.button_dict(
                    df_geo['Cases.new.per100k'], 'Recent cases<br>reported per 100k',
                    colorscale='YlOrRd',
                    colorbar_title='Cases / 100k',
                    subtitle='Reported recent cases in last 5 days per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.new'], 'Recent cases<br>(reported)',
                    colorscale='YlOrRd',
                    colorbar_title='Cases',
                    subtitle='Reported recent cases in last 5 days'),
            ],
            direction="down", bgcolor='#efe9da',
            pad={"r": 10, "t": 10},
            showactive=False, x=0.07, xanchor="left", y=1.1, yanchor="top"),            
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['owid_full_vaccinated_ratio'], 'Vaccinated (fully)<br>percent',
                    colorscale='Blues', scale_max=None, percent=True,
                    colorbar_title='%',
                    subtitle='Latest reported percent fully vaccinated (OWID)'),
                geo_helper.button_dict(
                    df_geo['owid_part_vaccinated_ratio'], 'Vaccinated (all)<br>percent',
                    colorscale='Blues', scale_max=None, percent=True,
                    colorbar_title='%',
                    subtitle='Latest reported percent vaccinated fully or partially (OWID)'),
                geo_helper.button_dict(
                    df_geo['owid_total_vaccinations_ratio'], 'Vaccination doses<br>percent',
                    colorscale='Blues', scale_max=None, percent=True,
                    colorbar_title='%',
                    subtitle='Latest reported percent administered vaccine doses per population (OWID)'),
                geo_helper.button_dict(
                    df_geo['affected_ratio.est'], 'Affected percent<br>(Current)',
                    colorscale='Bluyl', percent=True,
                    colorbar_title='%',
                    subtitle='Estimated current affected population percentage'),
                geo_helper.button_dict(
                    df_geo['affected_ratio.est.+14d'], 'Affected percent<br>(in 14 days)', 
                    colorscale='Bluyl', scale_max=25, percent=True,
                    colorbar_title='%',
                    subtitle='Projected affected population percentage in 14 days',
                    err_series=df_geo['affected_ratio.est.+14d.err']),
                geo_helper.button_dict(
                    df_geo['affected_ratio.est.+30d'], 'Affected percent<br>(in 30 days)', 
                    colorscale='Bluyl', scale_max=25, percent=True,
                    colorbar_title='%',
                    subtitle='Projected affected population percentage in 30 days',
                    err_series=df_geo['affected_ratio.est.+30d.err']),
                geo_helper.button_dict(
                    df_geo['affected_ratio.change.monthly.rate'], 
                    title='Affected percent<br>montly change rate', 
                    colorscale='Bluyl', scale_max=10, percent=True,
                    colorbar_title='% per month',
                    subtitle='Current affected population percentage monthly change rate',
                    err_series=df_geo['affected_ratio.est.+30d.err']),
                geo_helper.button_dict(
                    df_geo['Cases.total.per100k.est'], 'Total cases<br>estimated per 100k', 
                    colorscale='YlOrRd',
                    colorbar_title='Cases / 100k',
                    subtitle='Estimated total cases per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.total.est'], 'Total cases<br>(estimated)', colorscale='YlOrRd',
                    colorbar_title='Cases',
                    subtitle='Estimated total cases'),
                geo_helper.button_dict(
                    df_geo['Cases.total.per100k'], 'Total cases<br>reported per 100k', 
                    colorscale='YlOrRd',
                    colorbar_title='Cases / 100k',
                    subtitle='Reported total cases per 100k population'),
                geo_helper.button_dict(
                    df_geo['Cases.total'], 'Total cases<br>(reported)', colorscale='YlOrRd',
                    colorbar_title='Cases',
                    subtitle='Reported total cases'),
            ],
            direction="down", bgcolor='#dceae1',
            pad={"r": 10, "t": 10},
            showactive=False, x=0.305, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['needICU.per100k'], 'ICU need<br>(estimated)',
                    colorscale='Sunsetdark', scale_max=10,
                    colorbar_title='ICU beds / 100k',
                    subtitle='Estimated current ICU need per 100k population'),
                geo_helper.button_dict(
                    df_geo['owid_icu_per_100k'], 'ICU need<br>(reported)',
                    colorscale='Sunsetdark', scale_max=10,
                    colorbar_title='ICU beds / 100k',
                    subtitle='Latest reported ICU need per 100k population (OWID)'),
                geo_helper.button_dict(
                    df_geo['icu_estimation_error'], 'ICU estimation<br>error',
                    colorscale='Bluered', scale_max=200, percent=True,
                    colorbar_title='%',
                    subtitle='Ratio between estimated and latest reported ICU need as %'),
                geo_helper.button_dict(
                    df_geo['needICU.per100k.+14d'],  'ICU need<br>(in 14 days)',
                    colorscale='Sunsetdark', scale_max=10,
                    colorbar_title='ICU beds / 100k',
                    subtitle='Projected ICU need per 100k population in 14 days',
                    err_series=df_geo['needICU.per100k.+14d.err']),
                geo_helper.button_dict(
                    df_geo['needICU.per100k.+30d'],  'ICU need<br>(in 30 days)',
                    colorscale='Sunsetdark', scale_max=10,
                    colorbar_title='ICU beds / 100k',
                    subtitle='Projected ICU need per 100k population in 30 days',
                    err_series=df_geo['needICU.per100k.+30d.err']),
                geo_helper.button_dict(
                    df_geo['icu_capacity_per100k'], 'Pre-COVID<br>ICU Capacity', 
                    colorbar_title='ICU beds / 100k',
                    colorscale='Blues',
                    subtitle='Pre-COVID ICU capacity per 100k population'),
            ],
            direction="down", bgcolor='#efdaee',
            pad={"r": 10, "t": 10},
            showactive=False, x=0.54, xanchor="left", y=1.1, yanchor="top"),
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['Deaths.total.per100k'], 'Deaths<br>per 100k', colorscale='Reds',
                    colorbar_title='Deaths / 100k',
                    subtitle='Total deaths per 100k population'),
                geo_helper.button_dict(
                    df_geo['Deaths.total'], 'Deaths<br>Total', colorscale='Reds',
                    colorbar_title='Deaths',
                    subtitle='Total deaths'),
                geo_helper.button_dict(
                    df_geo['Deaths.new.per100k'], 'Recent deaths<br>per 100k', colorscale='Reds',
                    colorbar_title='Deaths / 100k',
                    subtitle='Recent deaths in last 5 days per 100k population'),
                geo_helper.button_dict(
                    df_geo['Deaths.new'], 'Recent deaths<br>total', colorscale='Reds',
                    colorbar_title='Deaths',
                    subtitle='Recent deaths in last 5 days'),
                geo_helper.button_dict(
                    df_geo['current_testing_bias'], 'Current testing<br>bias',
                    colorscale='YlOrRd', scale_max=20, percent=False,
                    colorbar_title='Testing bias',
                    subtitle='Current testing bias'),
            ],
            direction="down", bgcolor='#efdbda',
            pad={"r": 10, "t": 10},
            showactive=False, x=0.715, xanchor="left", y=1.1, yanchor="top"),
    ]);

# + [markdown] execution={"iopub.execute_input": "2020-05-01T12:16:14.297479Z", "iopub.status.busy": "2020-05-01T12:16:14.226157Z", "iopub.status.idle": "2020-05-01T12:16:14.457572Z", "shell.execute_reply": "2020-05-01T12:16:14.457201Z"} papermill={"duration": 0.238524, "end_time": "2020-05-01T12:16:14.457650", "exception": false, "start_time": "2020-05-01T12:16:14.219126", "status": "completed"} tags=[]
# # World map (choose column)
# > Hover mouse over map for detailed information.
#
# - Per country model [trajectories plots in main notebook](/pages/covid-progress-projections/#Interactive-plot-of-Model-predictions)
# - Recent cases and recent deaths refer to cases or deaths in the last 5 days.

# + execution={"iopub.execute_input": "2020-05-01T12:16:14.297479Z", "iopub.status.busy": "2020-05-01T12:16:14.226157Z", "iopub.status.idle": "2020-05-01T12:16:14.457572Z", "shell.execute_reply": "2020-05-01T12:16:14.457201Z"} papermill={"duration": 0.238524, "end_time": "2020-05-01T12:16:14.457650", "exception": false, "start_time": "2020-05-01T12:16:14.219126", "status": "completed"} tags=[]
#hide_input
# from IPython.display import HTML
# HTML(fig.to_html())
fig.show()

# + [markdown] execution={"iopub.execute_input": "2020-05-01T12:16:14.297479Z", "iopub.status.busy": "2020-05-01T12:16:14.226157Z", "iopub.status.idle": "2020-05-01T12:16:14.457572Z", "shell.execute_reply": "2020-05-01T12:16:14.457201Z"} papermill={"duration": 0.238524, "end_time": "2020-05-01T12:16:14.457650", "exception": false, "start_time": "2020-05-01T12:16:14.219126", "status": "completed"} tags=[]
# > Tip: The map is zoomable and draggable. Double click to reset.

# + [markdown] execution={"iopub.execute_input": "2020-05-01T12:16:14.297479Z", "iopub.status.busy": "2020-05-01T12:16:14.226157Z", "iopub.status.idle": "2020-05-01T12:16:14.457572Z", "shell.execute_reply": "2020-05-01T12:16:14.457201Z"} papermill={"duration": 0.238524, "end_time": "2020-05-01T12:16:14.457650", "exception": false, "start_time": "2020-05-01T12:16:14.219126", "status": "completed"} tags=[]
# ## Appendix
# <a id='appendix'></a>
# [See appendix in main notebook](/pages/covid-progress-projections/#appendix)
