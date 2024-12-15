from flask import Flask, request, jsonify, send_file, render_template
import os
from io import BytesIO
import base64
import logging
from PIL import Image
from gtts import gTTS

# Initialize Flask app
app = Flask(__name__)

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Ensure the static folder exists
if not os.path.exists('static'):
    os.makedirs('static')

# Placeholder image generation function
def generate_image(prompt):
    # For demonstration, create a simple placeholder image (e.g., a red image)
    image = Image.new('RGB', (256, 256), color='violet')
    return image

# Placeholder audio generation function using gTTS (Google Text-to-Speech)
def generate_audio(text, audio_path):
    tts = gTTS(text)
    tts.save(audio_path)

# Serve the HTML file for the frontend
@app.route('/')
def home():
    return render_template('index.html')  # Ensure `index.html` is in the `templates` folder

# Endpoint to generate image and audio based on prompt and text
@app.route('/generate-media', methods=['POST'])
def generate_media():
    logging.debug("Received request to generate media")
    data = request.json
    prompt = data.get('prompt', '')
    text = data.get('text', '')

    # Ensure both prompt and text are provided
    if not prompt or not text:
        logging.error("Prompt or text is missing.")
        return jsonify({"error": "Prompt and text are required"}), 400

    try:
        logging.debug(f"Generating image for prompt: {prompt}")
        image = generate_image(prompt)  # Generate image

        # Convert image to base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        image_data = base64.b64encode(buffered.getvalue()).decode()

        logging.debug("Generating audio from text.")
        audio_path = os.path.join('static', "output.wav")  # Save audio in the static folder
        generate_audio(text, audio_path)  # Generate audio

        # Return JSON response with image data and audio download link
        return jsonify({
            "image_data": image_data,
            "audio_path": f"/static/output.wav"
        })
    except Exception as e:
        logging.error(f"Error generating media: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

# Endpoint to download the generated audio file
@app.route('/download-audio', methods=['GET'])
def download_audio():
    path = request.args.get('path', '')
    logging.debug(f"Request to download audio from path: {path}")

    # Check if the audio file exists
    if not os.path.exists(path):
        logging.error(f"Audio file not found at path: {path}")
        return jsonify({"error": "Audio file not found"}), 404

    # Return the audio file for download
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    logging.debug("Starting Flask app on port 5000")
    app.run(debug=True, port=5000)

