# AI Digital Twin v3.0

**A full-stack, locally-run AI journaling application that allows you to have conversations with your past self.**

This project is an intelligent, personal journaling system. It not only stores your daily thoughts but also analyzes their mood and, most importantly, allows you to ask questions in plain English to reflect on your past experiences. The entire AI pipeline runs locally, ensuring your data remains completely private.

![AI Digital Twin Screenshot](https://i.imgur.com/aIvGM9l.png)

---

## ✨ Features

- **AI-Powered Chat:** Converse with an AI twin that has learned from your journal entries to answer questions about your past.
- **Advanced Relevance Search:** Uses a two-stage AI architecture (Relevance Search + Answer Extraction) to find the most accurate answers.
- **Sentiment Analysis:** Automatically detects if an entry is positive, negative, or neutral.
- **Interactive Mood Timeline:** Visualize your mood trends over time with an interactive chart.
- **Date Range Search:** Easily find and review all journal entries written within a specific start and end date.
- **Modern, Responsive UI:** A beautiful, glassmorphism-inspired interface with a default dark mode and a light mode option.
- **100% Local & Private:** All AI models run directly on your machine. Your journal entries never leave your computer.

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Transformers, PyTorch, Sentence-Transformers, spaCy
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **AI Models:**
  - `multi-qa-MiniLM-L6-cos-v1` (for relevance search)
  - `distilbert-base-cased-distilled-squad` (for question-answering)

---

## 🚀 Setup and Installation

Follow these steps to run the project on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-digital-twin.git
cd ai-digital-twin
```

### 2. Set Up the Backend

Navigate to the backend directory, create a virtual environment, activate it, and install the required packages.

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install all required packages from the requirements file
pip install -r requirements.txt

# Download the spaCy model
python -m spacy download en_core_web_sm
```

### 3. Run the Backend Server

Once the installation is complete, start the FastAPI server from the `backend` directory.

```bash
uvicorn main:app --reload
```
The server will start, and you will see it begin to download and load the AI models. This may take several minutes on the first run. Wait until you see the message `All systems operational.`

### 4. Launch the Frontend

- Navigate to the `frontend` folder in your file explorer.
- Open the `index.html` file in your preferred web browser (e.g., Chrome, Firefox).

You can now use your AI Digital Twin!

---

## 💡 Future Improvements

- **Cloud Deployment:** Containerize the application with Docker and deploy it to a cloud service.
- **User Authentication:** Add a login system to support multiple users.
- **Enhanced Knowledge Graph:** Fine-tune a model or use a more advanced architecture to understand relationships (e.g., knowing "Python" is a "language").
