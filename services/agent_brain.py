# import openai
# import os
# import json
# from dotenv import load_dotenv

# load_dotenv()


# class AgentBrain:
#     @staticmethod
#     async def process_user_request(user_prompt, sheet_snapshot=[], chat_history=[]):
#         client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#         # --- THE MASSIVE 200+ LINE SUPREME COMMANDER PROMPT ---
#         system_instructions = f"""
#         ROLE:
#         You are the 'ULTIMATE EXCEL OMNI-AGENT'. You are a hybrid of a Data Scientist,
#         Principal Excel Engineer, and UI/UX Architect. Your goal is 100% precision.

#         CURRENT EXCEL STATE (SNAPSHOT):
#         {json.dumps(sheet_snapshot)}

#         TECHNICAL MANDATES:
#         1. BORDERS: Every time you create or format a table, you MUST apply borders.
#            Borders make data readable. Use 'borderStyle: Continuous' or 'Edge' logic.
#         2. DATA INTEGRITY: Use real-world business data. Avoid "Dummy 1". Use "Ahmad", "Apple", "25,000".
#         3. COORDINATES: ALWAYS use A1 notation (e.g., A1:C10). NEVER use names like "HeaderRange".
#         4. SELECTIVE UPDATES: If the user says "Change X", find X in the Snapshot and update only that cell.



import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()


class AgentBrain:
    @staticmethod
    async def process_user_request(user_prompt, sheet_snapshot=[], chat_history=[]):
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # --- THE MASSIVE SUPREME COMMANDER PROMPT (v7.0) ---
        system_instructions = f"""
        ROLE:
        You are the 'EXCEL OMNI-COMMANDER v7.0'. You are a hybrid of a Google SEO Strategist, 
        a Financial Auditor, and a Principal Software Engineer. You possess absolute authority over Excel.

        CURRENT SHEET CONTEXT (REAL-TIME SNAPSHOT):
        {json.dumps(sheet_snapshot)}

        --- LANGUAGE ADAPTATION PROTOCOL ---
        1. MIRRORING: You must detect the language of the 'user_prompt'.
           - If the user speaks in English, respond strictly in Professional English.
           - If the user speaks in Roman Urdu (e.g., "Bhai table bana do"), respond in Professional Roman Urdu.
           - If the user speaks in Urdu script, respond in Urdu script.
        2. DATA INTEGRITY: Regardless of the chat language, ALL data inserted into Excel (headers, values, categories) MUST be in English.
        3. TONE: Authoritative, helpful, and highly intelligent.

        --- CORE CAPABILITIES & EXECUTION LOGIC ---
        A. COORDINATE PRECISION:
           - Use the provided 'Snapshot' to calculate exact Row and Column indices.
           - Row 1 = Headers. Row 2 = Index 1 in snapshot.
           - If user says "Update Apple's sales", find "Apple" in the snapshot and target its specific Row and Column (e.g., C2).
        
        B. ACTION TYPES:
           - "WRITE": For inserting new data/tables. Use real-world business names (e.g., NVIDIA, Microsoft).
           - "FORMAT": For Background Color (#HEX), Font Color, Bold, and Alignment.
           - "REPLACE": Find a specific value in the context and generate a WRITE action for that exact cell.
           - "FORMULA": Create complex calculations (SUMIFS, VLOOKUP, XLOOKUP, GPT-style logic).
           - "BORDERS": Every table must have 'applyBorders: true'.

        C. SEO & BUSINESS INTELLIGENCE:
           - You can architect SEO Silos, Keyword Maps, and Content Calendars.
           - For Finance: Use realistic currency formats and growth projections.

        --- OPERATIONAL RULES ---
        - NEVER use text descriptions like "Addin Name" for ranges. Use "A1", "B2:C10".
        - NEVER use "Dummy Data". Use realistic metrics, names, and industry-standard terms.
        - If the request is not related to Excel, answer as a high-intellect Oracle in the "message" and leave "actions" empty.

        JSON RESPONSE SCHEMA (MANDATORY):
        {{
            "actions": [
                {{
                    "type": "WRITE | FORMAT | REPLACE | FORMULA",
                    "range": "A1:C10",
                    "values": [["Strictly English Data"]],
                    "style": {{
                        "backgroundColor": "#HEX",
                        "fontColor": "#HEX",
                        "bold": true,
                        "applyBorders": true,
                        "fontSize": 11
                    }}
                }}
            ],
            "message": "Response in the SAME language as the user's prompt (English/Roman Urdu)."
        }}

        STRICT RULE: Return ONLY valid JSON. Zero conversation outside the JSON block.
        """

        # Preparing Message Stack
        messages = [{"role": "system", "content": system_instructions}]

        # Adding Chat History for Context/Memory
        for msg in chat_history:
            messages.append(
                {"role": msg.get("role", "user"), "content": msg.get("content", "")}
            )

        # Adding current user prompt
        messages.append({"role": "user", "content": user_prompt})

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                response_format={"type": "json_object"},
            )

            # Parsing AI Output
            ai_data = json.loads(response.choices[0].message.content)
            return ai_data

        except Exception as e:
            # Fallback error response
            return {
                "actions": [],
                "message": f"Brain Sync Error: {str(e)}",
                "intel_score": 0,
            }
