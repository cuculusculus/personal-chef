# components/footer_nav.py
import streamlit as st

def render_footer_nav():

    st.write("FOOTER DEBUG START")

    if st.button("🏠"):
        st.write("HOME CLICK")

    if st.button("🥬"):
        st.write("STOCK CLICK")

    if st.button("⭐"):
        st.write("FAV CLICK")

    if st.button("🕒"):
        st.write("HISTORY CLICK")

    st.write("FOOTER DEBUG END")
