from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai
import os
from openpyxl import Workbook
import tempfile
import uuid


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

    🎯 Strategy Guidelines:
    - Every post should address specific audience pain points.
    - Follow the latest social media engagement trends.
    - Mix short-form and long-form content.
    - Include **video content** suggestions in each plan.
    - Optimize for engagement (best times, emotional hooks, hashtags).
    
    📦 If the subscription is "Premium", include exactly:
    - 📌 Monday: AI-Generated Customer Testimonial Video
    - 📌 Wednesday: Live Q&A Session (AI Recommends Topics)
    - 📌 Friday: AI-Optimized Paid Ad Campaign (Social & Google)
    - 📌 Sunday: Personal Branding Blog Post (SEO-Optimized)
    
    🗓 Format your output like this:
    Day of Week: [Post Type] - [Short Description]
    Example:
    📌 Monday: Story-based video post – Highlight a transformation journey of a client.
    
    Generate the calendar now:
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )

        calendar_text = response.choices[0].message.content.strip()

        wb = Workbook()
        ws = wb.active
        ws.title = "Content Calendar"
        ws.append([f"Content Calendar for {business_name}"])
        ws.append(["Day", "Post Type", "Description"])

        for line in calendar_text.split("\n"):
            if ":" in line:
                try:
                    day_part, desc = line.split(":", 1)
                    if "–" in desc:
                        post_type, description = desc.split("–", 1)
                    elif "-" in desc:
                        post_type, description = desc.split("-", 1)
                    else:
                        post_type, description = "", desc
                    ws.append([day_part.strip(), post_type.strip(), description.strip()])
                except ValueError:
                    ws.append([line])  # se falhar, coloca linha inteira

        # Gera nome único
        unique_id = str(uuid.uuid4())
        filename = f"calendar_{unique_id}.xlsx"
        path = os.path.join("static", filename)

        # Salva na pasta pública
        os.makedirs("static", exist_ok=True)
        wb.save(path)

        # Retorna a URL pública
        base_url = request.host_url.rstrip("/")
        file_url = f"{base_url}/static/{filename}"

        return jsonify({"url": file_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
