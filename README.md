# Interviewer Pro 🎙️

An AI-powered interview simulator built with GPT-4o and Streamlit. Practice job interviews for real companies and positions, and get instant AI feedback with a performance score.

## Demo

![Interview Setup](https://via.placeholder.com/800x400?text=Add+a+screenshot+here)

## Features

- **Custom Setup** — Enter your name, experience, skills, target company, position, and seniority level
- **AI Interviewer** — GPT-4o acts as an HR executive and conducts a realistic interview tailored to your profile
- **Streaming Responses** — Answers appear word by word, just like ChatGPT
- **5-Question Interview** — Structured interview with a fixed number of rounds
- **AI Feedback** — After the interview, get an overall score (1–10) and detailed performance feedback
- **Restart Anytime** — Reset and start a new interview with one click

## How It Works

The app has 3 stages:

```
Stage 1 — Setup Form
  Fill in your personal info, target company and position

Stage 2 — Interview Chat
  GPT-4o interviews you based on your profile (5 messages)

Stage 3 — Feedback
  GPT-4o evaluates your performance and gives a score
```

## Tech Stack

- **Python**
- **Streamlit** — UI and chat interface
- **OpenAI GPT-4o** — Interview simulation and feedback generation
- **python-dotenv** — Secure API key management
- **streamlit-js-eval** — Page reload on interview restart

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/ulirotela/hr-interview-chatbot.git
cd hr-interview-chatbot
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv env
source env/bin/activate  # on Windows: env\Scripts\activate
pip install streamlit openai python-dotenv streamlit-js-eval
```

**3. Add your OpenAI API key**

Create a `.env` file in the root folder:
```
OPENAI_API_KEY=your-api-key-here
```

**4. Run the app**
```bash
streamlit run interviewer_pro.py
```

## Project Structure

```
hr-interview-chatbot/
├── interviewer_pro.py   # Main application
├── .env                 # API key (not committed to GitHub)
├── .gitignore
└── README.md
```

## Author

**Uli Rotela** — Junior AI Engineer  
[GitHub](https://github.com/ulirotela) · [LinkedIn](https://linkedin.com/in/ulirotela)
