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

# # World News from data (good & bad)
# > Significant changes vs. 10 days ago in transmission rates, ICU demand, and cases & deaths data.
#
# - permalink: /covid-news/
# - toc: true
# - image: images/news.png
# - sticky_rank: 0
# - hide: false

# > Note: For per country details projections, and for methodology see [main notebook](/pages/covid-progress-projections/)

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
df_cur_all, debug_dfs = cur_data.table_with_projections(projection_days=[30], debug_dfs=True)
df_cur = cur_data.filter_df(df_cur_all)

past_data = covid_helpers.CovidData(-day_diff)
df_past = past_data.filter_df(past_data.table_with_projections(projection_days=[day_diff-1]))
# -

#hide_input
from IPython.display import Markdown
past_date = pd.to_datetime(past_data.dt_cols[-1]).date().isoformat()
Markdown(f"***Based on data up to: {cur_data.cur_date}. \
            Compared to ({day_diff} days before): {past_date}***")


# +
#hide
df_data = df_cur.copy()
df_data['transmission_rate_past'] = df_past['transmission_rate']
df_data['transmission_rate_std_past'] = df_past['transmission_rate_std']
df_data['needICU.per100k_past'] = df_past['needICU.per100k']

# deaths toll changes
df_data['Deaths.total.diff'] = df_data['Deaths.total'] - df_past['Deaths.total']
df_data['Deaths.new.per100k.past'] = df_past['Deaths.new.per100k']
df_data['Deaths.new.past'] = df_past['Deaths.new']
df_data['Deaths.diff.per100k'] = df_data['Deaths.total.diff'] / (df_data['population'] / 1e5)

# misses and explanations
df_data['transmission_rate.change'] = (df_data['transmission_rate'] / df_data['transmission_rate_past']) - 1
df_data['affected_ratio.miss'] = (df_cur['affected_ratio.est'] / df_past['affected_ratio.est.+9d']) - 1
df_data['needICU.per100k.miss'] = (df_cur['needICU.per100k'] / df_past['needICU.per100k.+9d']) - 1
df_data['testing_bias.change'] = (df_data['testing_bias'] / df_past['testing_bias']) - 1


# +
#hide
def index_format(df):
    df = cur_data.rename_long_names(df)
    df.index = df.apply(
        lambda s: f"""<font size=3><b>{s['emoji_flag']} {s.name}</b></font>""", axis=1)
    return df

def emoji_flags(inds):
    return ' '.join(df_cur.loc[inds]['emoji_flag'])


# -

# # Transmission rate:

#hide
def style_news_infections(df):
    cols = {        
        'transmission_rate': '<i>Current:</i><br>Estimated<br>daily<br>transmission<br>rate',
        'transmission_rate_past': f'<i>{day_diff} days ago:</i><br>Estimated<br>daily<br>transmission<br>rate',
        'Cases.new.est': 'Estimated <br> <i>recent</i> cases <br> in last 5 days',
        'needICU.per100k': 'Estimated<br>current<br>ICU need<br>per 100k<br>population',
        'affected_ratio.est': 'Estimated <br><i>total</i><br>affected<br>population<br>percentage',
      }
    
    rate_norm = max(df['transmission_rate'].max(), df['transmission_rate_past'].max())
    return (index_format(df)[cols.keys()].rename(columns=cols).style
        .bar(subset=[cols['needICU.per100k']], color='#b21e3e', vmin=0, vmax=10)
        .bar(subset=cols['Cases.new.est'], color='#b57b17', vmin=0)
        .bar(subset=cols['affected_ratio.est'], color='#5dad64', vmin=0, vmax=1.0)
        .apply(stylers.add_bar, color='#f49d5a',
               s_v=df['transmission_rate']/rate_norm, subset=cols['transmission_rate'])
        .apply(stylers.add_bar, color='#d8b193',
               s_v=df['transmission_rate_past']/rate_norm, subset=cols['transmission_rate_past'])
        .format('<b>{:.2f}</b>', subset=[cols['needICU.per100k']])
        .format('<b>{:,.0f}</b>', subset=cols['Cases.new.est'])
        .format('<b>{:.1%}</b>', subset=[cols['affected_ratio.est'], 
                                         cols['transmission_rate'],
                                         cols['transmission_rate_past']], na_rep="-"))


#hide
# optimistic rates
rate_diff = df_data['transmission_rate'] - df_data['transmission_rate_past']
higher_trans = (
        (df_data['Cases.new.est'] > 100) &
        (rate_diff > 0.02) &
        (rate_diff > df_data['transmission_rate_std_past']) &
        (df_data['transmission_rate_past'] != 0)  # countries reporting infrequently
)
new_waves = rate_diff[higher_trans].sort_values(ascending=False).index

