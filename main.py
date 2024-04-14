from flask import Flask, request
import base64
import google.generativeai as genai
import os
import PIL.Image
import json

api_key = os.environ["API_KEY"]
port = os.environ.get("PORT", 443)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro-vision")


@app.post("/")
def index():
    print(request.get_data())
    data = request.get_data()
    print(data)
    data = json.loads(data)
    image = data["image"]
    del data["image"]
    decoded_image = base64.b64decode(image)
    with open("image.jpg", "wb") as f:
        f.write(decoded_image)
    img = PIL.Image.open("image.jpg")
    response = model.generate_content(
        [
            f"This is a food product. Give me the health rating for this between 1 and 10, where 1 is the worst and 10 is the healthiest. Also include some tips on how I can cook with that food product. When you give a rating, mention the characters '/10'. Also mention the name of the food product. Let me know if this is not suitable for people with any allergies. Give the health rating at the start of your response. These are my parameters of importance: {str(data)}",
            img,
        ]
    )
    print(response.text)
    return response.text


@app.get("/test")
def test():
    return "Test route"


app.run(debug=True, host="0.0.0.0", port=port)
