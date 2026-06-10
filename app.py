import streamlit as st
from src.screens.teacher_dashboard import teacher_dashboard
from src.screens.student_dashboard import student_dashboard
from src.screens.home_screen import home_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog
def main():
    st.set_page_config(
        page_title='SnapClass',
        page_icon='https://i.ibb.co/YTYGn5qV/logo.png'
    )
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    join_code = st.query_params.get('join-code')
    if join_code:
        st.session_state["pending_join_code"] = join_code
        if st.session_state["login_type"]!="student":
            st.session_state["login_type"]="student"
            st.rerun()

    match st.session_state['login_type']:
        case 'teacher':
            teacher_dashboard()
        case 'student':
            student_dashboard()
        case None:
            home_screen()
    




if __name__ == "__main__":
    main()