#hide_input
Markdown(f"## &#11093; Bad news: new waves {emoji_flags(new_waves)}")

# > Large increase in transmission rate vs. 10 days ago, that might mean a relapse, new wave, worsening outbreak.
#
# - Countries are sorted by size of change in transmission rate.
# - Includes only countries that were previously active (more than 100 estimated new cases).
# - "Large increase" = at least +2%.

#hide_input
style_news_infections(df_data.loc[new_waves])

#hide
df_alt_all = pd.concat([d.reset_index() for d in debug_dfs], axis=0)
def infected_plots(countries, title):
    return covid_helpers.altair_multiple_countries_infected(
        df_alt_all, countries=countries, title=title, days_back=90, marker_day=day_diff)


# > Tip: Click country name in legend to switch countries. Uze mouse wheel to zoom Y axis.

#hide_input
infected_plots(new_waves, "Countries with new waves (vs. 10 days ago)")

#hide
lower_trans = (
        (rate_diff < -0.02) &
        (df_cur['Cases.new.est'] > 100) &
        (rate_diff.abs() > df_data['transmission_rate_std']) &
        (df_data['transmission_rate'] != 0)  # countries reporting infrequently
)
slowing_outbreaks = rate_diff[lower_trans].sort_values().index

#hide_input
Markdown(f"## &#128994; Good news: slowing waves {emoji_flags(slowing_outbreaks)}")

# > Large decrease in transmission rate vs. 10 days ago, that might mean a slowing down / effective control measures.
#
# - Countries are sorted by size of change in transmission rate.
# - Includes only countries that were previously active (more than 100 estimated new cases).
# - "Large decrease" = at least -2%.

#hide_input
style_news_infections(df_data.loc[slowing_outbreaks])

# > Tip: Click country name in legend to switch countries. Uze mouse wheel to zoom Y axis.

#hide_input
infected_plots(slowing_outbreaks, "Countries with slowing waves (vs. 10 days ago)")


# # ICU need:

#hide
def style_news_icu(df):
    cols = {        
        'needICU.per100k': '<i>Current:</i><br>Estimated<br>ICU need<br>per 100k<br>population',
        'needICU.per100k_past': f'<i>{day_diff} days ago:</i><br>Estimated<br>ICU need<br>per 100k<br>population',
        'Cases.new.est': 'Estimated<br><i>recent</i> cases<br> in last 5 days',
        'transmission_rate': 'Estimated<br>daily<br>transmission<br>rate',
        'affected_ratio.est': 'Estimated <br><i>total</i><br>affected<br>population<br>percentage',
      }
    
    return (index_format(df)[cols.keys()].rename(columns=cols).style
        .bar(subset=cols['needICU.per100k'], color='#b21e3e', vmin=0, vmax=10)
        .bar(subset=cols['needICU.per100k_past'], color='#c67f8e', vmin=0, vmax=10)
        .bar(subset=cols['Cases.new.est'], color='#b57b17', vmin=0)
        .bar(subset=cols['affected_ratio.est'], color='#5dad64', vmin=0, vmax=1.0)
        .apply(stylers.add_bar, color='#f49d5a',
               s_v=df['transmission_rate']/df['transmission_rate'].max(),
               subset=cols['transmission_rate'])
        .format('<b>{:.2f}</b>', subset=[cols['needICU.per100k'], cols['needICU.per100k_past']])
        .format('<b>{:,.0f}</b>', subset=cols['Cases.new.est'])
        .format('<b>{:.1%}</b>', subset=[cols['affected_ratio.est'], 
                                         cols['transmission_rate']]))


#hide
icu_diff = df_cur['needICU.per100k'] - df_past['needICU.per100k']
icu_increase = icu_diff[icu_diff > 0.5].sort_values(ascending=False).index

#hide_input
Markdown(f"## &#11093; Bad news: higher ICU need {emoji_flags(icu_increase)}")

# > Large increases in need for ICU beds per 100k population vs. 10 days ago.
#
# - Only countries for which the ICU need increased by more than 0.5 (per 100k).

#hide_input
style_news_icu(df_data.loc[icu_increase])

# > Tip: Click country name in legend to switch countries. Uze mouse wheel to zoom Y axis.

#hide_input
infected_plots(icu_increase, "Countries with Higher ICU need (vs. 10 days ago)")

#hide
icu_decrease = icu_diff[icu_diff < -0.5].sort_values().index

