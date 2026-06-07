import streamlit as st
from src.screens.teacher_dashboard import teacher_dashboard
from src.screens.student_dashboard import student_dashboard
from src.screens.home_screen import home_screen
from src.components.dialog_auto_enroll import auto_enroll_dialog
def main():
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    match st.session_state['login_type']:
        case 'teacher':
            teacher_dashboard()
        case 'student':
            student_dashboard()
        case None:
            home_screen()
    
    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state["login_type"]!="student":
            st.session_state["login_type"]="student"
            st.rerun()
        if st.session_state['is_logged_in'] and st.session_state["user_role"]=='student':
            auto_enroll_dialog(join_code)



if __name__ == "__main__":
    main()
