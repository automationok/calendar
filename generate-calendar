from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate-calendar', methods=['POST'])
def generate_calendar():
    data = request.json
    business_name = data.get("business_name", "Your Business")
    industry = data.get("industry", "general")
    subscription = data.get("subscription", "Free")

    prompt = f"""
    You are an expert social media strategist.

    Generate a 1-week AI-powered content calendar for the business below:
    - Business Name: {business_name}
    - Industry: {industry}
    - Subscription Plan: {subscription}

    🔥 Requirements:
    - Create posts that solve audience pain points.
    - Use current engagement trends.
    - Include both short-form and long-form content.
    - Incorporate video ideas.
    - Optimize for engagement (timing, hashtags, tone).

    🗓 Format:
    - Day of Week: [Post Type] - [1-sentence description]
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )

        ai_content = response.choices[0].message.content.strip()
        return jsonify({"calendar": ai_content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
