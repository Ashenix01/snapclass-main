import streamlit as st

def header_home():
    logo_url="https://i.ibb.co/YTYGn5qV/logo.png"

    # Global CSS injection
    st.markdown("""
        <style>
        .custom-title {
            text-align: center;
            color: white !important;
            font-size: 48px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center; flex-direction: column;
        margin-bottom: 10px;
        margin-top: 0px; background-color: blue; padding: 20px; border-radius: 10px;">
                <img src='{logo_url}' style="height:100px;"/>
                <h1 class="custom-title">SNAP<br/> CLASS</h1>
        </div>
        """, unsafe_allow_html=True)
