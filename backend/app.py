from flask import Flask
from flask_cors import CORS
from api.predict import predict_app  # Import the blueprint
from flask import jsonify
import os

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

app.register_blueprint(predict_app, url_prefix='/api')  # Register the blueprint

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the ShotCaller API. Use /api/predict for predictions."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
