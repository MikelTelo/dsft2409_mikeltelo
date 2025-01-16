# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 02:24:17 2022

@author: 34632
"""

import pandas as pd
import streamlit as st
import numpy as np

st.title("Welcome to Streamlit!")

st.write("Line Chart in Streamlit")
# 10 * 2 dimensional data
chart_data = pd.DataFrame(
    np.random.randn(10, 2),
    columns=[f"Col{i+1}" for i in range(2)]
)

st.line_chart(chart_data)