import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_student_to_subject
import time
@st.dialog("Quick Enrollment")
def auto_enroll_dialog(join_code):
    # Only logged in student have auto join feature --> Acting as guard
    if "student_data" not in st.session_state:
        st.warning("Please login to your student profile first.Then open join link or scan joining QR code !!")
        return
    # Now enrollment for logged user student
    student_id = st.session_state['student_data']['student_id']
    response = supabase.table("subjects").select("subject_id,name").eq('subject_id',join_code).execute()
    if not response.data:
        st.error("Subject code not found!")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return 
    subject = response.data[0]
    check = supabase.table('subject_students').select("*").eq("subject_id",subject["subject_id"]).eq("student_id",student_id).execute()
    if check.data:
        st.info("You are already enrolled!")
        if st.button("Got it!"):
            st.query_params.clear()
            st.rerun()
    st.markdown(f"Would you like to enroll in **{subject['name']}**?")
    col1,col2 = st.columns(2)
    with col1:
        if st.button("No Thanks ❌"):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button("Yes!! Enroll Now!",type='primary',width='stretch'):
            enroll_student_to_subject(student_id,subject['subject_id'])
            st.toast("Joined Successfully !!!")
            st.query_params.clear()
            time.sleep(2)
            st.rerun()
