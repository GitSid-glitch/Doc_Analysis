# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})

# if not os.path.exists("uploads"):
#     os.makedirs("uploads")

# @app.route("/upload", methods=["POST"])
# def upload():
#     file = request.files.get("file")
#     if not file:
#         return jsonify({"error": "No file uploaded"}), 400

#     filename = file.filename
#     filepath = os.path.join("uploads", filename)
#     file.save(filepath)
#     return jsonify({"message": f"Received {filename}"}), 200

# if __name__ == "__main__":
#     app.run(port=5001, debug=True)






# backend/app.py
# import os
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from pypdf import PdfReader
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables from .env
# load_dotenv()

# app = Flask(__name__, static_folder="static")
# CORS(app, resources={r"/*": {"origins": "*"}})

# UPLOAD_FOLDER = "uploads"
# STATIC_FOLDER = "static"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(STATIC_FOLDER, exist_ok=True)

# # Simple in-memory store for last uploaded document text
# LAST_DOCUMENT = {"filename": None, "text": ""}

# # Configure Gemini
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# if OPENROUTER_API_KEY:
#     genai.configure(api_key=OPENROUTER_API_KEY)
# else:
#     print("⚠️ OPENROUTER_API_KEY not set. /ask will return an error.")


# def extract_text_from_pdf(filepath: str) -> str:
#     """Extract text from a PDF using pypdf."""
#     text_parts = []
#     try:
#         reader = PdfReader(filepath)
#         for page in reader.pages:
#             try:
#                 t = page.extract_text()
#             except Exception:
#                 t = ""
#             if t:
#                 text_parts.append(t)
#     except Exception as e:
#         print("PDF extract error:", e)
#     return "\n".join(text_parts)


# @app.route("/upload", methods=["POST"])
# def upload():
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"error": "Empty filename"}), 400

#     filename = file.filename
#     filepath = os.path.join(UPLOAD_FOLDER, filename)
#     file.save(filepath)

#     # Extract text from PDF
#     extracted_text = extract_text_from_pdf(filepath)
#     LAST_DOCUMENT["filename"] = filename
#     LAST_DOCUMENT["text"] = extracted_text

#     # TODO: table/chart extraction if you want later
#     charts = []  # e.g. ["chart1.png"]
#     tables = []

#     return jsonify({
#         "message": f"Received {filename}",
#         "filename": filename,
#         "text": extracted_text[:8000],  # send a reasonable preview length
#         "tables": tables,
#         "charts": charts
#     }), 200


# def gemini_answer(question: str, context_text: str) -> str:
#     """Use Gemini to answer a question about the document context."""
#     if not OPENROUTER_API_KEY:
#         return "Gemini API key not configured on the server."

#     # Limit context length so we don't blow up tokens
#     # (Gemini has big context, but still good practice)
#     context_send = context_text[:20000]

#     prompt = (
#         "You are a helpful assistant that answers questions about a document.\n\n"
#         "Document content:\n"
#         f"{context_send}\n\n"
#         f"Question: {question}\n\n"
#         "Answer clearly and concisely."
#     )

#     try:
#         model = genai.GenerativeModel("gemini-2.0-flash")
#         resp = model.generate_content(prompt)
#         # google-generativeai usually gives .text for the main content
#         return (resp.text or "").strip()
#     except Exception as e:
#         print("Gemini request error:", e)
#         return f"Error contacting Gemini: {e}"


# @app.route("/ask", methods=["POST"])
# def ask():
#     data = request.get_json(silent=True)
#     if not data:
#         return jsonify({"error": "No JSON body"}), 400

#     question = data.get("question")
#     snippet = data.get("snippet", "")

#     if not question:
#         return jsonify({"error": "No question provided"}), 400

#     # Prefer snippet from frontend; fall back to last uploaded text
#     context_text = snippet or LAST_DOCUMENT.get("text", "")
#     if not context_text:
#         return jsonify({"error": "No document context available; upload a file first"}), 400

#     answer_text = gemini_answer(question, context_text)
#     return jsonify({"answer": answer_text}), 200


# # For chart images later if you save them into static/
# @app.route("/static/<path:filename>")
# def static_files(filename):
#     return send_from_directory(STATIC_FOLDER, filename)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5001, debug=True)







