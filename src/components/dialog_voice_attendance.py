import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from datetime import datetime
from src.components.dialog_attendance_result import show_attendance_result

@st.dialog("Voice Attendance")
def voice_attendance_dialog(subject_id):
    st.write("Record audio of students saying I'm present. Then AI will take attendance.")
    audio_data=None
    audio_data = st.audio_input("Record classroom audio")
    if st.button("Analyse Audio",type='primary',width='stretch'):
        if audio_data is None:
            st.warning("Please record audio first.")
            return
        with st.spinner("AI is recognising the voice....."):
            enrolled_res=supabase.table("subject_students").select("*,students(*)").eq('subject_id',subject_id).execute()
            enrolled_students=enrolled_res.data
            if not enrolled_students:
                st.warning("No students in this subject !!!")
                return 
            candidate_dict={
                s['students']['student_id']:s['students']['voice_embedding']
                for s in enrolled_students if s['students'].get('voice_embedding')
            }
            if not candidate_dict:
                st.warning("No enrolled student has voice profile registered !! ")
                return
            audio_bytes = audio_data.read()
            detected_scores = process_bulk_audio(audio_bytes,candidate_dict)
            results, attendance_to_log = [], []
            current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            for node in enrolled_students:
                student = node["students"]
                score = detected_scores.get(student['student_id'],0.0)
                is_present = score> 0.65
                results.append({
                    "Name":student['name'],
                    "ID":student["student_id"],
                    "Source": "Voice" if is_present else "-",
                    "Status": "✅ Present" if is_present else "❌ Absent"
                })
                attendance_to_log.append({
                    "timestamp":current_timestamp,
                    "subject_id":subject_id, 
                    "student_id":int(student['student_id']),
                    "is_present": bool(is_present)
                })
            st.session_state["voice_attendance_result"]=(results,attendance_to_log)
    if st.session_state.get("voice_attendance_result"):
        st.divider()
        results,logs = st.session_state["voice_attendance_result"]
        show_attendance_result(results,logs)





