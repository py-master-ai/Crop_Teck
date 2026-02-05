import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image
from pathlib import Path
import requests

st.set_page_config(page_title="Crop Teck", page_icon="leaf", layout="wide")

hide_streamlit_style = """ 
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["Home", "Learn", "Phone", "About"],
    orientation="horizontal",
)

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

if selected == "Home":

    # LOGO.
    st.subheader("Farming the Smart Way", divider=True)
    logo = current_dir / "assets" / "logo.jpeg"
    logo = Image.open(logo)

    st.image(logo, width=500)

    api_url = "http://leaf-diseases-detect.vercel.app"

    col1, col2 = st.columns([1, 2], border=True)
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Leaf Image", type=["jpg", "jpeg", "png"], label_visibility="hidden")

        if uploaded_file is not None:
            st.image(uploaded_file, caption="Preview")

    with col2:
        if uploaded_file is not None:
            if st.button("🔍 Click to Detect Disease!", use_container_width=False, help="Internet Connection required"):
                with st.spinner("Analyzing image and contacting API..."):
                    try:
                        files = {
                            "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        response = requests.post(
                            f"{api_url}/disease-detection-file", files=files)
                        if response.status_code == 200:
                            result = response.json()

                            # Check if it's an invalid image
                            if result.get("disease_type") == "invalid_image":
                                st.markdown("<div class='result-card'>",
                                            unsafe_allow_html=True)
                                st.markdown(
                                    "<div class='disease-title'>⚠️ Invalid Image</div>", unsafe_allow_html=True)
                                st.markdown(
                                    "<div style='color: #ff5722; font-size: 1.1em; margin-bottom: 1em;'>Please upload a clear image of a plant leaf for accurate disease detection.</div>",
                                    unsafe_allow_html=True)

                                # Show the symptoms (which contain the error message)
                                if result.get("symptoms"):
                                    st.markdown(
                                        "<div class='section-title'>Issue</div>", unsafe_allow_html=True)
                                    st.markdown("<ul class='symptom-list'>",
                                                unsafe_allow_html=True)
                                    for symptom in result.get("symptoms", []):
                                        st.markdown(
                                            f"<li>{symptom}</li>", unsafe_allow_html=True)
                                    st.markdown("</ul>", unsafe_allow_html=True)

                                # Show treatment recommendations
                                if result.get("treatment"):
                                    st.markdown(
                                        "<div class='section-title'>What to do</div>", unsafe_allow_html=True)
                                    st.markdown("<ul class='treatment-list'>",
                                                unsafe_allow_html=True)
                                    for treat in result.get("treatment", []):
                                        st.markdown(
                                            f"<li>{treat}</li>", unsafe_allow_html=True)
                                    st.markdown("</ul>", unsafe_allow_html=True)

                                st.markdown("</div>", unsafe_allow_html=True)

                            elif result.get("disease_detected"):
                                st.markdown("<div class='result-card'>",
                                            unsafe_allow_html=True)
                                st.markdown(
                                    f"<div class='disease-title'>🦠 {result.get('disease_name', 'N/A')}</div>",
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f"<span class='info-badge'>Type: {result.get('disease_type', 'N/A')}</span>",
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f"<span class='info-badge'>Severity: {result.get('severity', 'N/A')}</span>",
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f"<span class='info-badge'>Confidence: {result.get('confidence', 'N/A')}%</span>",
                                    unsafe_allow_html=True)
                                st.markdown(
                                    "<div class='section-title'>Symptoms</div>", unsafe_allow_html=True)
                                st.markdown("<ul class='symptom-list'>",
                                            unsafe_allow_html=True)
                                for symptom in result.get("symptoms", []):
                                    st.markdown(
                                        f"<li>{symptom}</li>", unsafe_allow_html=True)
                                st.markdown("</ul>", unsafe_allow_html=True)
                                st.markdown(
                                    "<div class='section-title'>Possible Causes</div>", unsafe_allow_html=True)
                                st.markdown("<ul class='cause-list'>",
                                            unsafe_allow_html=True)
                                for cause in result.get("possible_causes", []):
                                    st.markdown(
                                        f"<li>{cause}</li>", unsafe_allow_html=True)
                                st.markdown("</ul>", unsafe_allow_html=True)
                                st.markdown(
                                    "<div class='section-title'>Treatment</div>", unsafe_allow_html=True)
                                st.markdown("<ul class='treatment-list'>",
                                            unsafe_allow_html=True)
                                for treat in result.get("treatment", []):
                                    st.markdown(
                                        f"<li>{treat}</li>", unsafe_allow_html=True)
                                st.markdown("</ul>", unsafe_allow_html=True)
                                st.markdown(
                                    f"<div class='timestamp'>🕒 {result.get('analysis_timestamp', 'N/A')}</div>",
                                    unsafe_allow_html=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                            else:
                                # Healthy leaf case
                                st.markdown("<div class='result-card'>",
                                            unsafe_allow_html=True)
                                st.markdown(
                                    "<div class='disease-title'>✅ Healthy Leaf</div>", unsafe_allow_html=True)
                                st.markdown(
                                    "<div style='color: #4caf50; font-size: 1.1em; margin-bottom: 1em;'>No disease detected in this leaf. The plant appears to be healthy!</div>",
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f"<span class='info-badge'>Status: {result.get('disease_type', 'healthy')}</span>",
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f"<span class='info-badge'>Confidence: {result.get('confidence', 'N/A')}%</span>",
                                    unsafe_allow_html=True)
                                st.markdown(
                                    f"<div class='timestamp'>🕒 {result.get('analysis_timestamp', 'N/A')}</div>",
                                    unsafe_allow_html=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            st.error(f"API Error: {response.status_code}")
                            st.write(response.text)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

elif selected == ("Learn"):

    st.subheader("Be Agri-SMART", divider=True)
    st.video("https://www.youtube.com/watch?v=oVg6ycY3eXQ&t=17s&pp=ygUfa2VueWEgY3JvcCBkaXNlYXNlcyBsZWFmIGNvdXJzZQ%3D%3D")
    st.video("https://www.youtube.com/watch?v=7w3anrCnm9Y&pp=ygUiY3JvcCBkaXNlYXNlcyBsZWFmIGNvdXJzZSBpbiBrZW55YQ%3D%3D")


elif selected == "Contact":
    st.info("Call/WhatsApp: +254712345678")

elif selected == "About":

    st.info("Crop Teck v1.0.0")



