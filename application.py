import os
from pathlib import Path

from flask import Flask, request, jsonify, render_template

from graph import graph


def create_application():
    base_dir = Path(__file__).resolve().parent
    templates_path = str(base_dir / "templates")
    static_path = str(base_dir / "static")

    application = Flask(
        __name__,
        template_folder=templates_path,
        static_folder=static_path
    )

    @application.route("/", methods=["GET"])
    def index():
        return render_template("chat.html")

    @application.route("/api/chat", methods=["POST"])
    def chat():
        payload = request.get_json(silent=True)

        if not payload:
            return jsonify({"error": "invalid_json"}), 400

        question = payload.get("question", "").strip()
        conversation_history = payload.get("history", [])

        if not question:
            return jsonify({"error": "question_required"}), 400

        try:
            state = {
                "question": question,
                "conversation_history": conversation_history,
            }

            result = graph.invoke(state)
            answer = result.get("final_answer", "")

            return jsonify({"answer": answer})

        except Exception as exc:
            return jsonify(
                {
                    "error": "server_error",
                    "message": str(exc)
                }
            ), 500

    return application



application = create_application()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)