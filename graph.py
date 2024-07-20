import streamlit as st
import pandas as pd
import altair as alt


df = pd.read_csv('data/adult_ll_history.csv', parse_dates=True)

# Initialize Streamlit
st.set_page_config(layout = 'wide')
st.title('Classic Constructed Living Legend Points History')

# Offer choice of heroes to lighten the graph view
options = st.multiselect(
    'Choose heroes to display',
    df['Hero'],
    df['Hero'])

df_restricted = df[df['Hero'].isin(options)]

df_melted = df_restricted.melt(id_vars=['Hero'], var_name='Date', value_name='LL Points')
df_melted['Date'] = pd.to_datetime(df_melted['Date'], format='%Y-%m-%d')

# Graph creation
chart = alt.Chart(df_melted).mark_line(point=True).encode(
    x='Date:T',
    y='LL Points:Q',
    color='Hero:N',
    tooltip=['Hero', 'Date:T', 'LL Points:Q']
).interactive()

# Add a LL threshold
horizontal_rule = alt.Chart(pd.DataFrame({'LL Points': [1000]})).mark_rule(color='red').encode(
    y='LL Points:Q',
    tooltip=alt.TooltipValue('Living legend threshold')
)

combined_chart = chart + horizontal_rule

st.write('Disclamer: These historical data were sourced from backups on the Wayback Machine for this page: https://fabtcg.com/resources/rules-and-policy-center/living-legend/. There is no guarantee that the data represented in this graph are 100% complete.')

# Graph display
st.altair_chart(combined_chart, use_container_width=True)


