from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from googletrans import Translator
from collections import Counter
from sqlalchemy import func
import re
import os
from flask_cors import CORS
from flask_jwt_extended import unset_jwt_cookies
from collections import defaultdict

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voice_analyzer.db'
app.config['JWT_SECRET_KEY'] = '0eee5890b079bf9522d5b141be5978d44f909baae2f96c89050b7a41aad1bf3b'

if not app.config['JWT_SECRET_KEY']:
    raise RuntimeError("JWT_SECRET_KEY must be set")

print(f"JWT_SECRET_KEY is set to: {app.config['JWT_SECRET_KEY']}")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
translator = Translator()

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    transcriptions = db.relationship('Transcription', backref='user', lazy=True)

class Transcription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=func.now())

# Utility functions
def translate_text(text, target_language='en'):
    translation = translator.translate(text, dest=target_language)
    return translation.text

def get_word_frequency(text):
    words = re.findall(r'\w+', text.lower())
    return Counter(words)

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(f"Received login request: {data}")  # Debugging: Log received data
    username = data.get('username')
    password = data.get('password')
    print(f"Username: {username}, Password: {password}")  # Debugging: Log credentials

    user = User.query.filter_by(username=username).first()
    print(f"User found: {user}")  # Debugging: Log user found

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        print(f"Access token created: {access_token}")  # Debugging: Log access token
        return jsonify(access_token=access_token), 200

    print("Invalid credentials")  # Debugging: Log invalid credentials
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/user', methods=['GET'])
@jwt_required()
def user_info():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "username": user.username,
            "email": user.email
        }), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/transcribe', methods=['POST'])
@jwt_required()
def transcribe():
    user_id = get_jwt_identity()
    data = request.get_json()
    text = data['text']
    language = data.get('language', 'en')

    if language != 'en':
        text = translate_text(text)

    new_transcription = Transcription(user_id=user_id, text=text, language='en')
    db.session.add(new_transcription)
    db.session.commit()

    return jsonify({"message": "Transcription stored successfully", "transcription": text}), 201

@app.route('/history', methods=['GET'])
@jwt_required()
def history():
    user_id = get_jwt_identity()
    transcriptions = Transcription.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": t.id, "text": t.text, "language": t.language, "timestamp": t.timestamp} for t in transcriptions]), 200

@app.route('/word_frequency', methods=['GET'])
@jwt_required()
def word_frequency():
    user_id = get_jwt_identity()

    # Fetch user-specific transcriptions
    user_transcriptions = Transcription.query.filter_by(user_id=user_id).all()
    user_text = ' '.join([t.text for t in user_transcriptions])
    user_word_freq = get_word_frequency(user_text)

    # Calculate global frequencies relative to user frequencies
    all_transcriptions = Transcription.query.all()
    global_text = ' '.join([t.text for t in all_transcriptions])
    global_word_freq = get_word_frequency(global_text)

    # Get top 3 words for user and global frequencies
    top_user_words = dict(user_word_freq.most_common(3))
    top_global_words = dict(global_word_freq.most_common(3))

    return jsonify({
        "user_frequency": top_user_words,
        "global_frequency": top_global_words
    }), 200

def get_unique_phrases(text):
    words = re.findall(r'\w+', text.lower())
    phrases = [words[i:i+3] for i in range(len(words) - 2)]
    phrase_freq = Counter(map(tuple, phrases))
    unique_phrases = [phrase for phrase, freq in phrase_freq.items() if freq == 1]
    return unique_phrases[:3]

# Routes
@app.route('/unique_phrases', methods=['GET'])
@jwt_required()
def unique_phrases():
    user_id = get_jwt_identity()
    transcriptions = Transcription.query.filter_by(user_id=user_id).all()
    all_text = ' '.join([t.text for t in transcriptions])
    unique_phrases = get_unique_phrases(all_text)

    return jsonify({"unique_phrases": unique_phrases}), 200

@app.route('/similar_users', methods=['GET'])
@jwt_required()
def similar_users():
    user_id = get_jwt_identity()

    # Function to calculate Jaccard similarity
    def jaccard_similarity(set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    # Get all transcriptions for the current user
    user_transcriptions = Transcription.query.filter_by(user_id=user_id).all()
    user_words = set()

    for transcription in user_transcriptions:
        words = set(transcription.text.lower().split())  # Assuming text is cleaned and split by spaces
        user_words.update(words)

    # Find similar users based on Jaccard similarity
    users = User.query.filter(User.id != user_id).all()
    similarity_scores = []

    for user in users:
        user_transcriptions = Transcription.query.filter_by(user_id=user.id).all()
        other_words = set()

        for transcription in user_transcriptions:
            words = set(transcription.text.lower().split())  # Assuming text is cleaned and split by spaces
            other_words.update(words)

        similarity_score = jaccard_similarity(user_words, other_words)
        similarity_scores.append((user.id, similarity_score))

    # Sort users by similarity score (higher first) and get top similar users
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    most_similar_users = [user_id for user_id, score in similarity_scores[:3]]

    # Retrieve usernames based on user ids
    similar_usernames = [User.query.get(user_id).username for user_id in most_similar_users]

    return jsonify({"most_similar_users": similar_usernames}), 200

# Protected route to demonstrate JWT usage
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Logout route to invalidate JWT token
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Optionally perform additional cleanup or logging out logic here
    return jsonify({'message': 'Successfully logged out'}), 200


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
