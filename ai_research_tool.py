import streamlit as st
import openai

# Set up OpenAI API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to get company research from OpenAI
def research_company(company_name, detailed=False):
    if detailed:
        prompt = f"""
        Provide a detailed, in-depth analysis of {company_name} with the following sections:
        - What the company does
        - Key products or services
        - Industry and competitors
        - Recent news (last 6 months)
        - Executive team
        - Size and location
        - Revenue or funding (if public)
        - Unique aspects
        Format the response with clear section headers using markdown (e.g., ## Section Name) and provide detailed paragraphs for each section. If information is unavailable, say 'Information not readily available.' At the start of the response, include an emoji that represents the company's primary industry (e.g., 🚗 for automotive, 💻 for tech, 🏥 for healthcare).
        """
    else:
        prompt = f"""
        Provide a concise summary of {company_name} with the following sections in a bulleted list format:
        - What the company does (include primary focus and mission)
        - Key products or services (list main offerings with a brief description)
        - Industry and competitors (name industry and 3-4 key competitors)
        - Recent news (last 6 months, include 2-3 key events)
        - Executive team (list CEO, CFO, and one other key executive with titles)
        - Size and location (employee count, HQ location, and major offices)
        - Revenue or funding (if public, latest annual revenue; if private, notable funding rounds)
        - Unique aspects (2-3 distinctive features or achievements)
        Format each section as a markdown bulleted list (e.g., - Item). Keep it clear and concise but informative. If information is unavailable, say 'Information not readily available.' At the start of the response, include an emoji that represents the company's primary industry (e.g., 🚗 for automotive, 💻 for tech, 🏥 for healthcare).
        """
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500 if detailed else 700,
        temperature=0.7
    )
    
    result = response.choices[0].message.content
    lines = result.split('\n')
    emoji = lines[0].strip() if lines and lines[0].strip() else "❓"
    content = '\n'.join(lines[1:]) if len(lines) > 1 else result
    formatted_result = f"<div style='font-size: 3em;'>{emoji}</div>\n\n{content}"
    formatted_result += f"\n\n*Generated using GPT-4o on April 03, 2025*"
    return formatted_result

# Custom CSS for a bright, clean look with visible text and colorful edges
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
        color: #333333;
    }
    .stApp {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        max-width: 900px;
        margin: 20px auto;
        border: 10px solid;
        border-image: linear-gradient(45deg, #3498db, #e74c3c, #2ecc71) 1;
        box-sizing: border-box;
    }
    div[data-testid="stAppViewContainer"] h1 {
        color: #000000 !important;
        font-family: 'Arial', sans-serif;
        font-size: 2em;
        margin-bottom: 10px;
    }
    h3 {
        color: #333333;
    }
    .stTextInput > div > div > input {
        border: 1px solid #3498db;
        border-radius: 5px;
        padding: 8px;
        color: #000000;
        background-color: #ffffff;
    }
    .stButton > button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #2980b9;
    }
    .stSpinner > div {
        color: #3498db;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: #333333;
    }
    .stWarning, .stError {
        color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "company_name" not in st.session_state:
    st.session_state.company_name = ""
if "concise_result" not in st.session_state:
    st.session_state.concise_result = None
if "detailed_result" not in st.session_state:
    st.session_state.detailed_result = None

# Streamlit UI setup
st.markdown("<h1 style='color: #000000;'>AI Company Research Tool</h1>", unsafe_allow_html=True)
st.write("Enter a company name to get a concise summary, with an option for deeper analysis.")

# Input field for company name
company_name = st.text_input("Company Name", placeholder="e.g., Tesla")

# Button to trigger initial research
if st.button("Research"):
    if company_name:
        with st.spinner("Researching... This may take a few seconds."):
            try:
                concise_result = research_company(company_name, detailed=False)
                st.session_state.company_name = company_name
                st.session_state.concise_result = concise_result
                st.session_state.detailed_result = None
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a company name.")

# Display concise results if available
if st.session_state.concise_result:
    st.markdown("### Company Summary")
    st.markdown(st.session_state.concise_result, unsafe_allow_html=True)

    if st.button("More Info"):
        with st.spinner("Fetching detailed analysis..."):
            try:
                detailed_result = research_company(st.session_state.company_name, detailed=True)
                st.session_state.detailed_result = detailed_result
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Display detailed results if available
if st.session_state.detailed_result:
    st.markdown("### Detailed Analysis")
    st.markdown(st.session_state.detailed_result, unsafe_allow_html=True)

# Add a footer
st.write("---")
st.write("Built with Streamlit and OpenAI by a friendly AI assistant.")