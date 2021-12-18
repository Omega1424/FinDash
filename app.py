import streamlit as st
import page1
import page2
from multiapp import MultiApp

st.set_page_config(
    page_title="Financial Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# rest of the code


app = MultiApp()
app.add_app("Company Information", page1.app)
app.add_app("Portfolio Tracker", page2.app)
app.run()