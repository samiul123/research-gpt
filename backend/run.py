from app import create_app, db
from flask_cors import CORS

app = create_app()
CORS(app, resources={r"/api/*": {"origins": "*"}})

with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run(port=5001, debug=True)