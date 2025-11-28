import utils.clients
import utils.http_session
import utils.transport
import utils.session
from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
	# Check if the file has a valid extension
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Placeholder: connect to DB (MongoDB/Firebase). Replace with real client.
# e.g. from pymongo import MongoClient
# db_client = MongoClient(os.environ.get("MONGO_URI"))
# db = db_client.get_database("virasky")

# Placeholder AI call helpers. Replace comments with real API calls:
def call_ai_chat(user_id, message, preferences):
	# Connect to GPT-4.1 / GPT-5 API for relationship & life advice.
	# Example: send system prompt with Vira Sky personality, user prefs, and message.
	# return ai_response_text
	return f"[AI placeholder reply to '{message}']"

def analyze_mood(text):
	# Use local sentiment model or GPT-4o-mini to detect mood and return tags/scores.
	# return {'mood': 'calm', 'score': 0.87}
	return {'mood': 'neutral', 'score': 0.5}

def summarize_journal(text):
	# Use GPT-4.1 / GPT-4o-mini for summarization and insights.
	# return {'summary': '...', 'insights': [...]}
	return {'summary': text[:200], 'insights': []}

def generate_affirmation(mood, user_profile):
	# Use GPT-4o-mini or Llama3-8B local to generate short affirmations.
	return f"Affirmation based on mood: {mood}"

# PAGE ROUTES
@app.route("/")
def home():
	theme = request.cookies.get('theme', 'light')
	return render_template("home.html", theme=theme)

@app.route("/chat")
def chat():
	theme = request.cookies.get('theme', 'light')
	return render_template("chat.html", theme=theme)

@app.route("/explore")
def explore():
	theme = request.cookies.get('theme', 'light')
	return render_template("explore.html", theme=theme)

@app.route("/explore/advice")
def explore_advice():
	theme = request.cookies.get('theme', 'light')
	categories = [
		{"id": "communication", "title": "Communication", "desc": "Improve clarity & active listening."},
		{"id": "trust", "title": "Trust", "desc": "Build reliability, repair breaches."},
		{"id": "breakup_healing", "title": "Breakup Healing", "desc": "Healing steps & self-care."},
		{"id": "overthinking", "title": "Overthinking", "desc": "Tools to quiet the mind."},
		{"id": "jealousy", "title": "Jealousy", "desc": "Manage feelings and boundaries."},
		{"id": "long_distance", "title": "Long-Distance", "desc": "Staying close across distance."},
		{"id": "self_love", "title": "Self-Love", "desc": "Cultivate inner compassion."},
		{"id": "confidence", "title": "Confidence", "desc": "Build presence & assertiveness."},
		{"id": "life_clarity", "title": "Life Clarity", "desc": "Find direction & priorities."}
	]
	return render_template("advice_categories.html", theme=theme, categories=categories)

@app.route("/explore/advice/<category_id>")
def explore_advice_detail(category_id):
	theme = request.cookies.get('theme', 'light')
	category_map = {
		"communication": {"title":"Communication","tagline":"Improve clarity & active listening."},
		"trust": {"title":"Trust","tagline":"Build reliability, repair breaches."},
		"breakup_healing": {"title":"Breakup Healing","tagline":"Healing steps & self-care."},
		"overthinking": {"title":"Overthinking","tagline":"Tools to quiet the mind."},
		"jealousy": {"title":"Jealousy","tagline":"Manage feelings and boundaries."},
		"long_distance": {"title":"Long-Distance","tagline":"Staying close across distance."},
		"self_love": {"title":"Self-Love","tagline":"Cultivate inner compassion."},
		"confidence": {"title":"Confidence","tagline":"Build presence & assertiveness."},
		"life_clarity": {"title":"Life Clarity","tagline":"Find direction & priorities."}
	}
	cat = category_map.get(category_id, {"title": category_id, "tagline": ""})
	preferences = {"tone":"soft","depth":"medium"}
	return render_template("advice_detail.html", theme=theme, category_id=category_id, category=cat, prefs=preferences)

@app.route("/explore/journals")
def explore_journals():
	theme = request.cookies.get('theme', 'light')
	return render_template("journals.html", theme=theme)

@app.route("/explore/affirmations")
def explore_affirmations():
	theme = request.cookies.get('theme', 'light')
	return render_template("affirmations.html", theme=theme)

