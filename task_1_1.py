from template import call_openai

prompt = "Hãy kể cho tôi một sự thật thú vị về Việt Nam."

for t in [0.0, 0.5, 1.0, 1.5]:
    text, latency = call_openai(prompt, temperature=t)
    print(f"--- temperature={t} (latency={latency:.2f}s) ---")
    print(text)
    print()
