import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from src.agent import ClaimResponse

load_dotenv() # Loads OPENAI_API_KEY from .env file
client = OpenAI()

SYSTEM_PROMPT = """
You are an insurance agent. Extract data from FNOL documents into JSON.
Rules:
- If a field is missing, return null.
- Extract 'estimated_damage' as a float/number only.
- 'claim_type' must be 'auto', 'property', or 'injury'.
"""

def process_fnol(text_content: str):
    # Pass 1: LLM Extraction
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text_content}
        ],
        response_format={"type": "json_object"}
    )
    
    extracted_json = json.loads(response.choices[0].message.content)
    
    # Pass 2: Logic & Routing Engine
    # We nest the extracted fields into our ClaimResponse model
    agent_output = ClaimResponse(extractedFields=extracted_json)
    
    return agent_output.model_dump_json(indent=2)

if __name__ == "__main__":
    # Example Test Case (Fast-Track)
    sample_fnol = """
    Policy: ABC-999. Holder: Alice Smith. 
    On Feb 5th, I backed into a mailbox at 10mph. 
    Minor dent in rear bumper. Estimated repair cost: $1,200.
    Type: Auto.
    """
    
    print("--- Processing Claim ---")
    result = process_fnol(sample_fnol)
    print(result)
