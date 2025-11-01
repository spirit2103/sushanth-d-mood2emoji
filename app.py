import streamlit as st
from textblob import TextBlob
from textblob.sentiments import PatternAnalyzer
from better_profanity import profanity
import re

# -----------------------------
# Setup: profanity & page
# -----------------------------
profanity.load_censor_words()
profanity.add_censor_words(['idiot', 'stupid', 'dumb', 'kill', 'fool'])

st.set_page_config(page_title="🎭 Mood2Emoji", page_icon="😊", layout="centered")

st.markdown(
    """
    <h1 style='text-align: center; color: #4C4CFF;'>🎭 Mood2Emoji</h1>
    <p style='text-align: center; color: #666;'>
    Type how you feel and get a little emoji friend & message for your mood 💬
    </p>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# SIDEBAR: Teacher Mode
# -----------------------------
with st.sidebar:
    st.header("👩‍🏫 Teacher Mode")
    show_teacher_mode = st.checkbox("Show Teacher Info")

    if show_teacher_mode:
        st.markdown(
            """
            ### 🧠 About the Project
            **Mood2Emoji** is an educational emotion detection app built for young learners (ages 12–16).  
            It helps students express how they feel through short text input and instantly visualizes their emotion using emojis and kind responses.  
            The system encourages emotional awareness, digital empathy, and safe communication online.

            ---

            ### ⚙️ How It Works – Data Flow
            Below is the visual data flow of how the Mood2Emoji app processes student input 👇
            """,
            unsafe_allow_html=True,
        )

        # -----------------------------
        # Data Flow Diagram (Mermaid)
        # -----------------------------
        st.markdown(
            """
            ```mermaid
            flowchart TD
                A[🧑 User Input] --> B[🧹 Text Preprocessing<br/>(Contraction Expansion + Profanity Filter)]
                B --> C[🧠 Sentiment Analyzer<br/>(PatternAnalyzer - TextBlob)]
                C --> D[⚖️ Polarity Adjustment<br/>(Negation & Keyword Rules)]
                D --> E[🎭 Mood Mapping<br/>(Happy / Neutral / Sad)]
                E --> F[😊 Emoji & Message Output]
            ```
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            **Step-by-step Explanation:**
            1. **User Input:** Students enter a text message expressing their mood.  
            2. **Text Preprocessing:** Cleans text, expands contractions (e.g., *don’t → do not*), and checks for bad words.  
            3. **Sentiment Analyzer:** Uses TextBlob’s PatternAnalyzer to detect sentiment polarity (-1 to +1).  
            4. **Polarity Adjustment:** Enhances accuracy using custom negation and emotional keyword rules.  
            5. **Mood Mapping:** Maps polarity to mood categories (positive, neutral, negative).  
            6. **Output Stage:** Displays emoji and motivational message with color-coded feedback.

            ---

            ### 🌟 Key Features
            - 🧩 **AI-based Emotion Detection** using PatternAnalyzer.  
            - 🧠 **Negation & Contraction Handling** for natural text.  
            - 🚫 **Profanity Filtering** for classroom safety.  
            - 🎨 **Dynamic Emoji & Color Feedback.**  
            - 💬 **Positive Reinforcement Messages.**  
            - 👩‍🏫 **Teacher Mode Dashboard** with explanation & DFD.  
            - 🌈 Designed for **Digital Emotional Literacy**.

            ---

            💡 *This app shows how simple NLP techniques can help students identify and express emotions safely and positively.*
            """,
            unsafe_allow_html=True,
        )

# -----------------------------
# Contractions map + helper
# -----------------------------
CONTRACTIONS = {
    "ain't": "is not", "aren't": "are not", "can't": "cannot", "couldn't": "could not",
    "didn't": "did not", "doesn't": "does not", "don't": "do not", "hadn't": "had not",
    "hasn't": "has not", "haven't": "have not", "he's": "he is", "she's": "she is",
    "it's": "it is", "i'm": "i am", "isn't": "is not", "let's": "let us",
    "mightn't": "might not", "mustn't": "must not", "shan't": "shall not",
    "shouldn't": "should not", "wasn't": "was not", "weren't": "were not",
    "won't": "will not", "wouldn't": "would not", "we're": "we are",
    "they're": "they are", "you're": "you are", "i've": "i have", "we've": "we have",
    "they've": "they have", "who's": "who is", "what's": "what is",
    "where's": "where is", "there's": "there is", "that's": "that is",
    "could've": "could have", "would've": "would have", "should've": "should have",
    "can't've": "cannot have", "y'all": "you all"
}

_contr_pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in CONTRACTIONS.keys()) + r')\b', flags=re.IGNORECASE)

def expand_contractions(text: str) -> str:
    def repl(m):
        key = m.group(0).lower()
        return CONTRACTIONS.get(key, key)
    return _contr_pattern.sub(repl, text)

# -----------------------------
# Negation rule helpers
# -----------------------------
_negation_positive_pattern = re.compile(
    r'\b(do not|does not|did not|not|never|no|cannot|can not|won not|will not)\b.*\b('
    r'happy|like|love|enjoy|enjoyed|good|great|awesome|fun|excited|win|won|pass|passed'
    r')\b', flags=re.IGNORECASE)

_negation_negative_pattern = re.compile(
    r'\b(do not|does not|did not|not|never|no|cannot|can not|won not|will not)\b.*\b('
    r'sad|hate|dislike|angry|upset|cry|hurt|bad|bored|tired|alone|scared|fail|failed|lost'
    r')\b', flags=re.IGNORECASE)

# -----------------------------
# Input + Main logic
# -----------------------------
user_text = st.text_area(
    "💭 How are you feeling today?",
    placeholder="Type something like 'I'm feeling amazing' or 'I didn't enjoy the game'",
    height=120
)

if st.button("✨ Show My Mood"):
    if user_text.strip() == "":
        st.warning("⚠️ Please type something first.")
    else:
        if profanity.contains_profanity(user_text):
            st.error("🚫 Oops! Please use some humble words 💖")
        else:
            expanded = expand_contractions(user_text)

            blob = TextBlob(expanded, analyzer=PatternAnalyzer())
            polarity = blob.sentiment[0]

            positive_words = [
                "won", "victory", "passed", "achieved", "celebrated",
                "amazing", "awesome", "great", "good", "excited", "fun",
                "love", "enjoyed", "happy", "proud", "win", "success"
            ]
            negative_words = [
                "lost", "failed", "sad", "angry", "upset", "cry", "hurt",
                "bad", "bored", "tired", "alone", "scared", "lose", "failure"
            ]

            text_lower = expanded.lower()
            if any(word in text_lower for word in positive_words):
                polarity = max(polarity, 0.4)
            elif any(word in text_lower for word in negative_words):
                polarity = min(polarity, -0.4)

            if _negation_positive_pattern.search(expanded):
                polarity = min(polarity, -0.5)
            elif _negation_negative_pattern.search(expanded):
                polarity = max(polarity, 0.5)

            polarity = max(-1, min(1, polarity))

            if polarity > 0.5:
                emoji = "😄"
                bg_color = "#4CAF50"
                message = "Yay! You seem really happy! Keep spreading those positive vibes 🌟"
            elif polarity > 0:
                emoji = "🙂"
                bg_color = "#8BC34A"
                message = "You look happy today! Stay cheerful and share a smile 😄"
            elif polarity == 0:
                emoji = "😐"
                bg_color = "#FFC107"
                message = "Feeling neutral is okay. Maybe do something fun to brighten your day 🌈"
            elif polarity > -0.5:
                emoji = "🙁"
                bg_color = "#FF9800"
                message = "A little sad? That’s okay. Every day won’t be perfect, but you’re doing great 💪"
            else:
                emoji = "😢"
                bg_color = "#F44336"
                message = "Oh no! You seem really down. Remember, tough times don’t last — you’re strong 💖"

            st.markdown(
                f"""
                <div style='text-align: center; padding: 40px; background-color: {bg_color};
                border-radius: 25px; color: white; margin-top: 25px;'>
                    <div style='font-size: 120px; line-height: 1;'>{emoji}</div>
                    <p style='font-size: 18px; margin-top: 15px; color: #fff;'>{message}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown(
    """
    <br><hr><p style='text-align: center; color: #999; font-size: 14px;'>
    🌈 Built for young learners (12–16) — Learn emotions safely & stay positive!
    </p>
    """,
    unsafe_allow_html=True,
)
