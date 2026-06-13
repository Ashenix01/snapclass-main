import streamlit as st
import numpy as np
import pandas as pd
from src.database.config import supabase
from src.UI.base_layout import style_base_layout_dashboard,style_base_layout_home,style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists,create_teacher,teachers_login,get_teacher_subjects
from src.components.dialog_create_subjects import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_add_photo import add_photo_dialog
from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.database.db import get_attendance_for_teacher
from datetime import datetime


def teacher_dashboard():
    style_base_layout_dashboard()
    style_base_layout()
    if "teacher_data" in st.session_state:
        teacher_dashboard_screen()
    elif 'teacher_login_type' not in st.session_state or st.session_state['teacher_login_type']=='login':
        teacher_dashboard_login()

    elif st.session_state['teacher_login_type']=='register':
        teacher_dashboard_register()
        st.session_state['teacher_login_type']='register'
    
        
def teacher_dashboard_screen():
    style_base_layout_dashboard()
    style_base_layout()
    teacher_data=st.session_state['teacher_data']
    st.title("Teacher Dashboard")
    col1, col2=st.columns(2,gap="large",vertical_alignment='bottom')
    with col1:
        header_dashboard()
    with col2:
        st.subheader(f"Welcome {teacher_data['name']}!")    
        if st.button("Logout", type='secondary', key='loginbackbtn',width='stretch', icon=":material/arrow_back:", icon_position="left"):
            st.session_state['is_logged_in'] = False
            del st.session_state["teacher_data"]
            st.rerun()

    st.space(2)
    if "current_teacher_tab" not in st.session_state:
        st.session_state["current_teacher_tab"]="take_attendance"
    tab1,tab2,tab3 = st.columns(3,gap='xsmall')
    with tab1:
        type1 = "primary" if st.session_state["current_teacher_tab"]=="take_attendance" else "tertiary"
        if st.button("Take Attendance",width='stretch',icon=":material/ar_on_you:",type=type1):
            st.session_state["current_teacher_tab"]="take_attendance"
            st.rerun()
    with tab2:
        type2 = "primary" if st.session_state["current_teacher_tab"]=="manage_subjects" else "tertiary"
        if st.button("Manage Subjects",width='stretch',icon=":material/book_ribbon:",type=type2):
            st.session_state["current_teacher_tab"]="manage_subjects"
            st.rerun()
    with tab3:
        type3 = "primary" if st.session_state["current_teacher_tab"]=="attendance_record" else "tertiary"
        if st.button("Attendace Records",width='stretch',icon=":material/cards_stack:",type=type3):
            st.session_state["current_teacher_tab"]="attendance_record"
            st.rerun()
        
    st.divider()

    if st.session_state["current_teacher_tab"]=="take_attendance":
        teacher_tab_take_attendance()
    if st.session_state["current_teacher_tab"]=="manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state["current_teacher_tab"]=="attendance_record":
        teacher_tab_attendance_record()
    st.space(25)
    footer_dashboard()

def teacher_tab_take_attendance():
    teacher_id = st.session_state["teacher_data"]["teacher_id"]
    st.header("Take AI Attendance")
    if "attendance_image" not in st.session_state:
        st.session_state["attendance_image"]=[]
    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning("You haven't created any subject ! Please create one to begin!")
        return 
    subjects_options = {f"{s['name']}-{s['subject_code']}":s["subject_id"] for s in subjects}

    col1,col2 = st.columns([3,2],vertical_alignment='bottom')
    with col1:
        selected_subject_label=st.selectbox("Select Subject",options=list(subjects_options.keys()))
    with col2:
        if st.button("Add Photos 🖼️",type='primary',width='stretch'):
            add_photo_dialog()
        

    selected_subject_id = subjects_options[selected_subject_label]
    st.divider()

    if st.session_state["attendance_image"]:
        st.header("Added Photos")
        gallery_cols = st.columns(4)
        for idx,img in enumerate(st.session_state["attendance_image"]):
            with gallery_cols[idx % 4]:
                st.image(img,width='stretch',caption=f'Photo {idx+1}')


    has_photos = bool(st.session_state["attendance_image"])
    col1,col2,col3 = st.columns(3)
    with col1:
        if st.button("Clear All Photos",width='stretch',type='tertiary',icon=":material/delete:",disabled=not has_photos):
            st.session_state["attendance_image"]=[]
            st.rerun()

    with col2:
        
        if st.button("Run face Analysis",width='stretch',type='secondary',icon=":material/analytics:",disabled=not has_photos):
            with st.spinner("Deep Scanning Classroom Photos...."):
                #to store which student was detected in which photo {id:[photo1,photo3]}
                all_detected_ids={}
                for idx,img in enumerate(st.session_state["attendance_image"]):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)
                    if detected:
                        for sid in detected:
                            student_id=int(sid)
                            all_detected_ids.setdefault(student_id,[]).append(f"Photo {idx+1}")
                # Now for all the students of that particular subject for which teacher has run the analysis we have to mark present all detected student in all these photos that are enrolled in the particular subject only because we made dictionary containing all the detected student that are part of the system with their "student_id" as key and "which photos" as value it may contain students that are not enrolled in this particular subject we 
                # all enrolled student
                # all detected student and that are enrolled in this subject 
                # mark present these student and for all the remaining student of all enrolled students mark absent
                enrolled_res=supabase.table("subject_students").select("*,students(*)").eq('subject_id',selected_subject_id).execute()
                enrolled_students=enrolled_res.data
                if not enrolled_students:
                    st.warning("No students in this subject !!!")
                else:
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    for node in enrolled_students:
                        student = node["students"]
                        source = all_detected_ids.get(int(student['student_id']),[]) # fetch list of photos in which student appeared
                        # is_present = detected.get(int(student['student_id']),False)
                        is_present = len(source)>0
                        results.append({
                            "Name":student['name'],
                            "ID":student["student_id"],
                            "Source":", ".join(source) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })
                        attendance_to_log.append({
                            "timestamp":current_timestamp,
                            "subject_id":int(subjects_options[selected_subject_label]),
                            "student_id":int(student['student_id']),
                            "is_present": bool(is_present)
                        })
                    attendance_result_dialog(results,attendance_to_log) # it is still within spinner 
    with col3:
        if st.button("Voice Attendance",width='stretch',type='primary',icon=":material/mic:"):
            voice_attendance_dialog(selected_subject_id)
    

