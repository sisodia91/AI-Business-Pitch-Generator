import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request

# --- Basic Setup ---
# Initialize the Flask app
app = Flask(__name__)

# Load environment variables and configure the Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Your Core AI Function ---
# (This is the same function you already wrote)
def generate_pitch(startup_idea):
    """Generates a business pitch using the Gemini API."""
    prompt = f"""
    You are an AI startup consultant. Generate a structured and compelling business pitch for the startup idea: "{startup_idea}".
    
    The pitch should be well-formatted and include these clear sections:
    1.  **Problem:** What is the core problem you are solving?
    2.  **Solution:** How does your product/service solve this problem?
    3.  **Target Market:** Who are your ideal customers?
    4.  **Revenue Model:** How will you make money?
    5.  **Competitive Advantage:** What makes you unique and better than others?
    6.  **Closing Statement:** A powerful final sentence to leave a lasting impression.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        # Use Markdown for better formatting on the webpage
        return response.text.replace('\n', '<br>') 
    except Exception as e:
        return f"An error occurred: {e}"

# --- Web Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles both displaying the page and processing the form."""
    pitch_result = ""
    if request.method == 'POST':
        # Get the startup idea from the form on the webpage
        startup_idea = request.form['startup_idea']
        if startup_idea:
            # Generate the pitch if an idea was submitted
            pitch_result = generate_pitch(startup_idea)
            
    # Render the HTML page and pass the pitch result to it
    return render_template('index.html', pitch=pitch_result)

# --- Run the App ---
if __name__ == '__main__':
    # Runs the web server
    app.run(debug=True) 