#hide_input
Markdown(f"## &#128994; Good news: lower ICU need {emoji_flags(icu_decrease)}")


# > Large decreases in need for ICU beds per 100k population vs. 10 days ago.
#
# - Only countries for which the ICU need decreased by more than 0.5 (per 100k).

#hide_input
style_news_icu(df_data.loc[icu_decrease])

# > Tip: Click country name in legend to switch countries. Uze mouse wheel to zoom Y axis.

#hide_input
infected_plots(icu_decrease, "Countries with Lower ICU need (vs. 10 days ago)")

# # New cases and deaths:

#hide
new_entries = df_cur.index[~df_cur.index.isin(df_past.index)]

#hide_input
Markdown(f"## &#11093; Bad news: new first significant outbreaks {emoji_flags(new_entries)}")

# > Countries that have started their first significant outbreak (crossed 1000 total reported cases or 20 deaths) vs. 10 days ago.

#hide_input
style_news_infections(df_data.loc[new_entries])

# > Tip: Click country name in legend to switch countries. Uze mouse wheel to zoom Y axis.

#hide_input
infected_plots(new_entries, "Countries with first large outbreak (vs. 10 days ago)")


#hide
def style_no_news(df):
    cols = {
        'Cases.total.est': 'Estimated<br>total<br>cases',
        'Deaths.total': 'Total<br>reported<br>deaths',
        'last_case_date': 'Date<br>of last<br>reported case',
        'last_death_date': 'Date<br>of last<br>reported death',
      }  
    return (index_format(df)[cols.keys()].rename(columns=cols).style
        .format('<b>{:,.0f}</b>', subset=[cols['Cases.total.est'], cols['Deaths.total']]))


#hide
significant_past = ((df_past['Cases.total.est'] > 1000) & (df_past['Deaths.total'] > 10))
active_in_past = ((df_past['Cases.new'] > 0) | (df_past['Deaths.new'] > 0))
no_cases_filt = ((df_cur['Cases.total'] - df_past['Cases.total']) == 0)
no_deaths_filt = ((df_cur['Deaths.total'] - df_past['Deaths.total']) == 0)
no_cases_and_deaths = df_cur.loc[no_cases_filt & no_deaths_filt &
                                 significant_past & active_in_past].index

#hide_input
Markdown(f"## &#128994; Good news: no new cases or deaths {emoji_flags(no_cases_and_deaths)}")

# > New countries with no new cases or deaths vs. 10 days ago.
#
# - Only considering countries that had at least 1000 estimated total cases and at least 10 total deaths and had an active outbreak previously.

#hide_input
style_no_news(df_data.loc[no_cases_and_deaths])

# > Tip: Click country name in legend to switch countries. Uze mouse wheel to zoom Y axis.

#hide_input
infected_plots(no_cases_and_deaths, "New countries with no new cases or deaths (vs. 10 days ago)")

#hide
no_deaths = df_cur.loc[no_deaths_filt & (~no_cases_filt) &
                       significant_past & active_in_past].index

#hide_input
Markdown(f"## Mixed news: no new deaths, only new cases {emoji_flags(no_deaths)}")

# > New countries with no new deaths (only new cases) vs. 10 days ago.
#
# - Only considering countries that had at least 1000 estimated total cases and at least 10 total deaths and had an active outbreak previously.

#hide_input
style_news_infections(df_data.loc[no_deaths])

# > Tip: Click country name in legend to switch countries. Uze mouse wheel to zoom Y axis.

#hide_input
infected_plots(no_deaths, "Countries with only new cases (vs. 10 days ago)")

#hide
not_active = df_cur.loc[no_cases_filt & significant_past & ~active_in_past].index

#hide_input
Markdown(f"## No news: continously inactive countries {emoji_flags(not_active)}")

# > Countries that had no new cases or deaths 10 days ago or now.
#
# - Only considering countries that had at least 1000 estimated total cases and at least 10 total deaths.
# - Caveat:  these countries may have stopped reporting data like [Tanzania](https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Tanzania).

#hide_input
style_no_news(df_data.loc[not_active])

# > Tip: Click country name in legend to switch countries. Uze mouse wheel to zoom Y axis.

#hide_input
infected_plots(not_active, "Continuosly inactive countries (now and 10 days ago)")


# # Deaths burden:

