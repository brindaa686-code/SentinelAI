from llm_integration.ollama_client import query_model

def main():
    prompt = "Explain what a failed login means in cybersecurity."
    result = query_model("gemma", prompt)
    print("\nLLM Response:\n")
    print(result)

if __name__ == "__main__":
    main()