# import os
# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from pypdf import PdfReader
# from dotenv import load_dotenv
# import requests

# # Load environment variables from .env
# load_dotenv()

# app = Flask(__name__, static_folder="static")
# CORS(app, resources={r"/*": {"origins": "*"}})

# # Folders
# UPLOAD_FOLDER = "uploads"
# STATIC_FOLDER = "static"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(STATIC_FOLDER, exist_ok=True)

# # Store last uploaded document text in memory (simple demo)
# LAST_DOCUMENT = {"filename": None, "text": ""}

# # OpenRouter config
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# if not OPENROUTER_API_KEY:
#     print("⚠️ OPENROUTER_API_KEY is not set. /ask will return an error.")


# def extract_text_from_pdf(filepath: str) -> str:
#     """Extract text from a PDF using pypdf."""
#     text_parts = []
#     try:
#         reader = PdfReader(filepath)
#         for page in reader.pages:
#             try:
#                 t = page.extract_text()
#             except Exception:
#                 t = ""
#             if t:
#                 text_parts.append(t)
#     except Exception as e:
#         print("PDF extract error:", e)
#     return "\n".join(text_parts)


# def openrouter_answer(question: str, context_text: str) -> str:
#     """Use OpenRouter to answer a question about the document."""
#     if not OPENROUTER_API_KEY:
#         return "OpenRouter API key not configured on the server."

#     # Limit context length to avoid huge prompts
#     context_text = context_text[:12000]

#     url = "https://openrouter.ai/api/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         # Optional but recommended for OpenRouter analytics
#         "HTTP-Referer": "http://localhost:5173",
#         "X-Title": "AI Document Analyzer",
#     }

#     payload = {
#         "model": "google/gemini-2.0-flash-exp:free",  # good free-ish model
#         "messages": [
#             {
#                 "role": "system",
#                 "content": (
#                     "You are a helpful assistant that answers questions "
#                     "about the provided document text."
#                 ),
#             },
#             {
#                 "role": "user",
#                 "content": (
#                     f"Document:\n{context_text}\n\n"
#                     f"Question: {question}\n\n"
#                     "Answer clearly and concisely."
#                 ),
#             },
#         ],
#         "temperature": 0.2,
#         "max_tokens": 512,
#     }

#     try:
#         resp = requests.post(url, headers=headers, json=payload, timeout=60)
#         resp.raise_for_status()
#         data = resp.json()
#         # OpenRouter is OpenAI-compatible in shape
#         return data["choices"][0]["message"]["content"].strip()
#     except Exception as e:
#         print("OpenRouter error:", e)
#         return "AI service temporarily unavailable. Please try again later."


# @app.route("/upload", methods=["POST"])
# def upload():
#     """Receive a PDF, save it, extract text, return extracted info."""
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400

#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"error": "Empty filename"}), 400

#     filename = file.filename
#     filepath = os.path.join(UPLOAD_FOLDER, filename)
#     file.save(filepath)

#     # Extract text
#     extracted_text = extract_text_from_pdf(filepath)
#     LAST_DOCUMENT["filename"] = filename
#     LAST_DOCUMENT["text"] = extracted_text

#     # You can hook in table/chart extraction later
#     charts: list[str] = []  # e.g. ["chart1.png"]
#     tables: list[dict] = []

#     return jsonify({
#         "message": f"Received {filename}",
#         "filename": filename,
#         "text": extracted_text[:8000],  # send preview; avoid massive payloads
#         "tables": tables,
#         "charts": charts,
#     }), 200


# @app.route("/ask", methods=["POST"])
# def ask():
#     """Answer a question about the last uploaded document (or snippet)."""
#     data = request.get_json(silent=True)
#     if not data:
#         return jsonify({"error": "No JSON body"}), 400

#     question = data.get("question")
#     snippet = data.get("snippet", "")

#     if not question:
#         return jsonify({"error": "No question provided"}), 400

#     # Prefer snippet sent from frontend; fall back to full last document
#     context_text = snippet or LAST_DOCUMENT.get("text", "")
#     if not context_text:
#         return jsonify({"error": "No document context available; upload a file first"}), 400

#     answer_text = openrouter_answer(question, context_text)
#     return jsonify({"answer": answer_text}), 200


