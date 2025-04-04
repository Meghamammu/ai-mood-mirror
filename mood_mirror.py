import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
import urllib.parse

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit App Config
st.set_page_config(page_title="AI Mood Mirror", page_icon="🪞")
st.title("🪞 AI Mood Mirror")
st.subheader("Type your vibe. Get your reflection.")

# User input
user_mood = st.text_area("How are you feeling today?", placeholder="e.g. I feel like a soggy cereal.")
mood_style = st.radio("Choose your vibe style:", ["Motivate Me", "Roast Me", "Make It Poetic"])

# Prompt generator
def get_prompt(mood, style):
    if style == "Motivate Me":
        return f"""You're a realistic but uplifting life coach who mixes truth with humor. 
The user says: '{mood}'.
Respond with a motivational message that's fun, human, and slightly self-aware. 
Keep it under 3 sentences. Be the friend who hypes them up without pretending life is perfect."""

    elif style == "Roast Me":
        return f"""You're a viral meme lord AI with savage roast skills and chaotic Gen Z energy. 
The user says: '{mood}'.
Roast them in a clever, meme-worthy way — use cursed metaphors, fake horoscopes, absurd comparisons, or mild chaos.
Don't be offensive, don't mention gender. Keep it under 2 sentences. Make it sound like something someone would post on Twitter or Threads."""

    else:
        return f"""You're an artistic AI poet with a love for metaphors and surprise beauty. 
The user says: '{mood}'.
Respond with a short poem (max 3 lines) that captures their mood — sometimes deep, sometimes beautiful, sometimes hilariously poetic.
Use haikus, rhymes, or lyrical metaphors. Think Shakespeare meets Tumblr meets Internet sadboi energy."""

# Button click logic
if st.button("Reflect My Mood"):
    if not user_mood.strip():
        st.warning("Please enter your mood first!")
    else:
        with st.spinner("Reflecting your vibe..."):
            try:
                # Generate GPT response
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": get_prompt(user_mood, mood_style)}],
                    temperature=0.9,
                    max_tokens=100
                )
                reflection = response.choices[0].message.content.strip()

                # Display emoji heading
                if "Roast Me" in mood_style:
                    st.markdown("😈 **Here’s your reflection:**")
                elif "Poetic" in mood_style:
                    st.markdown("🎭 **Here’s your reflection:**")
                else:
                    st.markdown("💪 **Here’s your reflection:**")

                # Show GPT output
                st.markdown(f"**{reflection}**")

                # URL-encoded version for sharing
                tweet_text = urllib.parse.quote(reflection)

                # Twitter share link
                twitter_url = f"https://twitter.com/intent/tweet?text={tweet_text}%20%23AIMoodMirror"

                # Instagram – dummy link or your Insta profile
                instagram_url = "https://www.instagram.com/yourprofile"  # Change this to your Insta page

                # Show share buttons
                st.markdown("---")
                st.markdown("**📣 Share your vibe:**")
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"[![Twitter](https://img.icons8.com/color/48/twitter.png)]({twitter_url})", unsafe_allow_html=True)

                with col2:
                    st.markdown(f"[![Instagram](https://img.icons8.com/color/48/instagram-new.png)]({instagram_url})", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
