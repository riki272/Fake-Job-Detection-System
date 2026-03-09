import streamlit as st
from predict import predict_job

st.title("Fake Job Detection System")

# Reset function
def clear_text():
    st.session_state.job_text = ""

# Text box
job_text = st.text_area("Paste Job Description", key="job_text")

col1, col2 = st.columns(2)

with col1:
    analyze = st.button("Analyze Job")

with col2:
    refresh = st.button("Reset", on_click=clear_text)

# Analyze logic
if analyze:

    if job_text.strip() == "":
        st.warning("⚠ Please paste a job description before analyzing.")

    else:
        result, confidence = predict_job(job_text)

        if result == "Fake Job":
            st.error("⚠ This job looks suspicious")
        else:
            st.success("✅ This job appears real")

        st.write("Prediction:", result)
        st.write("Confidence Score:", confidence)



