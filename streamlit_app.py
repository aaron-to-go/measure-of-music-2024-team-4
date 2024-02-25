import os
import streamlit as st
from main import get_recommendations

# Retrieve the OpenAI API key from the environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Setting Up Some Configuration Settings
st.set_page_config(
    page_title='BrandBeats',
    page_icon='🎧',
    layout='centered',
    initial_sidebar_state='collapsed',
)

# Setting Up The Application Landing Page
st.title('BrandBeats :musical_note:')
st.markdown("""
### Find the perfect track for your sync opportunity! 
1. To get started, please provide a detailed description of your project
2. (experimental 🧪) If you have any complimentary images, that describe your project or feeling that you are looking for, you can upload them as well
3. When ready, click the __Search__ button to get recommendations 

""")

def generate_response(project_description):
    # Use st.spinner to show a loading spinner while the model is working
    with st.spinner("🤖 Searching catalogue..."):
        output = get_recommendations(project_description, openai_api_key)
        st.markdown("### Recommendations:")
        st.write(output)

with st.form('my_form'):
      
    project_description = st.text_area("Project Description", value='', height=200, max_chars=1000)

    images = st.file_uploader("Upload images", type=["jpg", "png"], accept_multiple_files=True)

    submitted = st.form_submit_button('Search')

    if submitted:
        generate_response(project_description)
        
st.markdown("""
            Hacked with :heart: by Team 4 at the Measure of Music Hackathon 2024
            
            Ursola Noël | Aaron Dutschmann | Timalka Kalubowila | Osaruyi Enofe | Stephanie Gnahore
            
            Checkout [BrandBeats on GitHub](https://github.com/aaron-to-go/measure-of-music-2024-team-4)
            """)
