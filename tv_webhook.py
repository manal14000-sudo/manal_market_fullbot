import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
load_dotenv()
SECRET = os.getenv("TV_WEBHOOK_SECRET","change_me")
app = Flask(__name__)

@app.route("/tv-hook", methods=["POST"])
def tv_hook():
    try:
        data = request.get_json(force=True)
        if data.get("secret") != SECRET:
            return jsonify({"ok": False, "error": "unauthorized"}), 401
        # types: price_update, target_hit, breakout_true, breakout_false, support_break, resistance_break
        # TODO: integrate with bots via a message queue or direct telegram API if desired.
        return jsonify({"ok": True, "received": data})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
