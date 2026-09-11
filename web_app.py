"""
Giao diện web cho run_assistant() (Block 4 — Mini-Project).

Chạy: python web_app.py
Mở:   http://127.0.0.1:5000
"""

import json
import os

from flask import Flask, Response, render_template, request, stream_with_context

from template import (
    OPENAI_MODEL,
    batch_compare,
    count_tokens,
    estimate_cost,
    retry_with_backoff,
)

MAX_COMPARE_PROMPTS = 10

app = Flask(__name__)

STATS_MARKER = "\x00STATS\x00"
ERROR_MARKER = "\x00ERROR\x00"

DEFAULT_PERSONA = (
    "Bạn là thư ký chuyên nghiệp của giám đốc, hỗ trợ quản lý "
    "lịch trình, công việc và trao đổi bằng tiếng Việt."
)


@app.route("/")
def index():
    return render_template("index.html", default_persona=DEFAULT_PERSONA)


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True) or {}
    persona = (data.get("persona") or DEFAULT_PERSONA).strip()
    message = (data.get("message") or "").strip()
    history = data.get("history") or []

    if not message:
        return {"error": "Thiếu nội dung tin nhắn."}, 400

    messages = [{"role": "system", "content": persona}] + history + [
        {"role": "user", "content": message}
    ]

    def generate():
        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL"),
            )
            stream = retry_with_backoff(
                lambda: client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=messages,
                    stream=True,
                )
            )

            reply_parts = []
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                if delta:
                    reply_parts.append(delta)
                    yield delta

            reply = "".join(reply_parts)
            cost = estimate_cost(message, reply, OPENAI_MODEL)
            stats = {
                "reply": reply,
                "input_tokens": cost["input_tokens"],
                "output_tokens": cost["output_tokens"],
                "total_cost": cost["total_cost"],
            }
            yield STATS_MARKER + json.dumps(stats)
        except Exception as exc:
            yield ERROR_MARKER + str(exc)

    return Response(stream_with_context(generate()), mimetype="text/plain")


@app.route("/api/compare", methods=["POST"])
def compare():
    data = request.get_json(force=True) or {}
    raw_prompts = data.get("prompts") or []
    prompts = [p.strip() for p in raw_prompts if isinstance(p, str) and p.strip()]

    if not prompts:
        return {"error": "Cần ít nhất 1 prompt."}, 400
    if len(prompts) > MAX_COMPARE_PROMPTS:
        return {"error": f"Chỉ so sánh tối đa {MAX_COMPARE_PROMPTS} prompt/lần."}, 400

    try:
        results = batch_compare(prompts)
    except Exception as exc:
        return {"error": str(exc)}, 500

    return {"results": results}


if __name__ == "__main__":
    app.run(debug=True)
