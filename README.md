# AI Social Media Content Rewriter

**Client:** BuzzReach  
**Industry:** Social Media and Digital Marketing  

## About the Project
The AI Social Media Content Rewriter is a professional, portfolio-ready application designed to take an article or blog post and automatically generate tailored content. It uses the Gemini API to understand the core message of the original text and rewrite it appropriately, maintaining consistent meaning across all platforms while allowing for tone and length customization.

## Main Features
- **Supported Platforms:** 
  - Twitter / X (Generates concise threads)
  - LinkedIn (Generates professional, structured posts)
  - Newsletter (Generates friendly email formats)
- **Supported Tones:** Professional, Friendly, Persuasive, Educational, Casual.
- **Content Length Options:** Short, Medium, Long.
- **Error Handling:** Robust, user-friendly UI error messages for missing API keys, empty/short inputs (<10 words), and Gemini API failures (no Python tracebacks exposed).
- **Security:** The Gemini API key is securely loaded from a `.env` file and is never exposed in the UI or codebase.
- **Session State Persistence:** Selections and generated output remain visible even if you change dropdowns mid-session.
- **Regenerate / Reset:** Native buttons to easily clear data or regenerate content using updated settings.

## Tech Stack
- **Python**: Core programming language
- **Streamlit**: Web application framework for the UI
- **Gemini API**: Generative AI model for content rewriting
- **python-dotenv**: Environment variable management

## Folder Structure
- `app.py`: Main Streamlit application and UI flow.
- `prompts/`: Contains prompt templates for different platforms.
- `utils/`: Contains the Gemini API service and helper functions.
- `examples/`: Sample input files.

## Setup Instructions

### 1. Clone the repository
Ensure you are in the project folder.

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment
- **Windows:** `venv\Scripts\activate`
- **macOS/Linux:** `source venv/bin/activate`

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup Environment Variables
1. Copy `.env.example` to a new file named `.env`.
2. Open `.env` and add your Gemini API key exactly as follows:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-3.6-flash
   ```
*Security Note: Never commit your `.env` file to version control. The `.gitignore` is pre-configured to ignore it.*

### 6. Run the Application
```bash
streamlit run app.py
```

## Example Usage
1. Run the Streamlit app.
2. Paste the contents of `examples/sample_article.txt` into the "Source Article" text area.
3. Select "LinkedIn", "Professional" tone, and "Medium" length.
4. Click "Rewrite Content".
5. Copy the cleanly formatted output natively!

## Future Improvements
- Add support for direct integration with social media APIs for auto-posting.
- Implement caching to prevent duplicate API calls for identical requests.
- Add structured output (JSON mode) for more complex workflows.
