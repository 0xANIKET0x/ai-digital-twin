# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import datetime
import os

from textblob import TextBlob
import google.generativeai as genai
from dotenv import load_dotenv

# --- NEW: Load environment variables and configure API ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


# Initialize the FastAPI app
app = FastAPI(title="AI Digital Twin Backend")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for data validation ---
class JournalEntry(BaseModel):
    content: str

class AskRequest(BaseModel):
    question: str


DB_FILE = "journal_entries.json"


def get_sentiment(text: str) -> str:
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0.1:
        return "positive"
    elif analysis.sentiment.polarity < -0.1:
        return "negative"
    else:
        return "neutral"

# --- Endpoint for creating entries (Unchanged) ---
@app.post("/entries/")
def create_entry(entry: JournalEntry):
    try:
        with open(DB_FILE, "r") as f:
            entries = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        entries = []
    
    sentiment = get_sentiment(entry.content)
    new_entry_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "content": entry.content,
        "sentiment": sentiment
    }
    entries.append(new_entry_data)

    with open(DB_File, "w") as f:
        json.dump(entries, f, indent=2)

    return {"status": "success", "entry": new_entry_data}


# --- NEW: The "Brain" of the Digital Twin ---
@app.post("/ask/")
def ask_twin(request: AskRequest):
    """
    Answers a user's question based on their journal entries.
    """
    try:
        with open(DB_FILE, "r") as f:
            entries = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"answer": "I don't seem to have any memories yet. Please write a journal entry first."}

    # For now, let's use the 10 most recent entries as context.
    # We can make this smarter later (e.g., with vector search).
    context_entries = sorted(entries, key=lambda x: x["timestamp"], reverse=True)[:10]
    context = "\n".join([f"- On {e['timestamp']}, I wrote: '{e['content']}' (Sentiment: {e['sentiment']}) " for e in context_entries])

    # This is the prompt that tells the AI how to behave.
    prompt = f"""
    You are my AI Digital Twin. Your task is to answer the following question based ONLY on the context provided from my past journal entries.
    You must adopt a first-person perspective, using "I" and "me".
    Reflect on the memories provided. Do not mention that you are an AI.
    If the context is insufficient to answer the question, respond with something like "I don't seem to have enough memories about that to give a good answer."

    CONTEXT FROM JOURNAL:
    {context}

    QUESTION:
    "{request.question}"

    Answer:
    """

    try:
        # Call the Gemini API
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        return {"answer": response.text}
    except Exception as e:
        print(f"Error calling Generative AI: {e}")
        return {"answer": "I'm having trouble accessing my memories right now. Please try again later."}

