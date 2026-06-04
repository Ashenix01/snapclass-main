import streamlit as st
from src.UI.base_layout import style_base_layout_dashboard,style_base_layout_home,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists,create_teacher,teachers_login
from PIL import image
import numpy as np

def student_dashboard():
    style_base_layout_dashboard()
    style_base_layout()
    col1, col2=st.columns(2,gap="large")
    with col1:
        header_dashboard()
    with col2:
        st.markdown(
            "<div style='margin-top:60px; display:flex; justify-content:center;'>",
            unsafe_allow_html=True
        )
        if st.button("Go Back to Home", type='secondary', key='loginbackbtn', icon=":material/arrow_back:", icon_position="left"):
            st.session_state['login_type'] = None
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.space(2)

    st.header("Login using FaceID")
    photo_source=st.camera_input("Position your face in Center!")
    if photo_source:
        np.array(image.open(photo_source))
    footer_dashboard()
    

    