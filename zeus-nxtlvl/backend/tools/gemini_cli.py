import os
import argparse
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")


def generate_text(prompt: str) -> str:
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY not set")

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="Gemini text generation CLI")
    parser.add_argument("prompt", help="Prompt text")
    args = parser.parse_args()
    print(generate_text(args.prompt))


if __name__ == "__main__":
    main()
