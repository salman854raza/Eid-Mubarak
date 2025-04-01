import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import datetime
import time
import base64
import os
import urllib.parse

# Set page config
st.set_page_config(
    page_title="Eid Mubarak 2025",
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

# Audio function with improved error handling
def autoplay_audio(file_path: str, stop_after=10):
    try:
        if not os.path.exists(file_path):
            st.error(f"Audio file not found at: {file_path}")
            return
            
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio id="eidAudio" controls style="display:none;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mpeg">
                Your browser does not support the audio element.
                </audio>
                <script>
                    // Play audio after user interaction
                    function playAudio() {{
                        const audio = document.getElementById("eidAudio");
                        if (audio) {{
                            audio.play().catch(e => console.log("Audio play failed:", e));
                            setTimeout(() => {{
                                if (audio) audio.pause();
                            }}, {stop_after * 1000});
                        }}
                    }}
                    // Play when button is clicked
                    document.addEventListener('click', playAudio, {{once: true}});
                </script>
                """
            st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading audio: {str(e)}")

# Eidi image processing with improved font handling
def create_eidi_image(name, amount, template_path="eidi_template.jpg"):
    try:
        img = Image.open(template_path)
        draw = ImageDraw.Draw(img)
        
        # Font handling with fallbacks
        try:
            font_large = ImageFont.truetype("arial.ttf", 60) or ImageFont.load_default()
            font_small = ImageFont.truetype("arial.ttf", 40) or ImageFont.load_default()
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Draw amount text
        amount_text = f"Rs {amount}"
        amount_width = draw.textlength(amount_text, font=font_large)
        draw.text(
            (img.width//2 - amount_width//2, img.height//2 + 80), 
            amount_text, 
            fill=(255, 215, 0),  # Gold color
            font=font_large
        )
        
        # Draw name text
        name_text = f"For {name}"
        name_width = draw.textlength(name_text, font=font_small)
        draw.text(
            (img.width//2 - name_width//2, img.height//2 + 150), 
            name_text, 
            fill=(255, 255, 255),  # White color
            font=font_small
        )
        
        return img
    except Exception as e:
        st.error(f"Error creating Eidi image: {str(e)}")
        return None

# Main app function
def main():
    st.markdown("<h1 class='eid-title'>🌙 Eid Mubarak 2025 🌟</h1>", unsafe_allow_html=True)
    
    with st.form("user_info"):
        name = st.text_input("Enter Your Name:", placeholder="Your Name")
        linkedin = st.text_input("Enter LinkedIn Profile URL:", placeholder="https://linkedin.com/in/yourprofile")
        submitted = st.form_submit_button("Get Your Eidi!")
    
    if submitted:
        if not name.strip():
            st.warning("Please enter your name!")
            return
        
        # Show greeting immediately
        st.balloons()
        autoplay_audio("mp3.wav", stop_after=10)
        
        # Greeting box with LinkedIn share button
        share_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(linkedin)}"
        st.markdown(f"""
        <div class="greeting-box">
            <h2>Eid Mubarak, {name}! 🎉</h2>
            <p>May Allah bless you with happiness, peace, and prosperity!</p>
            <a href="{share_url}" target="_blank" class="share-button">
               Share on LinkedIn
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Display Eidi image with personalized message
        st.markdown("<h3 style='text-align: center;'>Your Eidi Gift</h3>", unsafe_allow_html=True)
        
        # Personalized Eidi image (updated to use_container_width)
        eidi_img = create_eidi_image(name, 5000)
        if eidi_img:
            st.image(eidi_img, 
                    caption=f"Rs 5000 is for you, {name}!",
                    use_container_width=True)  # Updated parameter
        
        # Standard Eidi image (updated to use_container_width)
        if os.path.exists("eidi-image.png"):
            st.image("eidi-image.png", 
                    caption="Traditional Eidi Gift",
                    use_container_width=True)  # Updated parameter
        
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
        setTimeout(fireConfetti, 500);
        
        // Continue every 3 seconds
        setInterval(fireConfetti, 3000);
        </script>
        """, height=0)

if __name__ == "__main__":
    main()
