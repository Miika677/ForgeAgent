import os
from backend.prompts import build_prompt, get_end_json, get_reasoning
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = genai.Client(api_key=api_key)

class PlayerAgent:

    #Generate prompt, get the result and turn it into a JSON string
    def think(self, envstate : dict) -> list:
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[build_prompt(envstate)]
        )

        action_json = get_end_json(response.text)
        reasoning = get_reasoning(response.text)
        return [action_json, reasoning]
        

    