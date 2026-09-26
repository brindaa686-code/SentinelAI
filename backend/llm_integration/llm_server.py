from flask import Flask, request, jsonify
import datetime

from input_layer.firewall_parser import read_firewall_log
from detection_engine.pipeline import analyze_log
from decision_engine.risk_scoring import score_findings
from response_system.responder import respond
from llm_integration.ollama_client import explain_findings

app = Flask(__name__)

LLM_MODEL = "gemma"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    detections = []

    if "analyze" in user_message.lower() or "firewall" in user_message.lower():
        try:
            entries = read_firewall_log()
        except FileNotFoundError:
            return jsonify({
                "reply": "I couldn't find the firewall log to analyze -- "
                          "check the path in input_layer/firewall_parser.py.",
                "detections": [],
            })

        findings = analyze_log(entries)
        scored = score_findings(findings)

        for finding in scored:
            respond(finding)
            detections.append({
                "time": finding["time"],
                "attack": ", ".join(finding["attacks"]),
                "ip": finding["log_entry"],
                "severity": finding["severity"],
            })

        if not scored:
            detections = [{
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "attack": "none", "ip": "N/A", "severity": "low",
            }]

        try:
            reply = explain_findings(LLM_MODEL, user_message, scored)
        except Exception as e:
            reply = (
                "Detection finished, but I couldn't reach the language "
                f"model to explain it in words ({e}). Raw findings are "
                "in the detections list."
            )
    else:
        try:
            reply = explain_findings(LLM_MODEL, user_message, [])
        except Exception as e:
            reply = f"I couldn't reach the language model ({e})."

    return jsonify({"reply": reply, "detections": detections})


if __name__ == "__main__":
    app.run(port=5000, debug=True)