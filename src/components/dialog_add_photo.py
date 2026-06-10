import streamlit as st
from PIL import Image

@st.dialog("Capture or Upload Photo")
def add_photo_dialog():
    st.write("Add Classroom photos to scan for attendance")

    if "photo_tab" not in st.session_state:
        st.session_state["photo_tab"]="camera"
    tab1, tab2 = st.columns(2)
    with tab1:
        type_camera = "primary" if st.session_state["photo_tab"]=="camera" else "tertiary"
        if st.button("Camera",type=type_camera,width='stretch'):
            st.session_state["photo_tab"]="camera"
    with tab2:
        type_upload = "primary" if st.session_state["photo_tab"]=="upload" else "tertiary"
        if st.button("Upload Photo",type=type_upload,width='stretch'):
            st.session_state["photo_tab"]="upload"        
    if st.session_state["photo_tab"]=="camera":
        cam_photo = st.camera_input("Take Snapshot",key="dialog_cam")
        if cam_photo:
            st.session_state["attendance_image"].append(Image.open(cam_photo))
            st.toast("Photo Captured !")
            st.rerun()
    if st.session_state["photo_tab"]=="upload":
        uploaded_files = st.file_uploader("Choose Images from file",type=['jpg','png','jpeg'],accept_multiple_files=True, key="dialog_upload")
        if uploaded_files:
            for f in uploaded_files:
                st.session_state["attendance_image"].append(Image.open(f))
            st.toast("Photos Uploaded Successfully !")
            st.rerun()
    st.divider()
    if st.button("Done",type='primary',width='stretch'):
        st.rerun() 