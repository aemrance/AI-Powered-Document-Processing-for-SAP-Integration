# pdf_text_split_extractor.py

import requests
import json

# ✅ Dummy/mock PDF extraction for now (replace with real logic later)
def extract_text(pdf_path):
    print(f"📄 (Mock) Extracting text from: {pdf_path}")
    return [
        {"page_number": 1, "text": "Goods Receipt Number: 4501234567\nYear: 2021"},
        {"page_number": 2, "text": "MBLNR: 4507654321\nMJAHR: 2022"}
    ]

# ✅ LLM-based field extractor
def with_llm(page_text):
    prompt = (
        "You are a strict JSON extractor.\n"
        "Extract the following fields from this document page:\n"
        "- MBLNR (Goods Receipt Number)\n"
        "- MJAHR (Year)\n"
        "Text:\n" + page_text + "\n\n"
        "Respond only with valid JSON in the form:\n"
        "{\"MBLNR\": \"...\", \"MJAHR\": \"...\"}"
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "deepseek-llm:7b-chat",
                "stream": False,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
    except requests.RequestException as e:
        print("❌ LLM request failed:", e)
        return {}

    if response.status_code != 200:
        print(f"❌ LLM call failed with status code: {response.status_code}")
        return {}

    content = response.json().get("message", {}).get("content", "")

    try:
        start = content.find("{")
        end = content.rfind("}") + 1
        json_data = content[start:end]
        data = json.loads(json_data)
        return {
            "MBLNR": data.get("MBLNR"),
            "MJAHR": data.get("MJAHR")
        }
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        print("↩️ Raw response:", content)
        return {}
