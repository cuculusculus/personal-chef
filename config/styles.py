#styles.py
import streamlit as st

APP_CSS = """
<style>

.block-container {
    padding-bottom: 80px !important;
}
.stApp {
    padding-bottom: 80px;
}
</style>
"""

def apply_styles():
    st.markdown(APP_CSS, unsafe_allow_html=True)
