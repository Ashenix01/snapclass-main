import streamlit as st
import segno
import io
from src.database.config import supabase
from src.database.db import enroll_student_to_subject
import time

@st.dialog("Enroll for Subject")
def enroll_subject_dialog():
    st.write("Enter subject code provided by Institute")
    join_code = st.text_input("Enter subject code",placeholder="E.g. CS203")
    if st.button("Enroll Now",type='primary',width='stretch'):
        if join_code:
            response = supabase.table("subjects").select('subject_id,name,subject_code').eq('subject_code',join_code).execute()
            if response.data:
                subject = response.data[0] #id,name,code all in a row
                # To check if student is already enrolled in this subject or not
                student_id = st.session_state["student_data"]["student_id"]
                check = supabase.table('subject_students').select("*").eq("subject_id",subject["subject_id"]).eq("student_id",student_id).execute()
                if check.data:
                    st.warning("You are Already Enrolled in this subject")
                else:
                    enroll_student_to_subject(student_id,subject["subject_id"])
                    st.success("Successfully Enrolled")
                    time.sleep(1)
                    st.rerun()
            else:
                st.warning("This Subject is unavailable!!")

        else:
            st.warning("Enter subject code first!!")
    