def teacher_tab_manage_subjects():
    teacher_id = st.session_state["teacher_data"]["teacher_id"]
    col1, col2 = st.columns(2)
    with col1:
        st.header("Manage Subjects",width='stretch')
    with col2:
        if st.button("Create new Subject",width='stretch'):
            create_subject_dialog(teacher_id)
    
    # List all subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥","Students",sub["total_students"]),
                ("🕰️","Classes",sub["total_classes"]),
                
            ]
            def share_btn():
                if st.button(
                    f"Share code : {sub['name']}",
                    key=f"share_{sub['subject_code']}",
                    icon=":material/share:"
                ):
                    share_subject_dialog(sub['name'],sub['subject_code'])
                st.space(2)
            subject_card(
                name = sub["name"],
                code = sub["subject_code"],
                section = sub["section"],
                stats = stats,
                footer_callback = share_btn
            )
    else:
        st.info("No subject found")


def teacher_tab_attendance_record():
    st.header("Attendance Records")
    teacher_id = st.session_state["teacher_data"]["teacher_id"]
    records = get_attendance_for_teacher(teacher_id)
    if not records:
        return 
    data =[]
    for r in records:
        ts = r.get("timestamp")

        data.append({
            "ts_group":ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject":r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "is_present": r.get("is_present",False)
        })
        df = pd.DataFrame(data)
        summary =(
            df.groupby(['ts_group','Time','Subject','Subject Code']).agg(
                Present_count = ('is_present','sum'),
                Total_count = ('is_present','count')
            ).reset_index()
        )
        summary['Attendance Stats']=(
            "✅"+summary['Present_count'].astype(str)+"/"+summary['Total_count'].astype(str)+' Students'
        )
        display_df = (summary.sort_values(by='ts_group',ascending=False)[["Time","Subject","Subject Code","Attendance Stats"]])
        st.dataframe(display_df,width='stretch',hide_index=True)












    

def login_teacher(username, password):
    teacher=teachers_login(username, password)
    if teacher:
        st.session_state['teacher_data']=teacher
        st.session_state['user_role']="teacher"
        st.session_state['is_logged_in']=True
        return True
    else:
        return False
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
            if not teacher_username or not teacher_password:
                st.error("Please enter both username and password.")
                return
            if login_teacher(teacher_username, teacher_password):
                st.toast("Login successful!", icon="✅")
                import time
                time.sleep(1)
                st.rerun() # Rerun is important because Session States were changed when login_teacher() function was called

            else:
                st.error("Invalid username or password.")
                import time
                time.sleep(2)
                st.session_state['teacher_login_type']='login'
                st.rerun()
    with btn_col2:
        if st.button("Register Instead", type='secondary', key='teacherregisterbtn',icon=":material/person_add:", icon_position="left",width='stretch'):
            st.session_state['teacher_login_type']='register'
            st.rerun()

    st.space(25)
    footer_dashboard()


def register_teacher(teacher_name, subject_expertise, subject_code, teacher_username, teacher_password, teacher_confirm_password):
    if not all([teacher_name, subject_expertise, subject_code, teacher_username, teacher_password, teacher_confirm_password]):
        return False, "Please fill in all the fields."

    if teacher_password != teacher_confirm_password:
        return False, "Passwords do not match."

    if check_teacher_exists(teacher_username):
        return False, "Username already exists. Please choose a different username."
    
    try:
        create_teacher(teacher_username, teacher_password, teacher_name,subject_expertise, subject_code)
        return True, "Registration successful. Login with your credentials."
    except Exception as e:
        return False, f"Unexpected error occured during registration ! + {str(e)}"


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
        if st.button("Register Now!", type='secondary', key='teacherloginbtn',icon=":material/passkey:", icon_position="left",width='stretch'):
            success, message = register_teacher(teacher_name, subject_expertise, subject_code, teacher_username, teacher_password, teacher_confirm_password)
            if success:
                st.toast("Registration successful!", icon="✅")
                import time
                time.sleep(2)
                st.session_state['teacher_login_type']='login'
                st.rerun()
            else:
                st.error(message)
                import time
                time.sleep(2)

    with btn_col2:
        if st.button("Login Instead", type='primary', key='teacherregisterbtn',icon=":material/person_add:", icon_position="left",width='stretch'):
            st.session_state['teacher_login_type']='login'
            st.success("Please login with your credentials.")
            st.rerun()

    st.space(25)
    footer_dashboard()

    

    