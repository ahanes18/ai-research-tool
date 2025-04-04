import streamlit as st
import openai

# Retrieve the API key safely without printing it
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error(
        "OPENAI_API_KEY not found in st.secrets! Ensure your secrets are set up correctly."
    )
    st.stop()

openai.api_key = api_key

def research_company(company_name, detailed=False):
    if detailed:
        prompt = f"""
        Using your real-time search capabilities, fetch current and verified data (up-to-date as of 2025) by referencing the company's official website and reliable business sources. Now, in Deep Research Mode, provide a comprehensive and in-depth analysis of {company_name}. Include detailed insights on the company's business strategy, market positioning, financial performance, and future outlook. Include the following sections:

        ## Company Overview
        Describe what the company does and its core business model.

        ## Products & Services
        List key products or services with detailed descriptions and mention any recent innovations.

        ## Industry & Competitors
        Analyze the industry, the company's market position, and list 3-4 major competitors with comparisons.

        ## Recent News & Developments
        Summarize major news and developments from the last 6 months (only include news from 2024-2025; exclude outdated info such as from 2021).

        ## Executive Team
        Search for and verify current C-level executive details directly from the company's official website and reliable sources. If you cannot fully verify, append the note: "This might be outdated, please reference the company's official website:" followed by the URL if available. List the CEO and other key executives (e.g., CFO, CTO).

        ## Deep Analysis & Insights
        Provide a deep dive into the company's business strategy, recent financial performance, competitive advantages, risks, and future outlook.

        ## Size & Location
        Provide employee count, headquarters location, and any significant office locations.

        ## Revenue/Funding
        Detail the latest annual revenue (if public) or notable funding rounds (if private).

        ## Marketing Data
        Present recent marketing data, including ad spend, the breakdown of digital vs. traditional marketing, and any notable campaigns or assets.

        ## Unique Aspects
        Highlight 2-3 distinctive features or achievements that set the company apart.

        Format your response with clear markdown section headers (e.g., ## Section Name) and detailed paragraphs. If any information is unavailable, state "Information not readily available." Begin with an emoji representing the company's primary industry (e.g., 🚗, 💻, 🏥).
        """
    else:
        prompt = f"""
        Using your real-time search capabilities and by referencing the company's official website and reliable sources, provide a concise summary of {company_name} (up-to-date as of 2025) with the following items (format each as a markdown bullet):
        - **Company Overview:** What the company does and its primary mission.
        - **Products & Services:** Key offerings with a brief description.
        - **Industry & Competitors:** The industry and 3-4 major competitors.
        - **Recent News:** 2-3 key events from the last 6 months (only include news from 2024-2025; avoid outdated info such as from 2021).
        - **Executive Team:** List the current CEO, CFO, and one other key executive. Verify these details by referencing the company's official website. If you cannot fully verify, append the note: "This might be outdated, please reference the company's official website:" with the URL if available.
        - **Size & Location:** Employee count, headquarters, and major offices.
        - **Revenue/Funding:** Latest annual revenue (if public) or notable funding rounds.
        - **Marketing Data:** A summary of recent marketing data including ad spend, digital vs. traditional breakdown, and any available marketing assets or campaign examples.
        - **Unique Aspects:** 2-3 distinctive features or achievements.

        Begin your response with an emoji representing the company's primary industry (e.g., 🚗, 💻, 🏥). If any information is unavailable, say "Information not readily available."
        """
    
    response = openai.chat.completions.create(
        model="gpt-4o",  # Using GPT-4o with real-time search capabilities
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful research assistant with real-time search capabilities. "
                    "Use the web—especially the official company website—to verify all information, particularly C-level executive data. "
                    "If you cannot fully verify the current data, include the note: 'This might be outdated, please reference the company's official website:' followed by the URL if available. "
                    "Ensure all news and data are current as of 2025."
                )
            },
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500 if detailed else 700,
        temperature=0.7
    )
    
    result = response.choices[0].message.content
    lines = result.split('\n')
    emoji = lines[0].strip() if lines and lines[0].strip() else "❓"
    content = '\n'.join(lines[1:]) if len(lines) > 1 else result
    formatted_result = f"<div style='font-size: 1em;'>{emoji}</div>\n\n{content}"
    formatted_result += "\n\n*Generated using ChatGPT 4o with real-time search capabilities*"
    return formatted_result

# Custom CSS for a bright, clean look and mobile responsiveness
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
    /* Override markdown header sizes to match regular text */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
         font-size: 1em !important;
         margin: 0 !important;
         padding: 0 !important;
    }
    /* Further reduce header sizes on small screens */
    @media only screen and (max-width: 600px) {
         .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
              font-size: 0.9em !important;
         }
    }
    .stWarning, .stError {
        color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color: #000000;'>AI Company Research Tool</h1>", unsafe_allow_html=True)
st.write("Enter a company name to get a concise summary, with an option for deep research.")

company_name = st.text_input("Company Name", placeholder="e.g., Tesla")

if st.button("Research"):
    if company_name:
        with st.spinner("Researching... This may take a few seconds."):
            try:
                concise_result = research_company(company_name, detailed=False)
                st.session_state.company_name = company_name
                st.session_state.concise_result = concise_result
                st.session_state.detailed_result = None  # Reset deep research result
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a company name.")

if st.session_state.get("concise_result"):
    tabs = st.tabs(["Company Summary", "Deep Research"])
    
    with tabs[0]:
        st.markdown("### Company Summary")
        st.markdown(st.session_state.concise_result, unsafe_allow_html=True)
    
    with tabs[1]:
        if st.session_state.get("detailed_result") is None:
            with st.spinner("Fetching deep research..."):
                try:
                    detailed_result = research_company(st.session_state.company_name, detailed=True)
                    st.session_state.detailed_result = detailed_result
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        # Set the deep research content font color to a darker shade (black)
        st.markdown("<div style='color: #000000;'>### Detailed Analysis (Deep Research Mode)</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='color: #000000;'>{st.session_state.detailed_result}</div>", unsafe_allow_html=True)

st.write("---")
st.write("Built with Streamlit and OpenAI by a friendly AI assistant.")
