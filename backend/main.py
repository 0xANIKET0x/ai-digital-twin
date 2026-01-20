# backend/main.py

from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import datetime

from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

# --- All models and setups are the same. ---
print("Loading all AI models...")
relevance_model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
print("All systems operational.")


app = FastAPI(title="AI Digital Twin Backend v2.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
class JournalEntry(BaseModel): content: str
class AskRequest(BaseModel): question: str
DB_FILE = "journal_entries.json"

def load_entries():
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError): return []

@app.post("/entries/")
def create_entry(entry: JournalEntry):
    # This function remains unchanged.
    entries = load_entries()
    from textblob import TextBlob
    analysis = TextBlob(entry.content)
    if analysis.sentiment.polarity > 0.1: sentiment = "positive"
    elif analysis.sentiment.polarity < -0.1: sentiment = "negative"
    else: sentiment = "neutral"
    new_entry_data = {"timestamp": datetime.datetime.now().isoformat(), "content": entry.content, "sentiment": sentiment}
    entries.append(new_entry_data)
    with open(DB_FILE, "w") as f: json.dump(entries, f, indent=2)
    return {"status": "success", "entry": new_entry_data}

@app.post("/ask/")
def ask_twin(request: AskRequest):
    # The robust "ask" function remains unchanged.
    entries = load_entries()
    if not entries: return {"answer": "My memories are empty right now."}
    entries.sort(key=lambda x: x["timestamp"], reverse=True)
    question_embedding = relevance_model.encode(request.question, convert_to_tensor=True)
    best_entry, highest_combined_score = None, -1.0
    for i, entry in enumerate(entries):
        entry_embedding = relevance_model.encode(entry['content'], convert_to_tensor=True)
        relevance_score = util.pytorch_cos_sim(question_embedding, entry_embedding)[0][0].item()
        timeliness_score = 1.0 / (i + 1)
        combined_score = (0.95 * relevance_score) + (0.05 * timeliness_score)
        if combined_score > highest_combined_score:
            highest_combined_score, best_entry = combined_score, entry
    
    if highest_combined_score < 0.3: return {"answer": "I looked through my memories, but none of them seemed relevant to your question."}
    
    context = best_entry['content']
    result = qa_pipeline(question=request.question, context=context)
    if result['score'] < 0.2: return {"answer": "I found a relevant memory, but I couldn't extract a clear answer from it."}
    
    return {"answer": result['answer']}

# --- ENHANCEMENT: Upgraded endpoint for Date Range Search ---
@app.get("/entries_by_date_range/")
def get_entries_by_date_range(start_date: str = Query(..., description="Start date in YYYY-MM-DD format"), 
                              end_date: str = Query(..., description="End date in YYYY-MM-DD format")):
    entries = load_entries()
    # Add a day to the end_date to make the range inclusive
    end_date_inclusive = (datetime.datetime.strptime(end_date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    filtered_entries = [
        entry for entry in entries 
        if start_date <= entry['timestamp'] < end_date_inclusive
    ]
    return filtered_entries

@app.get("/sentiment_over_time/")
def get_sentiment_over_time():
    # This function remains unchanged.
    entries = load_entries()
    sentiment_data = [{"timestamp": entry['timestamp'], "sentiment": entry['sentiment']} for entry in entries]
    sentiment_data.sort(key=lambda x: x["timestamp"])
    return sentiment_data
