import os
import requests
import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="GitHub Vibe-Check & Roast", page_icon="🔥", layout="centered")

st.title("🔥 GitHub Profile Auto-Roaster & Vibe Check")
st.write("Enter any public GitHub username to get a brutally honest, AI-powered roast and vibe check!")

# Sidebar for API Key Input
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not api_key and "GEMINI_API_KEY" in os.environ:
    api_key = os.environ["GEMINI_API_KEY"]

def fetch_github_data(username):
    """Fetches public profile and top repositories from GitHub REST API."""
    user_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=6"

    user_res = requests.get(user_url)
    if user_res.status_code != 200:
        return None, "User not found or GitHub API limit reached."

    repos_res = requests.get(repos_url)
    user_data = user_res.json()
    repos_data = repos_res.json() if repos_res.status_code == 200 else []

    summary = {
        "name": user_data.get("name"),
        "username": user_data.get("login"),
        "bio": user_data.get("bio"),
        "public_repos": user_data.get("public_repos"),
        "followers": user_data.get("followers"),
        "following": user_data.get("following"),
        "top_repositories": [
            {
                "name": repo.get("name"),
                "description": repo.get("description"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count"),
                "forks": repo.get("forks_count")
            }
            for repo in repos_data
        ]
    }
    return summary, None

def generate_roast(github_info, key):
    """Generates the roast using Gemini API."""
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-3.8-flash')    
    prompt = f"""
    You are a witty, tech-savvy internet roaster who judges developers based on their GitHub profile.
    Analyze this developer's GitHub profile data:
    {github_info}

    Provide a response in Markdown with the following 3 sections:
    1. 🔥 **The Brutal Roast**: 2-3 funny, sharp, sarcastic sentences about their bio, repo names, star counts, or tech stack.
    2. 🎯 **The Vibe Score**: Give them a funny custom rating out of 100 (e.g. "72/100 - Tutorial Hell Survivor", "88/100 - Unhinged Vibe Coder").
    3. 💡 **Silver Lining**: One genuine, funny compliment about what they actually did right.

    Keep it witty, fast-paced, and filled with internet/tech culture humor!
    """

    response = model.generate_content(prompt)
    return response.text

# UI Layout
username = st.text_input("GitHub Username", placeholder="e.g. torvalds, octocat")

if st.button("🔥 Roast Profile!"):
    if not username.strip():
        st.warning("Please enter a valid GitHub username.")
    elif not api_key:
        st.error("Please enter a Gemini API Key in the sidebar.")
    else:
        with st.spinner("Fetching profile and generating roast..."):
            data, error = fetch_github_data(username.strip())
            if error:
                st.error(error)
            else:
                try:
                    roast_output = generate_roast(data, api_key)
                    st.success("Roast Generated!")
                    st.markdown("---")
                    st.markdown(roast_output)
                except Exception as e:
                    st.error(f"Error generating roast: {str(e)}")