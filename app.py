from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os
import traceback

load_dotenv()

print("API KEY LOADED:", bool(os.getenv("GEMINI_API_KEY")))

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_content():

    try:
        data = request.get_json()
        course_title = data.get("course_title", "").strip()

        if not course_title:
            return jsonify({
                "error": "Please enter a course title."
            }), 400

        prompt = f"""
You are an expert educational content designer.

Create educational content for the course:
"{course_title}"

Return the answer in the following structure:

1. Course Objective
Write one clear course objective.

2. Sample Syllabus
Provide 5 to 6 modules with suitable topics.

3. Learning Outcomes
Provide exactly 3 measurable learning outcomes.
Start each outcome with an appropriate action verb.

4. Assessment Methods
Provide suitable assessment methods.

5. Recommended Readings
Provide useful books, documentation, or learning resources.

6. Bloom's Taxonomy Alignment
For each learning outcome, mention the Bloom's Taxonomy level:
Remember, Understand, Apply, Analyze, Evaluate, or Create.

Keep the content clear, practical, measurable, and suitable for students.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        generated_content = response.text

        return jsonify({
            "content": generated_content
        })

    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
