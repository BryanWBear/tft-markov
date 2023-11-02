import streamlit as st
from src import ProbabilityCalculator, Unit
import plotly.express as px
import pandas as pd

with st.sidebar:
    level = st.number_input('Player level', min_value=4, max_value=9)
    max_number_shops = st.number_input('Maximum number of shops', min_value=1, max_value=100)
    expander = st.expander("Filter 1")
    unit_cost = expander.number_input('Unit Cost', min_value=1, max_value=5)
    num_copies_start = expander.number_input('Number of Copies Out of Pool', min_value=0)
    num_copies_wanted = expander.number_input('Number of Copies Wanted', min_value=1, max_value=9)

p_calc = ProbabilityCalculator([Unit(num_wanted=num_copies_wanted, num_have=num_copies_start, cost=unit_cost)],
                               level)
probs = p_calc.get_agg_probs(max_number_shops)

df = pd.DataFrame({'probs': probs, 'num_shops': list(range(1, len(probs) + 1))})

fig = px.bar(df, x='num_shops', y='probs')
st.plotly_chart(fig, use_container_width=True)