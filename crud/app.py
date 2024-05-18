from flask import Flask
from config import Config
from book_app.models import db
from book_app.routes import api

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
with app.app_context():
    db.create_all()

# Register routing blueprint
app.register_blueprint(api, url_prefix="/api")

# Index routing
@app.route("/")
def home():
    return "Welcome to Book Store"


if __name__ == "__main__":
    app.run(debug=True)


    