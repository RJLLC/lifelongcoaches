import os
import re
import json
import time
import google.generativeai as genai
from google.api_core import exceptions

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY secret is not set.")

genai.configure(api_key=api_key)

TARGET_FILES = ["index.html", "Desktop/landing/index.html"]
STATE_FILE = ".github/scripts/swarm_roadmap.json"

DEFAULT_ROADMAP = {
    "milestones": [
        {
            "id": 1,
            "name": "Card Layout & Luxury Badge Alignment",
            "status": "pending",
            "directive": "Fix all CSS flex/grid collisions on practitioner cards so MASTER PRACTITIONER, FULLY INSURED, ACCEPTING CLIENTS, and the distance pill never overlap on desktop or mobile. Refine typography and spacing to match ultra-luxury private client aesthetics."
        },
        {
            "id": 2,
            "name": "National Affluent Roster Expansion",
            "status": "pending",
            "directive": "Expand the practitioner roster to 6 distinct, deeply detailed UK profiles covering Mayfair, Kensington, Sandbanks/Poole (BH13), Surrey/Wentworth (GU25), Cotswolds (GL7), and Edinburgh (EH3). Ensure realistic credentials (CIMSPA, MSc, BSc, Enhanced DBS) and hourly rates between £30 and £60."
        },
        {
            "id": 3,
            "name": "Interactive UK Postcode Radius & Specialism Filtering",
            "status": "pending",
            "directive": "Implement working vanilla JavaScript for the postcode input, Longevity Focus dropdown, and Sort selector. Map UK postcode prefixes (SW, W, BH, GU, GL, EH, etc.) to coordinates so entering any UK postcode calculates realistic mile distances, sorts the cards by proximity, and updates the distance badges dynamically."
        },
        {
            "id": 4,
            "name": "Client Booking, Shortlist & £25/mo Practitioner Onboarding Modals",
            "status": "pending",
            "directive": "Wire every button ('SECURE CONSULTATION', 'SHORTLIST', 'PRACTITIONER SIGN IN', 'APPLY FOR FOUNDING PRACTITIONER STATUS') to sleek, working luxury modal dialogs with form validation, interactive state feedback, localStorage shortlist persistence, and the 2-month free trial / £25 per month subscription onboarding flow."
        },
        {
            "id": 5,
            "name": "Executive QA Polish, SEO Schema & Accessibility Audit",
            "status": "pending",
            "directive": "Audit the entire DOM and JavaScript for broken links, mobile responsiveness, JSON-LD LocalBusiness/MedicalBusiness SEO schema, and high-contrast readability for older affluent adults."
        }
    ]
}

def call_gemini(prompt, model_name="gemini-2.5-flash"):
    model = genai.GenerativeModel(model_name)
    for attempt in range(1, 5):
        try:
            return model.generate_content(prompt, request_options={"retry": None}).text
        except exceptions.ResourceExhausted:
            wait = 30 * attempt
            print(f"Rate limit hit. Cooling down {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Quota exhausted after retries.")

def extract_html(text):
    match = re.search(r"```html\s*(.*?)\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    if "<!DOCTYPE html>" in text:
        return text[text.find("<!DOCTYPE html>"):].strip()
    return None

def load_roadmap():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return DEFAULT_ROADMAP

def save_roadmap(roadmap):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(roadmap, f, indent=2)

def run_pipeline():
    roadmap = load_roadmap()
    next_milestone = next((m for m in roadmap["milestones"] if m["status"] == "pending"), None)

    primary_file = "index.html" if os.path.exists("index.html") else "Desktop/landing/index.html"
    with open(primary_file, "r", encoding="utf-8") as f:
        current_html = f.read()

    if not next_milestone:
        print("All V1 milestones completed! Running continuous QA audit...")
        directive = "Perform an incremental UX, performance, and conversion polish without breaking existing interactive features."
    else:
        print(f"🎯 Active Milestone #{next_milestone['id']}: {next_milestone['name']}")
        directive = next_milestone["directive"]

    # AGENT 1: CTO & UX Architect Deliberation
    print("Step 1/2: CTO & UX Director auditing current HTML and planning implementation...")
    architect_prompt = f"""
    You are the CTO and UX Director for LifelongCoaches.co.uk (luxury fitness marketplace for 50+ affluent adults, £30-£60/hr coaches, £25/mo coach subscription).
    Audit the current HTML below and write a strict technical specification to execute this milestone without losing any existing content or styling:
    MILESTONE: {directive}

    CURRENT HTML:
    {current_html}
    """
    spec = call_gemini(architect_prompt)
    print("Architectural specification locked. Cooling down 25s to respect free-tier rate limits...")
    time.sleep(25)

    # AGENT 2: Lead Frontend Engineer Execution
    print("Step 2/2: Lead Engineer implementing specification into production HTML...")
    engineer_prompt = f"""
    You are the Principal Frontend Engineer for LifelongCoaches.co.uk.
    Implement the following CTO Technical Specification directly into the production `index.html` code.
    CRITICAL RULES:
    - Preserve all existing sections, styling, and working features.
    - Write complete, functional vanilla JavaScript and CSS—no placeholder comments like '// add logic here'.
    - Return ONLY the complete, valid `index.html` wrapped in ```html ... ```.

    CTO SPECIFICATION:
    {spec}

    CURRENT HTML:
    {current_html}
    """
    raw_output = call_gemini(engineer_prompt)
    updated_html = extract_html(raw_output)

    if updated_html and len(updated_html) > 2000:
        for path in TARGET_FILES:
            if os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write(updated_html)
                print(f"Saved updated production file: {path}")
        if next_milestone:
            next_milestone["status"] = "completed"
            save_roadmap(roadmap)
            print(f"Marked Milestone #{next_milestone['id']} as completed in {STATE_FILE}.")
    else:
        raise RuntimeError("Generated HTML failed validation check.")

if __name__ == "__main__":
    run_pipeline()