#hide
def style_death_burden(df):
    df = index_format(df)
    cols = {        
        'Deaths.new.per100k': f'<i>Current</i>:<br>{cur_data.PREV_LAG} day<br>death<br>burden<br>per 100k',
        'Deaths.new.per100k.past': f'<i>{day_diff} days ago</i>:<br>{cur_data.PREV_LAG} day<br>death<br>burden<br>per 100k',
        'Deaths.total.diff': f'New<br>reported deaths<br>since {day_diff}<br>days ago',
        'needICU.per100k': 'Estimated<br>current<br>ICU need<br>per 100k<br>population',
        'affected_ratio.est': 'Estimated <br><i>total</i><br>affected<br>population<br>percentage',        
      }  
    death_norm = max(df['Deaths.new.per100k'].max(), df['Deaths.new.per100k.past'].max())
    return (df[cols.keys()].rename(columns=cols).style
        .bar(subset=cols['needICU.per100k'], color='#b21e3e', vmin=0, vmax=10)
        .bar(subset=cols['Deaths.new.per100k'], color='#7b7a7c', vmin=0, vmax=death_norm)
        .bar(subset=cols['Deaths.new.per100k.past'], color='#918f93', vmin=0, vmax=death_norm)
        .bar(subset=cols['Deaths.total.diff'], color='#6b595d', vmin=0)
        .bar(subset=cols['affected_ratio.est'], color='#5dad64', vmin=0, vmax=1.0)
        .format('<b>{:.0f}</b>', subset=[cols['Deaths.total.diff'],
                                        ])
        .format('<b>{:.1f}</b>', subset=cols['needICU.per100k'])
        .format('<b>{:.2f}</b>', subset=[cols['Deaths.new.per100k'],
                                        cols['Deaths.new.per100k.past']])
        .format('<b>{:.1%}</b>', subset=[cols['affected_ratio.est']], na_rep="-"))


#hide
death_change_ratio = df_data['Deaths.new.per100k'] / df_data['Deaths.new.per100k.past']
filt = (
    (df_data['Deaths.new'] > 10) &
    (df_data['Deaths.new.past'] > 10) & 
    (df_data['Deaths.new.per100k'] > 0.1) &
    (death_change_ratio > 2))
higher_death_burden = df_data[filt]['Deaths.diff.per100k'].sort_values(ascending=False).index

#hide_input
Markdown(f"## &#11093; Bad news: higher death burden {emoji_flags(higher_death_burden)}")

# > Countries with significantly higher recent death burden per 100k population vs. 10 days ago.
#
# - "Significantly higher" = 100% more.
# - Only considering countries that had at least 10 recent deaths in both timeframes, and death burden of at least 0.1 per 100k.

#hide_input
style_death_burden(df_data.loc[higher_death_burden])

#hide_input
infected_plots(higher_death_burden, "Countries with higher death burden (vs. 10 days ago)")

#hide
filt = (
    (df_data['Deaths.new'] > 10) &
    (df_data['Deaths.new.past'] > 10) & 
    (df_data['Deaths.new.per100k.past'] > 0.1) &
    (death_change_ratio < 0.5))
lower_death_burden = df_data[filt]['Deaths.diff.per100k'].sort_values(ascending=False).index

#hide_input
Markdown(f"## &#128994; Good news: lower death burden {emoji_flags(lower_death_burden)}")

# > Countries with significantly lower recent death burden per 100k population vs. 10 days ago.
#
# - "Significantly lower" = 50% less
# - Only considering countries that had at least 10 recent deaths in both timeframes, and death burden of at least 0.1 per 100k.

#hide_input
style_death_burden(df_data.loc[lower_death_burden])

#hide_input
infected_plots(lower_death_burden, "Countries with lower death burden (vs. 10 days ago)")

# # Extras:
# ## Future model projections plots
# > For countries in any of the above groups. To see more details and methodology go to [main notebook](/pages/covid-progress-projections/)

# > Tip: Choose country from the drop-down below the graph.

#hide_input
all_news = (new_waves, slowing_outbreaks, 
            icu_increase, icu_decrease,
            higher_death_burden, lower_death_burden,
            not_active, no_deaths, no_cases_and_deaths, new_entries)
news_countries = [c for g in all_news for c in g]
df_alt_filt = df_alt_all[(df_alt_all['day'] > -60) & 
                         (df_alt_all['country'].isin(news_countries))]
covid_helpers.altair_sir_plot(df_alt_filt, new_waves[0])

#hide
# misses analysys (high misses of prediction, but not captured by recent news filters)
df_data.loc[~df_data.index.isin(news_countries)].sort_values('testing_bias.change')[[
    'affected_ratio.miss', 'needICU.per100k.miss', 'transmission_rate.change', 'testing_bias.change',
    'transmission_rate', 'transmission_rate_past', 'affected_ratio.est', 'needICU.per100k',
]].T
