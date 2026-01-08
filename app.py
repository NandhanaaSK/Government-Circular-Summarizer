import os
import requests
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from utils.pdf_extractor import extract_text_from_pdf
from utils.text_cleaner import clean_text
from models.summarizer import summarize_text   # ✅ UPDATED summarizer
from utils.category_detector import detect_category

# ---------------- Flask App Setup ----------------
app = Flask(__name__)

# ---------------- Upload Folder ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------------- Static Recent Updates ----------------
RECENT_UPDATES = [
    {"title": "New Education Policy Guidelines", "date": "02 Jan 2026", "category": "Education"},
    {"title": "Health Insurance Scheme Extension", "date": "28 Dec 2025", "category": "Health"},
    {"title": "Income Tax Filing Deadline Extended", "date": "20 Dec 2025", "category": "Finance"},
]

# ---------------- Fetch News ----------------
def fetch_news(category):
    return []  # keeping empty so fallback circulars show

# ---------------- Routes ----------------
@app.route("/")
def index():
    return render_template(
        "index.html",
        updates=RECENT_UPDATES,
        active_page="home"
    )

# ==================== SUMMARIZE ROUTE ====================
@app.route("/summarize", methods=["POST"])
def summarize():
    text = ""

    # ---- File Upload ----
    if "file" in request.files and request.files["file"].filename:
        file = request.files["file"]
        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        text = extract_text_from_pdf(path)

    # ---- Pasted Text ----
    elif request.form.get("pasted_text"):
        text = request.form.get("pasted_text")

    if not text.strip():
        return "No input text provided", 400

    # ✅ GET SUMMARY LENGTH FROM UI
    length = request.form.get("length", "medium")

    # ---- Clean Text ----
    cleaned = clean_text(text)

    # ✅ MAIN CHANGE: BULLET‑POINT SUMMARY
    summary_points = summarize_text(cleaned, length)

    # ---- Detect Category ----
    category = detect_category(cleaned)

    # ---- Send to result.html ----
    return render_template(
        "result.html",
        summary_points=summary_points,   # ✅ bullets
        category=category,
        updates=RECENT_UPDATES,
        active_page="result",
    )

# ==================== CATEGORY ROUTE ====================
@app.route("/category/<name>")
def category_view(name):
    news = fetch_news(name)
    return render_template(
        "category.html",
        category=name.title(),
        news=news,
        active_page=name.lower(),
    )

# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)
