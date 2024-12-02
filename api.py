from flask import Flask, request, jsonify
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Streamlit app ka URL yeh hai (aap apna update karein)
STREAMLIT_APP_URL = "https://share.streamlit.io/your-username/your-repo/main"  # Apna URL yahan dalein

@app.route('/api/sketch', methods=['POST'])
def sketch():
    # Check if the image file is provided
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Image ko open karein aur byte array mein convert karein
        img = Image.open(file)
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Streamlit app ko image bhejein
        response = requests.post(STREAMLIT_APP_URL, files={'image': img_byte_arr})

        # Agar response theek hai toh image ko return karein
        if response.status_code == 200:
            return response.content, 200, {'Content-Type': 'image/png'}
        else:
            return jsonify({"error": "Error processing image"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
  
