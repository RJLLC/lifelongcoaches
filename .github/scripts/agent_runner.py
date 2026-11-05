import os
import re
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY secret is not set.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

# Locate all index.html paths so Cloudflare updates regardless of root directory setting
TARGET_FILES = ["index.html", "Desktop/landing/index.html"]

def extract_html(text):
    match = re.search(r"```html\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    if "<!DOCTYPE html>" in text or "<html" in text:
        return text.strip()
    return None

def run_autonomous_builder():
    primary_file = "index.html"
    if not os.path.exists(primary_file) and os.path.exists("Desktop/landing/index.html"):
        primary_file = "Desktop/landing/index.html"

    with open(primary_file, "r", encoding="utf-8") as f:
        current_html = f.read()

    prompt = f"""
    You are the Elite Presidential Engineering Swarm for LifelongCoaches.co.uk.
    Below is the current production `index.html` file.
    
    Execute the following mandatory V1 upgrades directly into the code:
    1. FIX BADGE OVERLAP: Fix the CSS flex/grid header on the practitioner cards so 'MASTER PRACTITIONER', 'FULLY INSURED', 'ACCEPTING CLIENTS', and the distance pill ('2.4 miles away') have clean spacing and never overlap or clip.
    2. WORKING POSTCODE & GOAL FILTERING: Add clean vanilla JavaScript so entering a postcode (e.g., SW1X, W1K, BH13) and selecting a Longevity Focus dynamically filters and sorts the displayed practitioner cards, calculating simulated proximity and updating the UI smoothly.
    3. EXPAND THE ELITE ROSTER: Add 4 additional ultra-credible UK practitioner cards across key affluent regions (e.g., Surrey/Wentworth, Cotswolds, Sandbanks/Poole, Edinburgh) with distinct specialisms (Bone Density, Post-Operative Mobility, Neuromuscular Balance, Cardiovascular Longevity) and rates between £30/hr and £60/hr.
    4. INTERACTIVE MODALS: Build sleek luxury modal popups in HTML/CSS/JS triggered when clicking 'SECURE CONSULTATION', 'SHORTLIST', 'PRACTITIONER SIGN IN', and 'APPLY FOR FOUNDING PRACTITIONER STATUS' (featuring the 2-month free trial and £25/mo tier).
    
    Return ONLY the complete, valid, production-ready `index.html` code wrapped in a ```html ... ``` codeblock. Do not truncate any code.

    CURRENT HTML:
    {current_html}
    """

    print("Executing multi-agent code synthesis and writing directly to repository files...")
    response = model.generate_content(prompt)
    updated_html = extract_html(response.text)

    if updated_html and len(updated_html) > 1000:
        for path in TARGET_FILES:
            if os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write(updated_html)
                print(f"Successfully updated and saved: {path}")
    else:
        raise RuntimeError("Agent output did not contain valid complete HTML.")

if __name__ == "__main__":
    run_autonomous_builder()
