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

# # News (bad vs. good)
# > Signigicant changes since 10 days ago in transmission rates, ICU demand, and case / deaths data.
#
# - permalink: /covid-news/
# - toc: true
# - image: images/news.png
# - sticky_rank: 0
# - hide: false

# > Note: For per country details, projections, and for methodology see [main notebook](/pages/covid-progress-projections/)

# +
#hide
import pandas as pd
try:  # using in REPL
    from . import covid_helpers
except ImportError:
    import covid_helpers

stylers = covid_helpers.PandasStyling

# +
#hide
day_diff = 10

cur_data = covid_helpers.CovidData()
df_cur = cur_data.rename_long_names(cur_data.filter_df(cur_data.table_with_projections()))

past_data = covid_helpers.CovidData(-day_diff)
df_past = past_data.rename_long_names(past_data.filter_df(past_data.table_with_projections()))
# -

#hide_input
from IPython.display import Markdown
past_date = pd.to_datetime(past_data.dt_cols[-1]).date().isoformat()
Markdown(f"***Based on data up to: {cur_data.cur_date}. \
            Compared to ({day_diff} days before): {past_date}***")


#hide
df_data = df_cur.copy()
df_data['infection_rate_past'] = df_past['infection_rate']
df_data['infection_rate_past_err'] = df_past['growth_rate_std']
df_data['needICU.per100k_past'] = df_past['needICU.per100k']


# +
#hide
def large_index(df):
    df = df.copy()
    df.index = df.index.to_series().apply(lambda s: f'<font size=3><b>{s}</b></font>')
    return df

def style_news_infections(df):
    cols = {
        'Cases.new.est': 'Estimated <br> <i>recent</i> cases <br> in last 5 days',
        'infection_rate': '<i>Current:</i><br>Estimated<br>daily<br>transmission<br>rate',
        'infection_rate_past': f'<i>{day_diff} days ago:</i><br>Estimated<br>daily<br>transmission<br>rate',
        'needICU.per100k': 'Estimated<br>current<br>ICU need<br>per 100k<br>population',
        'affected_ratio.est': 'Estimated <br><i>total</i><br>affected<br>population<br>percentage',
      }
    
    rate_norm = max(df['infection_rate'].max(), df['infection_rate_past'].max())
    return (large_index(df)[cols.keys()].rename(columns=cols).style
        .bar(subset=[cols['needICU.per100k']], color='#b21e3e', vmin=0, vmax=10)
        .bar(subset=cols['Cases.new.est'], color='#b57b17')
        .bar(subset=cols['affected_ratio.est'], color='#5dad64', vmin=0, vmax=1.0)
        .apply(stylers.add_bar, color='#f49d5a',
               s_v=df['infection_rate']/rate_norm, subset=cols['infection_rate'])
        .apply(stylers.add_bar, color='#d8b193',
               s_v=df['infection_rate_past']/rate_norm, subset=cols['infection_rate_past'])
        .format('<b>{:.2f}</b>', subset=[cols['needICU.per100k']])
        .format('<b>{:,.0f}</b>', subset=cols['Cases.new.est'])
        .format('<b>{:.1%}</b>', subset=[cols['affected_ratio.est'], 
                                         cols['infection_rate'],
                                         cols['infection_rate_past']], na_rep="-"))
        
def style_news_icu(df):
    cols = {
        'Cases.new.est': 'Estimated<br><i>recent</i>cases<br> in last 5 days',
        'needICU.per100k': '<i>Current:</i><br>Estimated<br>ICU need<br>per 100k<br>population',
        'needICU.per100k_past': f'<i>{day_diff} days ago:</i><br>Estimated<br>ICU need<br>per 100k<br>population',
        'infection_rate': 'Estimated<br>daily<br>transmission<br>rate',
        'affected_ratio.est': 'Estimated <br><i>total</i><br>affected<br>population<br>percentage',
      }
    
    return (large_index(df)[cols.keys()].rename(columns=cols).style
        .bar(subset=cols['needICU.per100k'], color='#b21e3e', vmin=0, vmax=10)
        .bar(subset=cols['needICU.per100k_past'], color='#c67f8e', vmin=0, vmax=10)
        .bar(subset=cols['Cases.new.est'], color='#b57b17')
        .bar(subset=cols['affected_ratio.est'], color='#5dad64', vmin=0, vmax=1.0)
        .apply(stylers.add_bar, color='#f49d5a',
               s_v=df['infection_rate']/df['infection_rate'].max(), 
               subset=cols['infection_rate'])
        .format('<b>{:.2f}</b>', subset=[cols['needICU.per100k'], cols['needICU.per100k_past']])
        .format('<b>{:,.0f}</b>', subset=cols['Cases.new.est'])
        .format('<b>{:.1%}</b>', subset=[cols['affected_ratio.est'], 
                                         cols['infection_rate']]))

