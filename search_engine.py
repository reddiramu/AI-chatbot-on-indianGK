import os
import re
import requests
from typing import Tuple, Optional
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

KNOWN_FACTS = [
    (r"\bhow\s+many\s+days\b.*\b(indian\s+constitution|constitution\s+of\s+india)\b",
     "The Constituent Assembly took **2 years, 11 months, and 18 days** to complete the Constitution of India."),
    (r"\bwhen\b.*\bindia.*independence\b",
     "India gained independence on **15 August 1947**."),
    (r"\bfather\b.*\b(indian\s+constitution|constitution\s+of\s+india)\b",
     "Dr. B. R. Ambedkar is regarded as the **chief architect (father)** of the Constitution of India."),
    (r"\bcapital of india\b", "The capital of India is **New Delhi**."),
    (r"\blongest river\b.*india\b", "The longest river in India is the **Ganga (Ganges)**, about 2,525 km long."),
    (r"\bhighest mountain\b.*india\b", "The highest mountain peak in India is **Kangchenjunga**, at 8,586 m."),
    (r"\bnational animal of india\b", "The national animal of India is the **Bengal Tiger**."),
    (r"\bnational bird of india\b", "The national bird of India is the **Indian Peacock**."),
    (r"\bnational flower of india\b", "The national flower of India is the **Lotus**."),
    (r"\bnational anthem of india\b", "The national anthem of India is **Jana Gana Mana**."),
    (r"\bnational song of india\b", "The national song of India is **Vande Mataram**."),
    (r"\bnational currency of india\b", "The national currency of India is the **Indian Rupee (₹)**."),
    (r"\bfirst prime minister of india\b", "The first Prime Minister of India was **Jawaharlal Nehru**."),
    (r"\bfirst president of india\b", "The first President of India was **Dr. Rajendra Prasad**."),
    (r"\bquit india movement\b", "The Quit India Movement was launched on **8 August 1942**."),
    (r"\bjallianwala bagh massacre\b", "The Jallianwala Bagh massacre took place on **13 April 1919** in Amritsar."),
    (r"\b1857 revolt\b", "The Revolt of 1857, also known as the **First War of Indian Independence**, began in Meerut."),
]

SMALL_TALK = [
    (r"^(hi|hello|hey)\b", "Hello! Ask me anything about Indian polity, history, or geography."),
    (r"\bwhat('?| i)s your name\??", "I’m your Indian GK Chatbot, powered by Google Search."),
    (r"\bwho\s+are\s+you\??", "I’m a search-powered assistant focused on Indian polity, history, and geography."),
]

PREFERRED_DOMAINS = [
    "wikipedia.org", "britannica.com", "prsindia.org", "india.gov.in",
    "pib.gov.in", "ncert.nic.in", "nios.ac.in",
]

def _match_rules(query: str, rules) -> Optional[str]:
    q = query.strip().lower()
    for pattern, answer in rules:
        if re.search(pattern, q):
            return answer
    return None

def _bias_query(query: str) -> str:
    if not re.search(r"\b(india|indian|bharat)\b", query, flags=re.IGNORECASE):
        query = f"{query} India"
    return query

def _site_biased_queries(query: str):
    yield query + " site:wikipedia.org"
    yield query + " site:prsindia.org"
    yield query + " site:britannica.com"
    yield query + " site:india.gov.in"
    yield query

def _pick_best_item(items):
    def score(item):
        link = item.get("link", "")
        s = 0
        for d in PREFERRED_DOMAINS:
            if d in link:
                s += 10
        if item.get("snippet"):
            s += 1
        return -s
    if not items:
        return None
    best = sorted(items, key=lambda it: -score(it))[0]
    return best

def google_search(query: str, num_results: int = 5) -> Tuple[str, Optional[str]]:
    if not API_KEY or not SEARCH_ENGINE_ID:
        return "API key / search engine ID missing. Please set API_KEY and SEARCH_ENGINE_ID in .env.", None
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query, "key": API_KEY, "cx": SEARCH_ENGINE_ID, "num": num_results}
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
    except Exception:
        return "Network error while contacting Google Search.", None
    items = data.get("items", [])
    if not items:
        return "Sorry, I couldn't find an answer.", None
    top = _pick_best_item(items) or items[0]
    snippet = top.get("snippet", "No snippet available")
    link = top.get("link", "")
    return snippet, link

def smart_answer(user_query: str) -> Tuple[str, Optional[str]]:
    st = _match_rules(user_query, SMALL_TALK)
    if st:
        return st, None
    kf = _match_rules(user_query, KNOWN_FACTS)
    if kf:
        return kf, None
    biased = _bias_query(user_query)
    for q in _site_biased_queries(biased):
        ans, url = google_search(q, num_results=5)
        if "couldn't find" not in ans.lower() and "missing" not in ans.lower():
            return ans, url
    return "Sorry, I couldn't find an answer.", None
