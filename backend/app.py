from flask import Flask
from api.predict import app as predict_app
import os

app = Flask(__name__)

app.register_blueprint(predict_app, url_prefix='/api')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
