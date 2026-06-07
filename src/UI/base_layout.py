import streamlit as st

def style_base_layout_home():
    st.markdown("""
    <style>
        .stApp{
            background:blue !important;
        }
        .stApp div[data-testid="stColumn"]{
                background: white !important;
                padding: 2rem !important;
                border-radius: 3rem !important;}
                
    </style>
                """,unsafe_allow_html=True)
    
def style_base_layout_dashboard():
    st.markdown("""
    <style>
                .stApp{
                    background:#E0E3FF !important;
                     
                }
                
    </style>
                """,unsafe_allow_html=True)

def style_base_layout():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&display=swap');
    
    @import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Outfit:wght@100..900&display=swap');
                
    /* Hide tool bar*/
        #MainMenu, footer, header{
            visibility: hidden;
        }
        .block-container{
                padding-top:1.5rem;
        }
        h1{
                font-family: 'Archivo Black',sans-serif !important;
                font-size: 4rem !important;
                color: black !important;
                line-height: 1.1 !important;
                margin-bottom:0rem !important;
        }
        h2{
                font-family: 'Archivo Black',sans-serif !important;
                font-size: 2.5rem !important;
                color: black !important;
                line-height: 0.9 !important;
                margin-bottom:0rem !important;
        }
        h3 {
                font-family: 'Outfit', sans-serif !important;
                font-size: 2rem !important;  
                font-weight: bold !important; 
        }

        h4, p {
                font-family: 'Outfit', sans-serif !important;
                font-size: 1.2rem !important;
        }

        button[kind="primary"]{
                background: blue !important;  
                border-radius: 1.5rem !important;
                color: white !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                padding: 10px 20px !important;
        }
        button[kind="secondary"]{
                background: #EB459E !important;
                border-radius: 1.5rem !important;
                color: white !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                padding: 10px 20px !important;
        }
        button[kind="tertiary"]{
                background: black !important;
                border-radius: 1.5rem !important;
                color: white !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                padding: 10px 20px !important;
        }
        button:hover{
                transform : scale(1.05) 
        }
                
    </style>
                """,unsafe_allow_html=True)