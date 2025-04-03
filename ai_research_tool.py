import streamlit as st
import openai

# DEBUG: Check secrets content (remove this after debugging)
st.write("DEBUG: st.secrets contents", st.secrets)

# Retrieve the API key safely
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error(
        "OpenAI API key not found! Please ensure your secrets are set correctly. "
        "For local development, add a file named '.streamlit/secrets.toml' with:\n\n"
        "OPENAI_API_KEY = \"your-secret-api-key-here\"\n\n"
        "If using Streamlit Cloud, set your secrets in the Cloud interface."
    )
    st.stop()

openai.api_key = api_key

# Your existing code continues here...
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
        model="gpt-4",
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
    formatted_result += f"\n\n*Generated using GPT-4 on April 03, 2025*"
    return formatted_result

# The rest of your Streamlit UI code goes here...
