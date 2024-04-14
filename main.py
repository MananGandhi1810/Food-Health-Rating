from flask import Flask, request
import base64
import google.generativeai as genai
import os
import PIL.Image

api_key = os.environ["API_KEY"]

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro-vision")


@app.post("/")
def index():
    print(request.get_data())
    image = request.get_data()
    decoded_image = base64.b64decode(image)
    with open("image.jpg", "wb") as f:
        f.write(decoded_image)
    img = PIL.Image.open("image.jpg")
    response = model.generate_content(
        [
            "This is a food product. Give me the health rating for this between 1 and 10, where 1 is the worst and 10 is the healthiest. Also include some tips on how I can cook with that food product.",
            img,
        ]
    )
    print(response.text)
    return response.text


@app.get("/test")
def test():
    return "Test route"


app.run(debug=True, host="0.0.0.0", port=3000)