@app.route("/explore/exercises")
def explore_exercises():
	theme = request.cookies.get('theme', 'light')
	return render_template("exercises.html", theme=theme)

@app.route("/explore/avatar")
def explore_avatar():
	theme = request.cookies.get('theme', 'light')
	styles = ["dreamy", "neon", "anime", "cyber-glow"]
	return render_template("avatar.html", theme=theme, styles=styles)

@app.route("/profile")
def profile():
	theme = request.cookies.get('theme', 'light')
	user_profile = {"name": "Guest", "preferences": {}}
	return render_template("profile.html", theme=theme, profile=user_profile)

@app.route("/profile/user-data")
def profile_user_data():
	theme = request.cookies.get('theme', 'light')
	user_data = {"name": "Guest User", "age": None, "relationship_status": "Single", "avatar_url": None}
	return render_template("profile_user_data.html", theme=theme, user_data=user_data)

@app.route("/profile/preferences")
def profile_preferences():
	theme = request.cookies.get('theme', 'light')
	preferences = {"tone": "soft", "chat_depth": "medium", "emotional_sensitivity": "high", "romantic_mode": False}
	return render_template("profile_preferences.html", theme=theme, preferences=preferences)

@app.route("/profile/personal-settings")
def profile_personal_settings():
	theme = request.cookies.get('theme', 'light')
	settings = {"notifications_enabled": True, "daily_affirmation": True, "mood_tracking": True, "avatar_in_chat": False, "theme": theme}
	return render_template("profile_personal_settings.html", theme=theme, settings=settings)

@app.route("/settings")
def settings():
	theme = request.cookies.get('theme', 'light')
	settings_data = {"safety_18plus": False}
	return render_template("settings.html", theme=theme, settings=settings_data)

@app.route("/settings/privacy")
def settings_privacy():
	theme = request.cookies.get('theme', 'light')
	privacy = {"store_chats": True, "export_allowed": False, "app_lock": False}
	return render_template("settings_privacy.html", theme=theme, privacy=privacy)

@app.route("/settings/safety")
def settings_safety():
	theme = request.cookies.get('theme', 'light')
	safety = {"filters_enabled": True, "sensitive_topics_restricted": True}
	return render_template("settings_safety.html", theme=theme, safety=safety)

@app.route("/settings/18plus")
def settings_18plus():
	theme = request.cookies.get('theme', 'light')
	controls = {"enabled": False, "age_verified": False}
	return render_template("settings_18plus.html", theme=theme, controls=controls)

@app.route("/settings/behavior")
def settings_behavior():
	theme = request.cookies.get('theme', 'light')
	behavior = {"tone": "soft", "depth": "medium", "notifications": {"daily": True}}
	return render_template("settings_behavior.html", theme=theme, behavior=behavior)

@app.route("/toggle-theme")
def toggle_theme():
	current = request.cookies.get('theme', 'light')
	new = 'dark' if current == 'light' else 'light'
	resp = make_response(redirect(request.referrer or url_for('home')))
	resp.set_cookie('theme', new, max_age=30*24*3600)  # 30 days
	return resp

# API ENDPOINTS
@app.route("/api/chat", methods=["POST"])
def api_chat():
	data = request.get_json() or {}
	user_id = data.get('user_id', 'anon')
	message = data.get('message', '')
	# Load user preferences from DB (placeholder)
	preferences = data.get('preferences', {})
	# Safety: apply 18+ control / safety filters before calling AI
	# Call AI chat engine (recommendation: GPT-4.1 / GPT-5)
	reply = call_ai_chat(user_id, message, preferences)
	return jsonify({"reply": reply, "timestamp": datetime.utcnow().isoformat() + "Z"})

@app.route("/api/mood", methods=["POST"])
def api_mood():
	data = request.get_json() or {}
	user_id = data.get('user_id', 'anon')
	text = data.get('text', '')
	# Analyze mood (recommendation: local sentiment model or GPT-4o-mini)
	mood_result = analyze_mood(text)
	# Persist mood to DB (placeholder)
	# db.moods.insert_one({...})
	return jsonify({"mood": mood_result})

