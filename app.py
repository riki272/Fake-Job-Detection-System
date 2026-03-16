import streamlit as st
from predict import predict_job

# --- Page Setup ---
st.set_page_config(page_title="AI Fake Job Detector", page_icon="🚨")

st.title("🚨Fake Job Detection System")
st.write("Analyze job descriptions and detect potential fake job postings.")

# --- Session State / Reset Logic ---
if "job_text" not in st.session_state:
    st.session_state.job_text = ""

def clear_text():
    st.session_state.job_text = ""

# --- Input Area ---
job_text = st.text_area(
    "Paste Job Description",
    key="job_text",
    height=200
)

col1, col2 = st.columns(2)

with col1:
    analyze = st.button("🔍 Analyze Job")

with col2:
    st.button("🔄 Reset", on_click=clear_text)

# --- Analysis Logic ---
if analyze:
    if not job_text.strip():
        st.warning("⚠ Please paste a job description before analyzing.")
    else:
        # 1. Get Prediction
        result, confidence = predict_job(job_text)

        # 2. Percentage Normalization Logic
        # Safely handle floats/ints and scale them to a 0.0-100.0 range
        raw_val = float(confidence)
        
        # If the model returns 908, we treat it as 90.8%
        # If it returns 0.9, we treat it as 90.0%
        if raw_val > 100:
            norm_val = raw_val / 10
        elif raw_val <= 1.0:
            norm_val = raw_val * 100
        else:
            norm_val = raw_val

        # 3. Guardrail: Clamp the value to strictly 0-100 to avoid Streamlit crashes
        final_score = max(0.0, min(norm_val, 100.0))
        
        # --- UI Display ---
        st.subheader("Prediction Result")
        if result == "Fake Job":
            st.error(f"⚠ This job looks suspicious ({result})")
        else:
            st.success(f"✅ This job appears legitimate")

        st.metric("Confidence Score", f"{final_score:.2f}%")

        # --- Risk Visualization ---
        st.subheader("Risk Level")
        st.progress(int(final_score)) # Using the clamped score prevents the API Exception

        if final_score > 70:
            st.error("Low Risk Job Posting")
        elif final_score > 50:
            st.warning("Moderate Risk Job Posting")
        else:
            st.success("High Risk Job Posting")

        # --- Keyword Analysis ---
        st.subheader("AI Keyword Analysis")
        suspicious_words = ["payment", "investment", "quick money", "earn fast", "no experience required", "registration fee"]
        found_words = [word for word in suspicious_words if word in job_text.lower()]

        if found_words:
            for word in found_words:
                st.warning(f"⚠ Suspicious keyword detected: {word}")
        else:
            st.success("No suspicious keywords detected")