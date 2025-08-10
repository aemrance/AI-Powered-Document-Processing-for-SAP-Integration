from myextractor import extract_text, with_llm
import json

INPUT_PDF = "batch_3_2021.pdf"
OUTPUT_JSON = "final_output.json"

def main():
    print(f"📄 Extracting from: {INPUT_PDF}")
    pages = extract_text(INPUT_PDF)  # 🔁 FIXED
    results = []

    for page in pages:
        page_number = page.get("page_number", "Unknown")
        print(f"🔍 Page {page_number}")
        fields = with_llm(page.get("text", ""))  # 🔁 FIXED

        fields.setdefault("MBLNR", None)
        fields.setdefault("MJAHR", None)
        fields["page_number"] = page_number

        results.append(fields)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Done. Results saved to '{OUTPUT_JSON}'")

if __name__ == "__main__":
    main()
