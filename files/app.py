import streamlit as st

def main():
    st.title("SnapClass Demo")
    st.header("My first Snapclass app")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Column 1")
        st.write("This is the first column.")  
    with col2:
        st.subheader("Column 2")
        st.write("This is the second column.")

    name = st.text_input("What is your name?", placeholder="Enter your name here")

    if st.button("Display my name", type="primary", key='btn1'):
        st.write(f"Hello {name}!")

    if st.button("Good Morning", type="secondary", key='btn2'):
        st.write(f"Good Morning, {name}!")

    st.markdown(
        """
        <style>
        .stButton button {
            background-color: #4CAF50 !important;
            border: 2px solid #4CAF50 !important;
            color: white !important;
            font-size: 16px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.image("D:/SnapClass/image.png", caption="SnapClass Logo", width=200)

if __name__ == "__main__":
    main()
