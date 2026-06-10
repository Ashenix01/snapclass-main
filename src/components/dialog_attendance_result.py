import streamlit as st
import pandas as pd
from src.database.db import create_attendance

def show_attendance_result(results,attendance_log):
        st.write("Please review attendance before confirming.")
        df = pd.DataFrame(results)
        st.dataframe(df,use_container_width=True,hide_index=True,width='stretch')
        col1,col2 = st.columns(2)
        with col1:
            if st.button("Discard",width='stretch',type='secondary') :
                st.rerun()
        with col2:
            if st.button("Confirm & save ",type='primary',width='stretch'):
                try:
                    create_attendance(attendance_log)
                    st.toast("Attendance Taken ✅")
                    st.session_state["attendance_image"]=[]
                    st.session_state["voice_attendance_result"]=None
                    st.rerun()
                except Exception as e:
                    st.error(f"Unexpected error !!! Sync failed {str(e)}!!")

@st.dialog("Attendance Result")
def attendance_result_dialog(results,attendance_log):
    show_attendance_result(results,attendance_log)




    