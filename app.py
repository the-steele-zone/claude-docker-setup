#!/usr/bin/env python3
"""
Claude Docker Application
GitHub App webhook handler + Claude chat
"""

import hashlib
import hmac
import json
import os

from anthropic import Anthropic
from flask import Flask, abort, jsonify, request

app = Flask(__name__)

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")


def verify_signature(payload: bytes, signature: str) -> bool:
    expected = "sha256=" + hmac.new(
        WEBHOOK_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@app.route("/webhook", methods=["POST"])
def webhook():
    sig = request.headers.get("X-Hub-Signature-256", "")
    if WEBHOOK_SECRET and not verify_signature(request.data, sig):
        abort(401, "Invalid signature")

    event = request.headers.get("X-GitHub-Event", "unknown")
    payload = request.get_json(silent=True) or {}

    print(f"[webhook] event={event} action={payload.get('action', '-')}")

    return jsonify({"ok": True, "event": event})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


def chat():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")

    client = Anthropic(api_key=api_key)
    history = []

    print("=== Claude Docker Application ===")
    print("Type your message and press Enter (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                messages=history,
            )
            msg = response.content[0].text
            print(f"\nClaude: {msg}\n")
            history.append({"role": "assistant", "content": msg})
        except Exception as e:
            print(f"Error: {e}")
            history.pop()


if __name__ == "__main__":
    mode = os.environ.get("MODE", "web")
    if mode == "chat":
        chat()
    else:
        app.run(host="0.0.0.0", port=8000, debug=False)