def style_basic(df):
    cols = {
        'Cases.total.est': 'Estimated<br>total<br>cases',
        'Deaths.total': 'Total<br>reported<br>deaths'
      }  
    return (large_index(df)[cols.keys()].rename(columns=cols).style
        .format('<b>{:,.0f}</b>', subset=[cols['Cases.total.est'], cols['Deaths.total']]))


# -

# # Transmission rate:

# ## Bad news: new waves
# > Large increase in transmission rate vs. 10 days ago, that might mean a relapse, new wave, worsening outbreak. 
#
# - Countries are sorted by size of change in tranmission rate.
# - Includes only countries that were previously active (more than 100 estimated new cases).
# - "Large increase" = at least +1% change.

#hide_input
rate_diff = df_cur['infection_rate'] - df_past['infection_rate']
pct_rate_diff = rate_diff / df_past['growth_rate_std']
higher_trans = ((df_cur['infection_rate'] > 0.02) & 
        (df_cur['Cases.new.est'] > 100) &
        (rate_diff > 0.01) &
        (pct_rate_diff > 3))
new_outbreaks = rate_diff[higher_trans].sort_values(ascending=False).index
style_news_infections(df_data.loc[new_outbreaks])

# ## Good news: slowing waves
# > Large decrease in transmission rate vs. 10 days ago, that might mean a slowing down / effective control measures.
#
# - Countries are sorted by size of change in tranmission rate.
# - Includes only countries that were previously active (more than 100 estimated new cases).
# - "Large decrease" = at least -1% change.

#hide_input
lower_trans = ((df_cur['infection_rate'] > 0.02) & 
        (df_cur['Cases.new.est'] > 100) &
        (rate_diff < -0.01) &
        (pct_rate_diff < -3))
slowing_outbreaks = rate_diff[lower_trans].sort_values().index
style_news_infections(df_data.loc[slowing_outbreaks])

# # ICU need

# ## Bad news: higher ICU need
# > Large increases in need for ICU beds per 100k population vs. 10 days ago.
#
# - Only countries for which the ICU need increased by more than 0.5 (per 100k).

#hide_input
icu_diff = df_cur['needICU.per100k'] - df_past['needICU.per100k']
icu_increase = icu_diff[icu_diff > 0.5].sort_values(ascending=False).index
style_news_icu(df_data.loc[icu_increase])

# ## Good news: lower ICU need
# > Large decreases in need for ICU beds per 100k population vs. 10 days ago.
#
# - Only countries for which the ICU need decreased by more than 0.5 (per 100k).

#hide_input
icu_decrease = icu_diff[icu_diff < -0.5].sort_values().index
style_news_icu(df_data.loc[icu_decrease])

# # Cases and deaths

# ## Bad news: new first outbreaks
# > Countries that have started their first outbreak (crossed 1000 total reported cases or 20 deaths) vs. 10 days ago.

#hide_input
new_entries = df_cur.index[~df_cur.index.isin(df_past.index)]
style_news_infections(df_data.loc[new_entries])

# ## Good news: no new cases or deaths
# > New countries with no new cases or deaths vs. 10 days ago.
#
# - Only considering countries that had at least 1000 estimated total cases and at least 10 total deaths and had and active outbreak previously.

# +
#hide_input
significant_past = ((df_past['Cases.total.est'] > 1000) & (df_past['Deaths.total'] > 10))
active_in_past = ((df_past['Cases.new'] > 0) | (df_past['Deaths.new'] > 0))
no_cases_filt = ((df_cur['Cases.total'] - df_past['Cases.total']) == 0)
no_deaths_filt = ((df_cur['Deaths.total'] - df_past['Deaths.total']) == 0)
no_cases_and_deaths = df_cur.loc[no_cases_filt & no_deaths_filt & 
                                 significant_past & active_in_past].index

# style_news_table(df_pretty.loc[no_cases_and_deaths], df_data.loc[no_cases_and_deaths])
style_basic(df_data.loc[no_cases_and_deaths])
# -

# ## Mixed news: no new deaths, only new cases
# > New countries with no new deaths (only new cases) vs. 10 days ago.
#
# - Only considering countries that had at least 1000 estimated total cases and at least 10 total deaths and had an active outbreak previously.

#hide_input
no_deaths = df_cur.loc[no_deaths_filt & (~no_cases_filt) & 
                       significant_past & active_in_past].index
style_news_infections(df_data.loc[no_deaths])

# ## No news: continously inactive countries
# > Countries that have been inactive continuously previously (10 days ago), and still are now.
#
# - Only considering countries that had at least 1000 estimated total cases and at least 10 total deaths.
# - These countries may have stopped reporting data like [Tanzania](https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Tanzania).

#hide_input
not_active = df_cur.loc[no_cases_filt & significant_past & ~active_in_past].index
style_basic(df_data.loc[not_active])
