import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

AUDD_API_KEY = os.getenv("AUDD_KEY")

@app.route('/recognize', methods=['POST'])
def recognize():
    return {"message": "Recognize route is working!", "API_KEY": AUDD_API_KEY}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)
