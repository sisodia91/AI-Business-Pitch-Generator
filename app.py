import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request


app = Flask(__name__)


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


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
       
        return response.text.replace('\n', '<br>') 
    except Exception as e:
        return f"An error occurred: {e}"


@app.route('/', methods=['GET', 'POST'])
def index():
    """Handles both displaying the page and processing the form."""
    pitch_result = ""
    if request.method == 'POST':
        
        startup_idea = request.form['startup_idea']
        if startup_idea:
            
            pitch_result = generate_pitch(startup_idea)
            
   
    return render_template('index.html', pitch=pitch_result)


if __name__ == '__main__':
   
    app.run(debug=True) 
