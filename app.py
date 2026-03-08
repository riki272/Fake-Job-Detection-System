import streamlit as st
from predict import predict_job

st.title("AI Fake Job Detection System")

job_text = st.text_area("Paste Job Description")

if st.button("Analyze Job"):

    result = predict_job(job_text)

    if result == "Fake Job":
        st.error("⚠ This job looks suspicious")

    else:
        st.success("✅ This job appears real")

    st.write("Prediction:", result)