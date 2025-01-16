# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 02:20:11 2022

@author: 34632
"""

import streamlit as st

st.title("Welcome to Streamlit!")

selectbox = st.selectbox(
    "Select yes or no",
    ["Yes", "No"]
)
st.write(f"You selected {selectbox}")