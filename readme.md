# Forging Game SPA with AI Agent Helper

Complete the forging of a sword with the help of an AI agent, either with single steps or to full completion.  
Inspired by OldSchool Runescape's Giants' Foundry minigame: https://oldschool.runescape.wiki/w/Giants%27_Foundry

## AI Implementation

The basic loop for the AI Agent goes as follows:
1. Observe game state from injected game environment values
2. Select action with its repeats and intensity from a constrained toolset after reasoning for risk and reward
3. Outputs structured JSON actions for execution in game environment
4. Update game state, inject it and proceed with next step until the game is completed.

The goal is to complete the forging process efficiently while managing heat constraints, dynamic objectives, and failure penalties.
The system effectively forms a closed-loop LLM-driven decision policy operating in an environment with randomized action outcomes, constrained actions and dynamic objectives.

## How to Run

1. Create a .env file with your Google Gemini API key:  

API_KEY=yourAPIKeyHere

2. Execute run.py
3. Visit http://localhost:8000 in your browser

## How to Play

- Goal: Reach 120 progress before 5 fails. 5 fails = game over.  
- Progress only increases when performing the desired action within its valid heat range.  
- The desired action changes randomly every 30 progress (at 30, 60, 90) and may stay the same.  
- If progress crosses 30/60/90 during repeats, the desired action can change mid-sequence.

### Actions

| Action     | Effect                                      | Notes                         |
|------------|--------------------------------------------|-------------------------------|
| Hammer     | Valid heat 100-140, lowers temp            |                               |
| Grind      | Valid heat 50-100, raises temp             |                               |
| Polish     | Valid heat 10-50, lowers temp              |                               |
| Lava Dunk  | Raises temp                                 | No progress, no fail          |
| Quench     | Lowers temp                                 | No progress, no fail          |

- Wrong action at the wrong temperature / desired action will result in a fail.  
- Speed (1-2) increases progress gained per action.  
- Actions can be repeated 1-10 times.  
- Heat range is checked at the start of each individual repeat.

## Video Demo on YouTube

[![Watch the demo](https://img.youtube.com/vi/C8vgLsjBs3w/0.jpg)](https://www.youtube.com/watch?v=C8vgLsjBs3w)
