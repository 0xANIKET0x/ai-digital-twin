# backend/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import datetime

# Initialize the FastAPI app
app = FastAPI(title="AI Digital Twin Backend")

# --- CORS Middleware ---
# This allows our frontend to talk to our backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for simplicity. In production, you'd restrict this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This defines the structure of the data we expect from the frontend
class JournalEntry(BaseModel):
    content: str

# --- API Endpoint ---
@app.post("/entries/")
def create_entry(entry: JournalEntry):
    """
    Receives a new journal entry and saves it to a JSON file.
    """
    DB_FILE = "journal_entries.json"

    try:
        # Try to load existing entries
        with open(DB_FILE, "r") as f:
            entries = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, start a new list
        entries = []

    # Create the new entry data with a timestamp
    new_entry_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "content": entry.content
    }

    entries.append(new_entry_data)

    # Write the updated list back to the file
    with open(DB_FILE, "w") as f:
        json.dump(entries, f, indent=2)

    return {"status": "success", "entry": new_entry_data}
