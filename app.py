import streamlit as st
import os
from dotenv import load_dotenv
from utils.gemini_service import generate_content, GeminiServiceError
from utils.helpers import load_prompt

# Load environment variables
load_dotenv()

def init_session_state():
    if 'article_text' not in st.session_state:
        st.session_state.article_text = ""
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = None
    if 'selected_platform' not in st.session_state:
        st.session_state.selected_platform = "LinkedIn"
    if 'selected_tone' not in st.session_state:
        st.session_state.selected_tone = "Professional"
    if 'selected_length' not in st.session_state:
        st.session_state.selected_length = "Medium"
    if 'error_msg' not in st.session_state:
        st.session_state.error_msg = None
    
    # Metadata for currently generated content
    if 'meta_platform' not in st.session_state:
        st.session_state.meta_platform = None
    if 'meta_tone' not in st.session_state:
        st.session_state.meta_tone = None
    if 'meta_length' not in st.session_state:
        st.session_state.meta_length = None

def clear_data():
    st.session_state.article_text = ""
    st.session_state.generated_content = None
    st.session_state.error_msg = None
    st.session_state.selected_platform = "LinkedIn"
    st.session_state.selected_tone = "Professional"
    st.session_state.selected_length = "Medium"
    st.session_state.meta_platform = None
    st.session_state.meta_tone = None
    st.session_state.meta_length = None

def perform_generation(article_text, platform, tone, length):
    st.session_state.error_msg = None
    
    word_count = len(article_text.split()) if article_text else 0
    if not article_text.strip():
        st.session_state.error_msg = "Please enter a source article before rewriting."
        return
    if word_count < 10:
        st.session_state.error_msg = "The article is too short. Please provide at least 10 words of context."
        return

    with st.spinner(f"Optimizing content for {platform} in a {tone.lower()} tone..."):
        try:
            platform_map = {
                "Twitter / X": "twitter",
                "LinkedIn": "linkedin",
                "Newsletter": "newsletter"
            }
            prompt_name = platform_map[platform]
            prompt_template = load_prompt(prompt_name)
            
            # Format the prompt dynamically
            final_prompt = prompt_template.format(article=article_text, tone=tone, length=length)
            
            # Call Gemini
            result = generate_content(final_prompt)
            
            st.session_state.generated_content = result
            st.session_state.meta_platform = platform
            st.session_state.meta_tone = tone
            st.session_state.meta_length = length
            
        except FileNotFoundError as e:
            st.session_state.error_msg = f"Configuration Error: {str(e)}"
        except GeminiServiceError as e:
            st.session_state.error_msg = f"AI Service Error: {str(e)}"
        except Exception as e:
            st.session_state.error_msg = f"An unexpected error occurred: {str(e)}"

def main():
    st.set_page_config(page_title="AI Social Media Content Rewriter", page_icon="✨", layout="centered")
    init_session_state()
    
    # 1. Branding
    st.title("AI Social Media Content Rewriter")
    st.markdown("Transform your articles and blog posts into platform-optimized social media content.")
    st.markdown("---")
    
    # 2. Layout & Article Input
    st.subheader("Source Article")
    
    article_text = st.text_area(
        label="Paste your full article below:",
        value=st.session_state.article_text,
        height=250,
        placeholder="e.g., Artificial intelligence is changing how we write code...",
        key="article_input_widget"
    )
    
    word_count = len(article_text.split()) if article_text else 0
    st.caption(f"Word count: {word_count}")

    # 3. Controls (Advanced Settings)
    st.subheader("Settings")
    col1, col2, col3 = st.columns(3)
    
    available_platforms = ["Twitter / X", "LinkedIn", "Newsletter"]
    platform_idx = available_platforms.index(st.session_state.selected_platform) if st.session_state.selected_platform in available_platforms else 1
    
    available_tones = ["Professional", "Friendly", "Persuasive", "Educational", "Casual"]
    tone_idx = available_tones.index(st.session_state.selected_tone) if st.session_state.selected_tone in available_tones else 0
    
    available_lengths = ["Short", "Medium", "Long"]
    length_idx = available_lengths.index(st.session_state.selected_length) if st.session_state.selected_length in available_lengths else 1

    with col1:
        platform = st.selectbox("Select Platform", available_platforms, index=platform_idx)
    with col2:
        tone = st.selectbox("Select Tone", available_tones, index=tone_idx)
    with col3:
        length = st.selectbox("Content Length", available_lengths, index=length_idx)
        
    # Buttons
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        generate_clicked = st.button("Rewrite Content", type="primary", use_container_width=True)
    with col_btn2:
        reset_clicked = st.button("Clear / Reset", use_container_width=True)
        
    if reset_clicked:
        clear_data()
        st.rerun()

    if generate_clicked:
        # Save selections to state
        st.session_state.article_text = article_text
        st.session_state.selected_platform = platform
        st.session_state.selected_tone = tone
        st.session_state.selected_length = length
        
        perform_generation(article_text, platform, tone, length)
    
    # Display Errors
    if st.session_state.error_msg:
        st.error(st.session_state.error_msg)
        
    # Display Generated Content
    if st.session_state.generated_content and not st.session_state.error_msg:
        st.success("Content generated successfully!")
        
        st.markdown("### Generated Result")
        
        # Display Metadata cleanly
        st.info(f"**Platform:** {st.session_state.meta_platform} | **Tone:** {st.session_state.meta_tone} | **Length:** {st.session_state.meta_length}")
        
        st.markdown("---")
        st.write(st.session_state.generated_content)
        st.markdown("---")
            
        st.caption("*Tip: Highlight the text above to copy it to your clipboard.*")
        
        # Regeneration Button near the generated result
        if st.button("Regenerate", use_container_width=False):
            st.session_state.article_text = article_text
            st.session_state.selected_platform = platform
            st.session_state.selected_tone = tone
            st.session_state.selected_length = length
            
            perform_generation(article_text, platform, tone, length)
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray; font-size: 0.8em;'>"
        "AI Social Media Content Rewriter • Developed By Anees Ur Rehman"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
