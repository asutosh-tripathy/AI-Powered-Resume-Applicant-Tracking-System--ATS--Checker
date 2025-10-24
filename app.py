import os
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model (v1 API)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

st.set_page_config(page_title="Resume Cabin", page_icon=":robot:", layout="wide")

# Background and styling (unchanged)
page_bg_img = """<style> ... </style>"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("Resume Check: Instantly Check Your Resume for 30+ Issues")
st.write("Improve Your Resume ATS Score")

st.subheader("Paste the Job Description")
jd = st.text_area("", height=150)

st.subheader("Upload Your Resume")
uploaded_file = st.file_uploader("", type="pdf", help="Please upload the PDF")

submit = st.button("Check ATS Score")

if submit:
    if uploaded_file is not None:
        reader = pdf.PdfReader(uploaded_file)
        extracted_text = "".join([p.extract_text() for p in reader.pages])

        input_prompt = f"""
        You are an advanced and highly experienced Applicant Tracking System...
        Resume: {extracted_text}
        Description: {jd}

        I want the only response in 4 sectors as follows:
        • Job Description Match:
        • Missing Keywords:
        • Profile Summary:
        • Personalized suggestions for skills, keywords and achievements that can enhance the provided resume:
        • Application Success rates:
        """

        response = model.generate_content(input_prompt)
        st.subheader("Analysis Result")
        st.write(response.text)
    else:
        st.error("Please upload a resume to continue.")