# @app.route("/static/<path:filename>")
# def static_files(filename):
#     """Serve static files (e.g., chart images) if you add them later."""
#     return send_from_directory(STATIC_FOLDER, filename)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5001, debug=True)






import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from utils.text_extraction import extract_pdf_text, extract_docx_text
from utils.table_extraction import extract_pdf_tables
from utils.chart_extraction import extract_charts
from utils.eda import describe_table
from utils.ai_integration import ask_ai  # uses OpenRouter

load_dotenv()

app = Flask(__name__, static_folder="static")
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# store current document in memory for /ask
CURRENT_DOC = {
    "filename": None,
    "text": "",
    "tables": [],   # list of table dicts (for frontend)
    "charts": [],   # list of chart filenames (for frontend)
}


def build_table_payload(dfs):
    """
    Convert list of pandas DataFrames into JSON-serializable structures
    with both a small preview and a describe() summary.
    """
    tables_payload = []
    for df in dfs:
        try:
            summary = describe_table(df)  # your eda.py
        except Exception as e:
            print("describe_table error:", e)
            summary = {}

        # small preview of first few rows so you can inspect data itself
        preview = {
            "columns": list(map(str, df.columns)),
            "rows": df.head(5).values.tolist(),
        }

        tables_payload.append({
            "preview": preview,
            "summary": summary,
        })

    return tables_payload


@app.route("/upload", methods=["POST"])
def upload():
    """
    Receive a file (PDF or DOCX), save it, run text/table/chart extraction,
    and return results for frontend.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    ext = os.path.splitext(filename)[1].lower()

    text = ""
    tables_payload = []
    chart_filenames = []

    # ---- TEXT ----
    try:
        if ext == ".pdf":
            text = extract_pdf_text(filepath)
        elif ext == ".docx":
            text = extract_docx_text(filepath)
        else:
            return jsonify({"error": f"Unsupported file type: {ext}"}), 400
    except Exception as e:
        print("text extraction error:", e)
        text = ""

    # ---- TABLES (PDF only) ----
    if ext == ".pdf":
        try:
            dfs = extract_pdf_tables(filepath)  # list of DataFrames
            tables_payload = build_table_payload(dfs)
        except Exception as e:
            print("table extraction error:", e)
            tables_payload = []

    # ---- CHARTS (PDF only) ----
    if ext == ".pdf":
        try:
            chart_paths = extract_charts(filepath, output_dir=STATIC_FOLDER)
            # keep only filenames; frontend uses /static/<filename>
            chart_filenames = [os.path.basename(p) for p in chart_paths]
        except Exception as e:
            print("chart extraction error:", e)
            chart_filenames = []

    # store for /ask
    CURRENT_DOC["filename"] = filename
    CURRENT_DOC["text"] = text
    CURRENT_DOC["tables"] = tables_payload
    CURRENT_DOC["charts"] = chart_filenames

    # send preview text (to avoid huge JSON), but full tables/charts
    return jsonify({
        "message": f"Received {filename}",
        "filename": filename,
        "text": text[:8000] if text else "",
        "tables": tables_payload,
        "charts": chart_filenames,
    }), 200


@app.route("/ask", methods=["POST"])
def ask():
    """
    Use AI (OpenRouter via ask_ai) to answer a question about the current document.
    Uses either snippet from frontend or full text + table summaries.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No JSON body"}), 400

    question = data.get("question")
    snippet = data.get("snippet", "")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # context: prefer snippet from frontend; otherwise full text + table summaries
    context_text = snippet.strip()
    if not context_text:
        context_text = CURRENT_DOC.get("text", "")

        # append light table info if present
        tables = CURRENT_DOC.get("tables") or []
        if tables:
            context_text += "\n\nTable summaries:\n"
            for i, t in enumerate(tables, start=1):
                # t["summary"] is already a dict from describe_table
                context_text += f"Table {i} summary: {str(t.get('summary', {}))[:500]}\n"

    if not context_text:
        return jsonify({"error": "No document context available; upload a file first"}), 400

    answer_text = ask_ai(question, context_text)
    return jsonify({"answer": answer_text}), 200


@app.route("/static/<path:filename>")
def static_files(filename):
    """Serve chart images extracted into the static/ folder."""
    return send_from_directory(STATIC_FOLDER, filename)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
