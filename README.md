# Indian GK Chatbot (Google Custom Search API + Streamlit GUI)

🤖 A chatbot that answers questions about **Indian Polity, History, and Geography** using the **Google Custom Search API**.

Includes:
- Known facts (e.g., Constitution drafting time, capitals, national symbols).
- A Streamlit web GUI (`gui_streamlit.py`).

## Setup
1. Create a project in **Google Cloud Console**.
2. Enable **Custom Search API** and create an **API Key**.
3. Create a Programmable Search Engine and copy the **Search Engine ID (CX)**.
4. Save credentials in `.env`:

```
API_KEY=your_google_api_key
SEARCH_ENGINE_ID=your_search_engine_id
```

## Run (Terminal)
```bash
pip install -r requirements.txt
python chatbot.py
```

## Run (GUI - Streamlit)
```bash
streamlit run gui_streamlit.py
```
