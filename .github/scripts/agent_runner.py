import os
import google.generativeai as genai

# Configure secure Google Gemini API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY secret is not set in GitHub repository settings.")

genai.configure(api_key=api_key)
# Utilizing advanced Gemini reasoning capabilities for executive agent coordination
model = genai.GenerativeModel('gemini-2.5-flash')

def run_presidential_agent_swarm():
    print("👑 Initializing Presidential Multi-Agent Executive Swarm for LifelongCoaches.co.uk...")
    
    master_directive = """
    You are the CTO Agent heading an elite executive multi-agent software engineering team building LifelongCoaches.co.uk.
    Target Audience: Ultra-successful, affluent seniors and high-net-worth individuals who view health, strength, and longevity as the ultimate status symbol (out-performing younger generations in vitality and independence).
    Pricing Model: £30-£60/hr paid directly to independent local coaches; coaches pay £25/month after a 2-month free trial.
    
    The Departmental Heads (UX Director, Growth/SEO Director, Backend Architect, and Creative Media Director) must now coordinate their reports to optimize the platform's code, structure, and asset placeholders.
    
    Provide an executive briefing and actionable code/asset updates for the repository to maintain world-class prestige.
    """
    
    response = model.generate_content(master_directive)
    
    print("\n================== EXECUTIVE SWARM REPORT ==================")
    print(response.text)
    print("============================================================")
    print("👑 Presidential Agent Swarm execution completed successfully.")

if __name__ == "__main__":
    run_presidential_agent_swarm()
