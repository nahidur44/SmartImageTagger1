from flask import Flask, render_template, request
import os
import requests

app = Flask(__name__)

# Replace these with YOUR Azure keys!
API_KEY = "Fqzie1fCdkiI2vWucXKLez5QhHyNLF2bqAaq5yWcthvl3pIkmQnbJQQJ99BCACYeBjFXJ3w3AAAFACOGQn0K"
ENDPOINT = "https://imagetaggerbynahid.cognitiveservices.azure.com/"

@app.route("/", methods=["GET", "POST"])
def home():
    tags = []
    image_url = None
    
    if request.method == "POST":
        if "image" in request.files:
            file = request.files["image"]
            if file.filename != "":
                # Save the uploaded image temporarily
                image_path = "static/uploaded_image.jpg"
                file.save(image_path)
                image_url = image_path
                
                # Call Azure AI to analyze the image
                headers = {
                    "Ocp-Apim-Subscription-Key": API_KEY,
                    "Content-Type": "application/octet-stream"
                }
                
                with open(image_path, "rb") as img:
                    response = requests.post(
                        f"{ENDPOINT}/vision/v3.2/analyze?visualFeatures=Tags",
                        headers=headers,
                        data=img
                    )
                
                if response.status_code == 200:
                    tags = [tag["name"] for tag in response.json().get("tags", [])]
    
    return render_template("index.html", tags=tags, image_url=image_url)

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)