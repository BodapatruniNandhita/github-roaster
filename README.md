# GitHub Roaster

A small Streamlit app that fetches a public GitHub profile and asks Gemini for a playful roast.

## Run locally

1. Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/apikey).
2. Install Python 3.10 or newer.
3. In this folder, install dependencies and start the app:

   ```bash
   python -m pip install -r requirements.txt
   streamlit run app.py
   ```

4. Enter a GitHub username or profile URL and your Gemini API key. The key can instead be configured as `GEMINI_API_KEY` in the environment.

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Sign in at [share.streamlit.io](https://share.streamlit.io/) with the GitHub account that can access the repository.
3. Choose **Create app**, select this repository, the `main` branch, and `app.py`, then deploy.
4. In the deployed app's **Settings** → **Secrets**, add:

   ```toml
   GEMINI_API_KEY = "your-gemini-api-key"
   ```

5. Save the secret and let Streamlit restart the app. Never commit an actual API key to GitHub.

The app uses GitHub's public API without authentication, so GitHub's unauthenticated rate limit applies.
