import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiServiceError(Exception):
    """Custom exception for Gemini API errors to allow clean handling by app.py."""
    pass

def generate_content(prompt: str) -> str:
    """
    Sends a prompt string to the Gemini API and returns the generated text.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    if not api_key or api_key == "your_gemini_api_key_here":
        raise GeminiServiceError("GEMINI_API_KEY is missing or invalid in the environment.")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        
        # Generate content (plain text for now)
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text
        else:
            raise GeminiServiceError("Received an empty response from Gemini.")
    except Exception as e:
        # Wrap the underlying exception
        raise GeminiServiceError(f"Gemini API request failed: {str(e)}")

if __name__ == "__main__":
    # Basic test mechanism to run directly via python
    print("Testing Gemini connection...")
    try:
        result = generate_content("Reply with exactly: GEMINI CONNECTION SUCCESS")
        print(f"Result: {result}")
    except GeminiServiceError as e:
        print(f"Test failed cleanly with application error: {e}")
    except Exception as e:
        print(f"Test failed with unexpected error: {e}")
