"""Entry point for the StreamLit app"""
import plotly.express as px
import streamlit as st
import utils.management as aux

data = aux.load_clean_data_into_main()
data.info()
