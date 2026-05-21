import google.generativeai as genai
import json

def analyze_incident(api_key, report_text):
    try:
        genai.configure(api_key=api_key)
        
        # --- SMART MODEL FINDER (The Magic Fix) ---
        # Instead of guessing, we ask the API: "What do you have?"
        working_model_name = "gemini-pro" # Default fallback
        
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    if 'gemini' in m.name:
                        working_model_name = m.name
                        break # Found one! Stop looking.
        except:
            pass # If listing fails, try the default
            
        print(f"DEBUG: Using Model -> {working_model_name}")
        model = genai.GenerativeModel(working_model_name) 
        
        # --- THE PROMPT ---
        prompt = f"""
        Act as a Disaster Response System. Analyze this report: "{report_text}"
        Return a valid JSON object (NO markdown) with these keys:
        - "category": (String) Fire, Flood, Accident, Medical, Earthquake.
        - "severity": (Integer) 1 to 10.
        - "summary": (String) max 10 words.
        - "is_real": (Boolean).
        """
        
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        
        # --- JSON PARSING ---
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end != -1:
            ai_data = json.loads(text[start:end])
        else:
            ai_data = json.loads(text)

        return {
            "type": ai_data.get('category', "Other"),
            "severity": ai_data.get('severity', 1),
            "description": ai_data.get('summary', report_text),
            "is_real": ai_data.get('is_real', False)
        }

    except Exception as e:
        print(f"AI Error: {e}")
        # Return a safe fallback so the UI doesn't crash
        return {
            "type": "Manual Report",
            "severity": 5,
            "description": f"AI Connection Issue. Raw: {report_text[:30]}...", 
            "is_real": True
        }