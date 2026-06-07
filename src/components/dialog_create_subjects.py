import streamlit as st
from src.database.db import create_subject


@st.dialog("Create New Subjects")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of the new subject")
    subject_code=st.text_input("Subject Code",placeholder="CS203")
    subject_name=st.text_input("Subject Name",placeholder="Cyber Security, Data Structures, etc")
    subject_section=st.text_input("Section",placeholder="P1,P2, etc.")

    if st.button("Create subject now",type='primary',width='stretch'):
        if subject_code and subject_name and subject_section:
            try:
                create_subject(subject_code,subject_name,subject_section,teacher_id)
                st.toast("Subject Created Successful !")
                st.rerun()
            except Exception as e:
                st.error("Unexpected Error !"+str(e))
        else:
            st.warning("All fields Required !")
