import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import datetime
import time
import base64
import os

# Set page config
st.set_page_config(
    page_title="Eid Mubarak 2024",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for animations and styling
def set_css():
    st.markdown("""
    <style>
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    
    .eid-title {
        color: #2ecc71;
        text-align: center;
        animation: float 3s ease-in-out infinite;
        font-size: 3em !important;
    }
    
    .greeting-box {
        background: linear-gradient(45deg, #f1c40f, #2ecc71);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-align: center;
    }
    
    .countdown {
        font-size: 2em;
        color: #e74c3c;
        text-align: center;
        margin: 1rem 0;
    }
    
    .eidi-image {
        border: 5px solid #f1c40f;
        border-radius: 15px;
        animation: float 4s ease-in-out infinite;
        margin: 0 auto;
        display: block;
    }
    
    .share-button {
        background-color: #0077b5 !important;
        color: white !important;
        border-radius: 5px;
        padding: 10px 15px;
        text-decoration: none;
        display: inline-block;
        margin-top: 15px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

set_css()

# Background music with stop functionality
def autoplay_audio(file_path: str, stop_after=10):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio id="eidAudio" autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                <script>
                    // Stop audio after {stop_after} seconds
                    setTimeout(() => {{
                        const audio = document.getElementById("eidAudio");
                        if (audio) audio.pause();
                    }}, {stop_after * 1000});
                </script>
                """
            st.markdown(md, unsafe_allow_html=True)
    else:
        st.warning(f"Audio file not found at: {file_path}")

# Eidi image processing
def create_eidi_image(name, amount, template_path="src/eidi_template.JPG"):
    try:
        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)
        
        # Try to load font (with fallback)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
            font.size = 40
        
        # Draw amount text
        amount_text = f"Rs {amount}"
        amount_width = draw.textlength(amount_text, font=font)
        draw.text(
            (img.width//2 - amount_width//2, img.height//2 + 80), 
            amount_text, 
            fill=(255, 215, 0),  # Gold color
            font=font
        )
        
        # Draw name text
        name_text = f"For {name}"
        name_width = draw.textlength(name_text, font=font)
        draw.text(
            (img.width//2 - name_width//2, img.height//2 + 130), 
            name_text, 
            fill=(255, 255, 255),  # White color
            font=font
        )
        
        return img
    except FileNotFoundError:
        st.error("Eidi template image not found!")
        return None

# Countdown timer
def calculate_countdown(target_date):
    now = datetime.datetime.now()
    difference = target_date - now
    return difference

# Main app
def main():
    st.markdown("<h1 class='eid-title'>🌙 Eid Mubarak 2024 🌟</h1>", unsafe_allow_html=True)
    
    # Set Eid date (update accordingly)
    eid_date = datetime.datetime(2024, 6, 17, 0, 0)  # Example date
    
    with st.form("user_info"):
        name = st.text_input("Enter Your Name:", placeholder="Your Name")
        linkedin = st.text_input("Enter LinkedIn Profile URL:", placeholder="https://linkedin.com/in/yourprofile")
        submitted = st.form_submit_button("Get Your Eidi!")
    
    if submitted:
        if not name.strip():
            st.warning("Please enter your name!")
            return
        
        # Start countdown
        countdown_placeholder = st.empty()
        
        while datetime.datetime.now() < eid_date:
            time_left = calculate_countdown(eid_date)
            countdown_text = f"""
            <div class="countdown">
                Time until Eid: {time_left.days} days, {time_left.seconds//3600} hours, 
                {(time_left.seconds//60)%60} minutes, {time_left.seconds%60} seconds
            </div>
            """
            countdown_placeholder.markdown(countdown_text, unsafe_allow_html=True)
            time.sleep(1)
        
        countdown_placeholder.empty()
        
        # Show greeting
        st.balloons()
        autoplay_audio("src/mp3.WAV", stop_after=10)
        
        # Greeting box with LinkedIn share button
        st.markdown(f"""
        <div class="greeting-box">
            <h2>Eid Mubarak, {name}! 🎉</h2>
            <p>May Allah bless you with happiness, peace, and prosperity!</p>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url={linkedin}" 
               target="_blank" 
               class="share-button">
               Share on LinkedIn
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Display Eidi image with personalized message
        st.markdown("<h3 style='text-align: center;'>Your Eidi Gift</h3>", unsafe_allow_html=True)
        
        # Personalized Eidi image
        eidi_img = create_eidi_image(name, 5000)
        if eidi_img:
            st.image(eidi_img, 
                    caption=f"Rs 5000 is for you, {name}!", 
                    use_column_width=True)
        
        # Standard Eidi image
        if os.path.exists("src/eidi-image.PNG"):
            st.image("src/eidi-image.PNG", 
                    caption="Traditional Eidi Gift", 
                    use_column_width=True)
        
        # Confetti animation
        st.components.v1.html("""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
        function fireConfetti() {
            confetti({
                particleCount: 150,
                spread: 70,
                origin: { y: 0.6 },
                colors: ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff']
            });
        }
        
        // Initial burst
        fireConfetti();
        
        // Continue every 3 seconds
        setInterval(fireConfetti, 3000);
        </script>
        """, height=0)

if __name__ == "__main__":
    main()