def generate_roast(github_info, key):
    """Generates the roast using Gemini API."""
    client = genai.Client(api_key=key)
    
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

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )
    return response.text