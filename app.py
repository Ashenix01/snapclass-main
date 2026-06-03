import streamlit as st
from src.screens.teacher_dashboard import teacher_dashboard
from src.screens.student_dashboard import student_dashboard
from src.screens.home_screen import home_screen

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


if __name__ == "__main__":
    main()
