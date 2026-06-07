import streamlit as st
from src.UI.base_layout import style_base_layout_dashboard,style_base_layout_home,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists,create_teacher,teachers_login
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embeddings
from src.database.db import get_all_students, create_student
from src.database.db import get_student_subjects,get_student_attendance
from src.components.dialog_enroll_subject import enroll_subject_dialog
from src.components.subject_card import subject_card
from src.database.db import unenroll_student_from_subject
from src.components.dialog_auto_enroll import auto_enroll_dialog
from PIL import Image
import numpy as np
import time

global show_registration

def student_dashboard_screen():
    style_base_layout_dashboard()
    style_base_layout()
    student_data=st.session_state['student_data']
    student_id = student_data["student_id"]
    st.title("Student Dashboard")
    col1, col2=st.columns(2,gap="large")
    with col1:
        header_dashboard()
    with col2:
        st.subheader(f"Welcome {student_data['name']}!")    
        st.markdown(
            "<div style='margin-top:10px; display:flex; justify-content:center;'>",
            unsafe_allow_html=True
        )
        if st.button("Logout", type='secondary', key='loginbackbtn', icon=":material/arrow_back:", icon_position="left",width='stretch'):
            st.session_state['is_logged_in'] = False
            del st.session_state["student_data"]
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    c1,c2=st.columns(2)
    with c1:
        st.header("Your Enrolled Subjects")
    with c2:
        if st.button("Enroll in Subject",type='primary',width='stretch'):
            enroll_subject_dialog()
           
    st.divider()
    with st.spinner("Loading your subjects ...."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    for log in logs:
        sid=log['subject_id']
        if sid not in stats_map:
            stats_map[sid]={"total":0,"attended":0}
        stats_map[sid]['total']+=1
        if log.get("is_present"):
            stats_map[sid]["attended"]+=1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']

        stats = stats_map.get(sid,{"total":0,"attended":0})
        def unenroll_button():
            if st.button("Unenroll from this subject",type='tertiary',key=f"unenroll_{sid}",width='stretch',icon=":material/delete_forever:"):
                unenroll_student_from_subject(student_id,sid) #sid is subject_id
                st.toast(f"Unerolled from {sub['name']}")
                st.rerun()

        with cols[i%2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('📅',"Total",stats['total']),
                    ('✅',"Attended",stats['attended'])
                ],
                footer_callback=unenroll_button

            )


    footer_dashboard()



def student_dashboard():
    style_base_layout_dashboard()
    style_base_layout()
    # if pending join state is there and user is logged in it will direct to auto enroll page
    if (
        st.session_state.get("is_logged_in", False)
        and "pending_join_code" in st.session_state and st.session_state["user_role"]=="student"
    ):
        auto_enroll_dialog(
            st.session_state["pending_join_code"]
        )


    show_registration=False
    if "student_data" in st.session_state:
        student_dashboard_screen()
        return
    
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
        img = np.array(Image.open(photo_source))
        with st.spinner("AI is scanning ......"):
            detected, all_ids, num_faces = predict_attendance(img) 

            if num_faces==0:
                st.warning("Face not found !")
            elif num_faces > 1:
                st.warning("Multiple faces found !")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id']==student_id),None)

                    if student:
                        st.session_state['student_data']=student
                        st.session_state['user_role']='student'
                        st.session_state['is_logged_in']=True
                        st.toast(f"Welcome Back! {student['name']}")
                        time.sleep(2)
                        st.rerun()


                else:
                    st.info("Face not recognized ! You might be a new Student! Login first !")
                    show_registration = True
    
    if show_registration:
        with st.container(border=True):
            st.header("Register New Profile ! ")
            new_name = st.text_input("Enter your name", placeholder="E.g. Ashish Chauhan")
            st.subheader("Optional : Voice Enrollment!")
            st.info("Enroll for voice only attendance!")
            audio_data=None

            try:
                audio_data = st.audio_input("Record a short phrase. E.g. I'm present.")
            except Exception as e:
                st.error("Audio Data failed")
            if st.button('Create Account', type='primary'):
                if new_name:
                    with st.spinner("Creating profile ..."):
                        img=np.array(Image.open(photo_source))
                        encoding = get_face_embeddings(img)
                        if encoding:
                            face_emb = encoding[0].tolist()

                            voice_embedding = None
                            if audio_data:
                                voice_emb = get_voice_embeddings(audio_data.read()) #audio bytes using read function
                            response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)
                            if response_data:
                                train_classifier()
                                st.session_state['student_data']=response_data[0]
                                st.session_state['user_role']='student'
                                st.session_state['is_logged_in']=True
                                st.toast(f"Profile Created! {new_name}")
                                time.sleep(2)
                                st.rerun()
                        else:
                            st.error("Couldn't capture your facial feature for registration !! ")




                else:
                    st.warning("Please enter your name!")
            
                



    st.space(25)
    footer_dashboard()
    

    