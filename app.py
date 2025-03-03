import os
import requests
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
import io 

load_dotenv()

AUDD_API_KEY = os.getenv("AUDD_API_KEY")
AUDD_API_URL = os.getenv("AUDD_API_URL")
CATALOGUE_API_URL = "http://localhost:5001/tracks/audio" 

app = Flask(__name__)
def get_track_audio(title, artist):
    response = requests.post(CATALOGUE_API_URL, json={"title": title, "artist": artist})
    if response.status_code == 200:
        return response.content, response.headers.get('Content-Type') 
    return None, None

@app.route('/recognize', methods=['POST'])
def recognize():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    try:
        response = requests.post(
            AUDD_API_URL,
            data={'api_token': AUDD_API_KEY},
            files={'file': (file.filename, file.stream, file.content_type)}  
           
        )
        result = response.json()
        is_success = result.get('status') == 'success' and result.get('result')

        if is_success:
            track_info = result["result"]
            title, artist = track_info.get("title"), track_info.get("artist")
            

            audio_content, content_type = get_track_audio(title, artist)

            if audio_content:
                return send_file(
                    io.BytesIO(audio_content),
                    mimetype=content_type,
                    as_attachment=True,
                    download_name=f"{title} - {artist}.mp3"
                )

        return jsonify({
            "error": "Track not recognized",
            "api_response": result
        }), 404
    

    except Exception as e:
        return jsonify({"error": "AudD API request failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
