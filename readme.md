# 🧠 Sentiment Analyzer Project

This project analyzes the mood of user text using AI-based sentiment analysis.  
It cleans the text, detects emotions (happy, neutral, or sad), and responds with a matching emoji and message.  
The system includes preprocessing, polarity adjustment, and mood mapping for more accurate emotional detection.

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Libraries:** TextBlob, Regex, re, Emoji  
- **Frontend (optional):** Streamlit  
- **Version Control:** GitHub  

---

## ⚙️ Setup Guide

Follow these steps to set up and run the project:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/sentiment-analyzer.git
cd sentiment-analyzer
 
2. Create and Activate Virtual Environment
    python -m venv venv
    venv\Scripts\activate       # On Windows
    source venv/bin/activate    # On Mac/Linux

3. Install dependencies
    pip install -r requirements.txt

4. Run the scripts
    streamlit run app.py
    