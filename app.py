import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import datetime
import time
import base64
import os

# Set page config
st.set_page_config(
    page_title="Eid Mubarak 2025",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for animations and styling
# Custom CSS for animations and styling
def set_css():
    st.markdown("""
    <style>
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes colorChange {
        0% { color: #2ecc71; }
        25% { color: #f1c40f; }
        50% { color: #e74c3c; }
        75% { color: #3498db; }
        100% { color: #9b59b6; }
    }
    
    .eid-title {
        text-align: center;
        animation: float 3s ease-in-out infinite, colorChange 10s infinite;
        font-size: 3.5em !important;
        margin-bottom: 0.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .greeting-box {
        background: linear-gradient(45deg, #f1c40f, #2ecc71);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    .countdown {
        font-size: 2em;
        color: #e74c3c;
        text-align: center;
        margin: 1rem 0;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .eidi-image {
        border: 5px solid #f1c40f;
        border-radius: 15px;
        animation: float 4s ease-in-out infinite;
        margin: 0 auto;
        display: block;
        transition: transform 0.3s;
    }
    
    .eidi-image:hover {
        transform: scale(1.03);
    }
    
    .share-button {
        background-color: #0077b5 !important;
        color: white !important;
        border-radius: 25px;
        padding: 12px 25px;
        text-decoration: none;
        display: inline-block;
        margin-top: 15px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }
    
    .share-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    .stTextInput input {
        border-radius: 10px !important;
        padding: 12px !important;
    }
    
    .stButton>button {
        border-radius: 10px !important;
        padding: 10px 24px !important;
        background: linear-gradient(45deg, #2ecc71, #3498db) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }
    
    .moon-phases {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .moon-phase {
        font-size: 2rem;
        animation: float 5s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)

set_css()


# Update your autoplay_audio function to this version:
def autoplay_audio(file_path: str, stop_after=10):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio id="eidAudio" autoplay controls style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
                Your browser does not support the audio element.
                </audio>
                <script>
                    // Autoplay with user interaction requirement
                    document.addEventListener('click', function() {{
                        const audio = document.getElementById("eidAudio");
                        if (audio) {{
                            audio.play().catch(e => console.log("Audio play failed:", e));
                            setTimeout(() => {{
                                if (audio) audio.pause();
                            }}, {stop_after * 1000});
                        }}
                    }}, {{once: true}});
                </script>
                """
            st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading audio: {str(e)}")

# Eidi image processing
def create_eidi_image(name, amount, template_path="src/eidi_template.jpg"):
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

def display_moon_phases():
    phases = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
    st.markdown("""
    <div class="moon-phases">
        <div class="moon-phase" style="animation-delay: 0s">🌑</div>
        <div class="moon-phase" style="animation-delay: 0.5s">🌒</div>
        <div class="moon-phase" style="animation-delay: 1s">🌓</div>
        <div class="moon-phase" style="animation-delay: 1.5s">🌔</div>
        <div class="moon-phase" style="animation-delay: 2s">🌕</div>
        <div class="moon-phase" style="animation-delay: 2.5s">🌖</div>
        <div class="moon-phase" style="animation-delay: 3s">🌗</div>
        <div class="moon-phase" style="animation-delay: 3.5s">🌘</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='eid-title'>🌙 Eid Mubarak 2025 🌟</h1>", unsafe_allow_html=True)
    
    # Display moon phases animation
    display_moon_phases()

    
    # Set Eid date (update accordingly)
    eid_date = datetime.datetime(2024, 6, 17, 0, 0)  # Example date
    
    with st.form("user_info"):
        name = st.text_input("Enter Your Name:", placeholder="Your Name")
        linkedin = st.text_input("Enter LinkedIn Profile URL:", placeholder="https://linkedin.com/in/yourprofile")
        submitted = st.form_submit_button("Get Your Eidi!")
        
    if submitted and name and linkedin:
        # Show greeting immediately
        st.balloons()
        autoplay_audio("src/music.mp3", stop_after=10)
    
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
        autoplay_audio("src/mp3.wav", stop_after=10)
        
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
                    use_container_width=True)
        
        # Standard Eidi image
        if os.path.exists("src/eidi-image.PNG"):
            st.image("src/eidi-image.PNG", 
                    caption="Traditional Eidi Gift", 
                    use_container_width=True)
        
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