@app.route("/api/journal", methods=["POST"])
def api_journal():
	data = request.get_json() or {}
	user_id = data.get('user_id', 'anon')
	journal_text = data.get('text', '')
	# Summarize journal (GPT-4.1 / GPT-4o-mini)
	summary = summarize_journal(journal_text)
	# Persist journal and summary (placeholder)
	# db.journals.insert_one({...})
	return jsonify({"summary": summary})

@app.route("/api/journals", methods=["GET"])
def api_journals():
	# In production: fetch user's journal entries from DB, compute weekly summaries and mood trends.
	sample_entries = [
		{"id": "e1", "date": "2025-11-20", "text": "Felt anxious about a conversation, but we resolved it.", "summary": "Anxiety then resolution"},
		{"id": "e2", "date": "2025-11-22", "text": "A calm day, worked on self-care.", "summary": "Calm & self-care"},
		{"id": "e3", "date": "2025-11-24", "text": "Missing partner in long-distance.", "summary": "Loneliness & longing"}
	]
	weekly_summary = {"mood_trend":"mixed", "key_themes":["anxiety","connection","self-care"]}
	return jsonify({"entries": sample_entries, "weekly_summary": weekly_summary})

@app.route("/api/affirmation", methods=["GET","POST"])
def api_affirmation_full():
	if request.method == "GET":
		user_id = request.args.get('user_id', 'anon')
		mood = request.args.get('mood', 'neutral')
		affirmation = generate_affirmation(mood, {})
		return jsonify({"affirmation": affirmation})
	else:
		# POST: save/favorite affirmation - placeholder
		data = request.get_json() or {}
		affirmation = data.get('affirmation')
		action = data.get('action', 'save')
		# Persist to DB in production
		return jsonify({"status":"ok","action":action,"affirmation":affirmation})

@app.route("/api/exercises", methods=["GET"])
def api_exercises():
	# Return sample exercises; in production this can be driven by DB + AI recommendations
	exercises = [
		{"id": 1, "title": "Active Listening Exercise", "desc": "Practice 10 minutes of focused listening."},
		{"id": 2, "title": "Gratitude Reflection", "desc": "Write three things you're grateful for."},
		{"id": 3, "title": "Grounding Activity", "desc": "5-4-3-2-1 sensory technique."},
		{"id": 4, "title": "Communication Challenge", "desc": "Practice saying 'I feel...' statements."}
	]
	return jsonify({"exercises": exercises})

@app.route("/api/avatar", methods=["POST"])
def api_avatar():
	# Avatar generation endpoint: accepts uploaded image and style params
	if 'file' not in request.files:
		return jsonify({"error": "No file provided"}), 400
	file = request.files['file']
	style = request.form.get('style', 'dreamy')
	if file.filename == '' or not allowed_file(file.filename):
		return jsonify({"error": "Invalid file"}), 400
	filename = secure_filename(file.filename)
	save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	file.save(save_path)
	# Call Avatar API (recommendation: Replicate / Stability AI / FaceSwap API)
	# Example: send save_path + style to remote service and return generated asset URL
	# For now return placeholder
	return jsonify({"status": "uploaded", "file": filename, "style": style})

@app.route("/api/profile/user-data", methods=["POST"])
def api_save_user_data():
	data = request.get_json() or {}
	# Placeholder: validate and save to DB
	# db.users.update_one({...}, {'$set': data})
	return jsonify({"status": "ok", "message": "User data saved"})

@app.route("/api/profile/preferences", methods=["POST"])
def api_save_preferences():
	data = request.get_json() or {}
	# Placeholder: save preferences to DB and apply to chat behavior
	# db.users.update_one({...}, {'$set': {'preferences': data}})
	return jsonify({"status": "ok", "message": "Preferences saved", "preferences": data})

@app.route("/api/profile/personal-settings", methods=["POST"])
def api_save_personal_settings():
	data = request.get_json() or {}
	# Placeholder: save personal settings to DB
	# db.users.update_one({...}, {'$set': {'personal_settings': data}})
	return jsonify({"status": "ok", "message": "Personal settings saved"})


# Basic error handlers
@app.errorhandler(413)
def request_entity_too_large(error):
	return jsonify({"error": "File too large"}), 413

@app.errorhandler(500)
def server_error(e):
	return jsonify({"error": "Server error"}), 500

if __name__ == "__main__":
	# In production replace with gunicorn/uvicorn and proper config
	app.run(debug=True, host="0.0.0.0", port=5000)
