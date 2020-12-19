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

# # Risk of deadly infection by age (unvaccinated)
# > Estimates of monthly risk of death due to infection for unvaccinated or not previosly infected. Mapped by country and age.
#
# - permalink: /micromorts/
# - image: images/micromorts.png
# - toc: false
# - sticky_rank: 0
# - hide: false

# > Important: This page contains estimations that were not calculated by an epidemiologist.

# +
#hide
import pandas as pd
try:  # using in REPL
    from . import covid_helpers
except ImportError:
    import covid_helpers

covid_data = covid_helpers.CovidData()
df_all, _, _ = covid_data.table_with_current_rates_and_ratios()
# -

#hide
df_all.columns.sort_values()

#hide_input
from IPython.display import Markdown
Markdown(f"***Based on data up to: {covid_data.cur_date}***")

#hide
df_all['monthly_infection_chance'] = (
    30 * df_all['transmission_rate'] * df_all['current_active_ratio'] /
    (1 - df_all['current_active_ratio'] - df_all['current_recovered_ratio'])
)
df_all['monthly_deadly_infection_risk'] = (
        df_all['monthly_infection_chance'] * df_all['age_adjusted_ifr'])
df_all['monthly_average_micromorts'] = df_all['monthly_deadly_infection_risk'] * 1e6

#hide
# add age specific data
ifrs = covid_helpers.AgeAdjustedData.intl_ifrs
cols = covid_helpers.AgeAdjustedData.Cols
age_ifrs = {
    '0-29': ifrs.loc[cols.o4:cols.o29].mean(),
    '30-44': ifrs.loc[cols.o34:cols.o44].mean(),
    '45-59': ifrs.loc[cols.o49:cols.o59].mean(),
    '60-64': ifrs.loc[cols.o64],
    '65-69': ifrs.loc[cols.o69],
    '70-74': ifrs.loc[cols.o74],
    '75-79': ifrs.loc[cols.o79],
    '80+': ifrs.loc[cols.o84],
}
for age_range, ifr in age_ifrs.items():
    df_all[f'monthly_micromorts_{age_range}'] = 1e6 * ifr * df_all['monthly_infection_chance']

#hide
geo_helper = covid_helpers.GeoMap
df_geo = geo_helper.make_geo_df(df_all, cases_filter=1000, deaths_filter=20)

# +
#hide
def hover_func(r: pd.Series, age_range=None):    
    if age_range is None:
        ifr, ifr_str = r['age_adjusted_ifr'], "this country's age profile"
        micromorts_col='monthly_average_micromorts'
    else:
        ifr, ifr_str = age_ifrs[age_range], f'age range {age_range}'
        micromorts_col=f'monthly_micromorts_{age_range}'
    mm = r[micromorts_col]
    return (
        f"<br>Risk of death due to <br>"
        f"one month of exposure comparable to:<br>"
        f"  - <b>{mm / 8:.0f}</b> sky diving jumps<br>"
        f"  - <b>{mm / 5:.0f}</b> scuba dives<br>"        
        f"  - <b>{mm / 430:.0f}</b> base jumping jumps<br>"
        f"  - <b>{mm / 12000:.0f}</b> Everest climbs<br>"
        f"  - <b>{mm * 10:.0f}</b> km by Motorcycle<br>"
        f"  - <b>{mm * 370:.0f}</b> km by Car<br>"
        f"  - <b>{mm * 1600:.0f}</b> km by Plane<br><br>"
        f"Chance of infection today:<br>"
        f"  <b>{r['monthly_infection_chance']:.1%}</b> over a month<br>"
        f"Chance of death after infection:<br>"
        f"  <b>{ifr:.2%}</b> for {ifr_str}"
    )

def hover_texts_for_age_range(age_range):
    return df_geo.apply(hover_func, axis=1, age_range=age_range).tolist()


# -

#hide
colorscale = 'RdPu'
fig = geo_helper.make_map_figure(df_geo,
                                 col='monthly_average_micromorts',
                                 title='Micromorts',
                                 subtitle="Risk of deadly infection due to a month's exposure",
                                 hover_text_func=hover_func,
                                 scale_max=None,
                                 colorscale=colorscale,
                                 err_col=None,
                                )

#hide
max_micromorts = df_geo[f'monthly_micromorts_80+'].max()
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                geo_helper.button_dict(
                    df_geo['monthly_average_micromorts'],
                    title='Average monthly risk in micromorts',
                    colorbar_title='Micromorts',
                    colorscale=colorscale, scale_max=None, percent=False,
                    subtitle="Risk of deadly infection due to a month's exposure",
                    err_series=None,
                    hover_text_list=hover_texts_for_age_range(None)
                ),
            ] + [
                geo_helper.button_dict(
                    df_geo[f'monthly_micromorts_{age_range}'],
                    title=f'Ages {age_range} monthly risk in micromorts',
                    colorbar_title='Micromorts',
                    colorscale=colorscale, scale_max=max_micromorts, percent=False,
                    subtitle=f"Ages {age_range}: risk of deadly infection due to a month's exposure",
                    err_series=None,
                    hover_text_list=hover_texts_for_age_range(age_range)
                ) 
                for age_range in reversed(list(age_ifrs.keys()))
            ] + [
                geo_helper.button_dict(
                    df_geo['monthly_infection_chance'],
                    title='Monthly infection chance',
                    colorbar_title='%',
                    colorscale='Reds', scale_max=None, percent=True,
                    subtitle="Chance of being infected during a month's exposure",
                    err_series=None, 
                    hover_text_list=['' for _ in range(len(df_geo))]
                )
            ],
            direction="down", bgcolor='#dceae1',
            pad={"t": 10},
            showactive=True, x=0.1, xanchor="left", y=1.1, yanchor="top"),
    ]);

# ### Use dropdown menu to select specific age range
# > <font size=2>- Hover the mouse over a country for a risk comparison to some sports and travel modes.<br>- <a href="https://en.wikipedia.org/wiki/Micromort">"Micromorts"</a> are a measure of risk of death.<br>- Risk of death calculated for the unvaccinated or not previosly infected. </font>

#hide_input
# from IPython.display import HTML
# HTML(fig.to_html())
fig.show()

# > Tip: The map is zoomable and draggable. Double click to reset.

# ### Appendix
# <a id='appendix'></a>
# - TODO explanation about how it is calculated + citations of papers
# - TODO estimates assume average exposure for the population of that country, protective measures and self isolation should of course reduce the risk.
# - TODO Vaccination risk reduction
# - Per country model [trajectories plots in main notebook](/pages/covid-progress-projections/#Interactive-plot-of-Model-predictions)
#
# [See estimations appendix in main notebook](/pages/covid-progress-projections/#appendix)
