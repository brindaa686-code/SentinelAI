import ollama


def query_model(model: str, prompt: str) -> str:
    """
    Query an Ollama model and return the full response as a string.
    """
    stream = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    output = ""
    for chunk in stream:
        # ollama.chat's stream yields {"message": {"content": "..."}, ...}
        piece = chunk.get("message", {}).get("content", "")
        output += piece
    return output.strip()


def explain_findings(model: str, user_message: str, scored_findings: list) -> str:
    """
    Ask the LLM to describe, in plain language, what the detection
    pipeline found -- lets the agent talk to the user about attacks
    instead of just returning raw labels.
    """
    if not scored_findings:
        findings_text = "No suspicious activity was found in the analyzed logs."
    else:
        lines = [
            f"- {', '.join(f['attacks'])} (severity: {f['severity']}) "
            f"at {f['time']} -- log line: {f['log_entry']}"
            for f in scored_findings
        ]
        findings_text = "\n".join(lines)

    prompt = (
        "You are a cybersecurity assistant embedded in a monitoring agent. "
        "The detection engine just scanned firewall/log data and found the "
        f"following:\n\n{findings_text}\n\n"
        f'The user asked: "{user_message}"\n\n'
        "Explain what was found in plain, non-technical language, mention "
        "the most serious item first, and suggest one clear next step. "
        "Keep it under 120 words."
    )
    return query_model(model, prompt)