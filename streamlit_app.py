import os
import dotenv
import streamlit as st
from main import get_recommendations

# Retrieve the OpenAI API key from the environment variable
dotenv.load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Setting Up Some Configuration Settings
st.set_page_config(
    page_title='BrandBeats',
    page_icon='🎧',
    layout='wide',
    initial_sidebar_state='collapsed',
)

# Setting Up The Application Landing Page
st.markdown("""
# BrandBeats

###### Find the perfect track for your synch opportunity! 
###### To get started, please provide a detailed project description and upload any relevant images, like mood boards that describe the feeling you're looking for.
###### When ready click the "Submit" button search for recommendations from your catalogue. 
""")

def generate_response(project_description):
    # Use st.spinner to show a loading spinner while the model is working
    with st.spinner("Searching catalogue..."):
        output = get_recommendations(project_description)
        st.write(output)

with st.form('my_form'):
      
    project_description = st.text_area("Project Description", value='', height=200, max_chars=1000)

    images = st.file_uploader("Upload images", type=["jpg", "png"], accept_multiple_files=True)

    submitted = st.form_submit_button('Submit')

    if submitted:
        get_recommendations(project_description)
