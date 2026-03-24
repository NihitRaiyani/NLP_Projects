import streamlit as st
import pickle
import re

# Define category mapping (based on the alphabetical sorting of datasets)
CATEGORY_MAPPING = {
    0: "ACCOUNTANT", 1: "ADVOCATE", 2: "AGRICULTURE", 3: "APPAREL", 4: "ARTS",
    5: "AUTOMOBILE", 6: "AVIATION", 7: "BANKING", 8: "BPO", 9: "BUSINESS-DEVELOPMENT",
    10: "CHEF", 11: "CONSTRUCTION", 12: "CONSULTANT", 13: "DESIGNER",
    14: "DIGITAL-MEDIA", 15: "ENGINEERING", 16: "FINANCE", 17: "FITNESS",
    18: "HEALTHCARE", 19: "HR", 20: "INFORMATION-TECHNOLOGY",
    21: "PUBLIC-RELATIONS", 22: "SALES", 23: "TEACHER"
}

def clean_resume(resume_text):
    """
    Basic text cleaning function commonly used for resume datasets.
    Removes URLs, special characters, punctuations, and extra spaces.
    """
    resume_text = re.sub('http\S+\s*', ' ', resume_text)  # remove URLs
    resume_text = re.sub('RT|cc', ' ', resume_text)  # remove RT and cc
    resume_text = re.sub('#\S+', '', resume_text)  # remove hashtags
    resume_text = re.sub('@\S+', '  ', resume_text)  # remove mentions
    resume_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resume_text)  # remove punctuations
    resume_text = re.sub(r'[^\x00-\x7f]', r' ', resume_text) 
    resume_text = re.sub('\s+', ' ', resume_text)  # remove extra whitespace
    return resume_text

# Load the model and vectorizer
@st.cache_resource
def load_model():
    with open("resume_model.pkl", "rb") as f:
        data = pickle.load(f)
    return data['model'], data['vectorizer']

def main():
    st.set_page_config(page_title="Resume Screening App", page_icon="📄")
    st.title("📄 Resume Screening & Classification App")
    st.write("This is a simple Streamlit web app that predicts the job category of a given resume.")

    try:
        model, vectorizer = load_model()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return

    st.subheader("Enter Resume Text")
    resume_input = st.text_area("Paste the contents of the resume below:", height=250)

    if st.button("Predict Category"):
        if resume_input.strip() == "":
            st.warning("Please enter some text to classify.")
        else:
            # 1. Clean the input text
            cleaned_text = clean_resume(resume_input)
            
            # 2. Vectorize the text
            vectorized_text = vectorizer.transform([cleaned_text])
            
            # 3. Make prediction
            prediction = model.predict(vectorized_text)[0]
            
            # 4. Map integer prediction to readable category
            category_name = CATEGORY_MAPPING.get(prediction, "Unknown Category")
            
            st.success("Prediction Successful!")
            st.markdown(f"### Predicted Job Category: **{category_name}**")

if __name__ == "__main__":
    main()
