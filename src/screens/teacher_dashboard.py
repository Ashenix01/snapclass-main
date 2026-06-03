import streamlit as st
from src.UI.base_layout import style_base_layout_dashboard,style_base_layout_home,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard


def teacher_dashboard():
    style_base_layout_dashboard()
    style_base_layout()

    if 'teacher_login_type' not in st.session_state or st.session_state['teacher_login_type']=='login':
        teacher_dashboard_login()

    elif st.session_state['teacher_login_type']=='register':
        teacher_dashboard_register()
        st.session_state['teacher_login_type']='register'
    
        


def teacher_dashboard_login():
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
        
    st.header("Login to your Teacher Profile",text_alignment="center")
    st.space(50)
    teacher_username = st.text_input("Username", placeholder="Enter your username")

    teacher_password = st.text_input("Password", placeholder="Enter your password", type="password")

    st.divider()
    btn_col1, btn_col2=st.columns(2, gap="small")
    with btn_col1:
        if st.button("Login", type='primary', key='teacherloginbtn',icon=":material/passkey:", icon_position="left",width='stretch'):
            st.session_state['teacher_login_type']='login'
            st.success("Login successful!")
            st.rerun()
    with btn_col2:
        if st.button("Register Instead", type='secondary', key='teacherregisterbtn',icon=":material/person_add:", icon_position="left",width='stretch'):
            st.session_state['teacher_login_type']='register'
            st.rerun()
    
    footer_dashboard()






def teacher_dashboard_register():
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
    st.header("Register your Teacher Profile",text_alignment="center")
    st.space(50)
    teacher_name = st.text_input("Full Name", placeholder="Enter your full name")
    subject_expertise = st.text_input("Subject Expertise", placeholder="Enter your subject expertise (e.g., Math, TAFL, DS, etc.)")
    subject_code= st.text_input("Subject Code", placeholder="Enter your subject code (e.g., BCS304)")
    teacher_username = st.text_input("Username", placeholder="Enter your username")

    teacher_password = st.text_input("Password", placeholder="Enter your password", type="password")

    teacher_confirm_password = st.text_input("Confirm Password", placeholder="Confirm your password", type="password")

    st.divider()
    btn_col1, btn_col2=st.columns(2, gap="small")
    with btn_col1:
        if st.button("Register", type='secondary', key='teacherloginbtn',icon=":material/passkey:", icon_position="left",width='stretch'):
            st.session_state['teacher_login_type']='login'
            st.success("Registration successful! Please login with your credentials.")
            st.rerun()
    with btn_col2:
        if st.button("Login Instead", type='primary', key='teacherregisterbtn',icon=":material/person_add:", icon_position="left",width='stretch'):
            st.session_state['teacher_login_type']='login'
            st.success("Please login with your credentials.")
            st.rerun()
    footer_dashboard()

    

    