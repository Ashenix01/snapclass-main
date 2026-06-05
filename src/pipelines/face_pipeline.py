import dlib
import face_recognition_models
from sklearn.svm import SVC
import numpy as np
import streamlit as st
from src.database.db import get_all_students


@st.cache_resource #So that model load for only one time
def load_dlib_models():
    detector=dlib.get_frontal_face_detector()

    sp=dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec=dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector,sp,facerec 


def get_face_embeddings(image_np):
    detector,sp,facerec=load_dlib_models()

    faces=detector(image_np,1)

    embeddings=[]

    for face in faces:
        shape = sp(image_np,face) # gives 68 landmark point of the face 
        face_description = facerec.compute_face_descriptor(image_np,shape,1) # Genereate 128 Dimension embedding for the image Unique signature of the face
        embeddings.append(np.array(face_description))

    return embeddings


@st.cache_resource
def get_trained_model():
    X=[]  #all face embeddings of in numpy array form
    y=[]  #all students ids to uniquely identity all students

    students_db=get_all_students()

    if not students_db:
        return None
    for student in students_db:
        embedding=student.get('face_embedding')
        id=student.get('student_id')
        X.append(np.array(embedding))
        y.append(id)
    
    if len(X)==0:
        return 0
    
    clf=SVC(kernel='linear',probability=True,class_weight='balanced')

    try:
        clf.fit(X,y)
    except ValueError:
        pass
    return {
        "clf":clf,
        "X":X,
        "y":y
    }

def train_classifier():
    st.cache_resource.clear()
    model_data=get_trained_model() 
    return bool(model_data)

def predict_attendance(class_image_np):
    embeddings=get_face_embeddings(class_image_np)
    detected_students={}
    model_data = get_trained_model()

    if not model_data:
        return detected_students,[],len(embeddings)
    
    clf = model_data['clf']
    X_train=model_data['X']
    y_train=model_data['y']

    all_students=sorted(list(set(y_train)))

    for embedding in embeddings:
        if len(all_students)>=2:
            predicted_id=int(clf.predict([embedding]))
        else:
            predicted_id=int(all_students[0])
        
        student_embedding=X_train[y_train.index(predicted_id)] 
        best_match_score = np.linalg.norm(student_embedding-embedding)
        resemblance_threshold = 0.6
        if best_match_score <= resemblance_threshold:
            detected_students[predicted_id]=True

    return detected_students,all_students,len(embeddings)



    


    
