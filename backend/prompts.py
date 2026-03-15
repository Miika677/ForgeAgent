#AI starts hallucinating badly if the output isn't allowed to have reasoning.
def get_end_json(ai_response : str) -> str:
    start = ai_response.rfind("{")
    end= ai_response.rfind("}")
    json_str = ai_response[start:end+1]
    return json_str

def get_reasoning(ai_response : str) -> str:
    end = ai_response.rfind("{")
    response_str = ai_response[0:end]
    return response_str

def build_prompt(envstate : dict):
    return f"""You are the player of a sword-forging simulator game.

CURRENT STATE:
Progress: {envstate["progress"]} / 120
Temperature of the blade: {envstate["heat"]} / 150
Desired action: {envstate["desiredAction"]}
Fail count: {envstate["failCount"]}

GOAL:
Finish the sword by reaching 120 progress. 5 fails = game over.

TOOLS AND ACTIONS:

Progress-Increasing Actions:
- Hammer: +3-5 progress * speed, -1-5 heat, valid heat range 100-140
- Grind: +3-5 progress * speed, +1-5 heat, valid heat range 50-100
- Polish: +3-5 progress * speed, -1-5 heat, valid heat range 10-50
Speed has no effect on the on the heat change for these actions, only affecting the progress gained.

Heat-Regulating Measures:
- Lava Dunk: +5 * speed heat, no progress, no fail
- Quench: -5 * speed heat, no progress, no fail
Use these Heat-regulating measures to reach the heat range of the desired action.

HEAT RANGES (for reference):
| Action | Min Heat | Max Heat |
|--------|----------|----------|
| Hammer | 100      | 140      |
| Grind  | 50       | 100      |
| Polish | 10       | 50       |

RULES:
Progress will increase only when doing desired action in the valid heat range.
Doing a progress-increasing action that is not the desired action will result in a fail.
Doing the desired action while in the wrong heat range will result in a fail.
Desired action will change every 30 progress. This desired action is chosen randomly and may even be the same one as before.
Each action and measure can be repeated 1-10 times in a row. Heat range is checked at the start of each individual repeat.
Be careful when repeating actions at high speed; desired action can change mid repeat-sequence if progress reaches 30/60/90 during it.
Desired action will not change after reaching 120 progress.


IMPORTANT OUTPUT FORMAT:

- Show your reasoning for the choice.
- Do actions as efficiently as possible; you should reason a step ahead of the current action to minimize amount of actions needed for the goal.
- Example: Progress increasing actions also affect the temperature; therefore the temperature adjustment before these actions should take this into account
  so that multiple repeats may be done in a row which in turn reduces the amount of individual actions chosen to reach the goal.
- Keep reasoning as concise and short as possible; do not start it off with a title or anything, just get straight to reasoning.
- For quotations within the reasoning only use the normal quotation marks "".

- After all reasoning is complete,
  output a JSON object on its own line.

- The JSON object MUST be the final thing in the response.

- Do NOT put anything after the JSON.
- Do NOT wrap the JSON in markdown.
- Do NOT add commentary after the JSON.

The final lines of your output MUST be valid json in this format:

{{
  "action_name": "hammer" | "grind" | "polish" | "lava_dunk" | "quench",
  "speed": 1 or 2,
  "repeats": 1-10
}}
"""


