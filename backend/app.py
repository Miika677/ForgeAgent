#Forging Game SPA with AI Agent Helper
#Author: Miika677
import os
from backend.agent import PlayerAgent
from backend.environment import ForgeEnvironment
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, ValidationError



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

class Action(BaseModel):
    action_name : str
    speed : int
    repeats : int

player = PlayerAgent()
game = ForgeEnvironment()

@app.get("/")
def index():
    path = os.path.join(frontend_path, "index.html")
    return FileResponse(path)

#Get static data from the game's set base values for frontend
@app.get("/initiatevalues")
def initial_state():
    return game.initial_state()

#Update frontend dynamically with game state
@app.get("/state")
def get_state():
    return game.get_state()

@app.post("/reset", status_code=204)
def reset_state():
    game.reset_state()
    return {"status": "ok"}

@app.post("/manualaction")
def manual_action(req : Action):
    game.choose_action(req.action_name, req.speed, req.repeats)
    return {"action_name": req.action_name,
            "speed": req.speed,
            "repeats": req.repeats}


@app.post("/aiaction")
def ai_action():
    #Ask AI for action with speed and repeats as JSON str, based on game state.
    #Returns a list with index 0 being the JSON and index 1 the reasoning
    ai_choice_list = player.think(game.get_state())

    #Validate JSON part against Pydantic model
    try:
        action_obj = Action.model_validate_json(ai_choice_list[0])
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail="AI returned invalid action format")
    
    reasoning = ai_choice_list[1]

    game.choose_action(action_obj.action_name, action_obj.speed, action_obj.repeats)

    #For AI auto-completion: stops the auto-completion process if max progress or max fails is reached
    stop = False
    state_dict = game.get_state() | game.initial_state()
    if state_dict.get("progress") >= state_dict.get("progressMax") or state_dict.get("failCount") >= state_dict.get("failCountMax"):
        stop = True

    return {"lastAction": action_obj.action_name,
            "lastSpeed": action_obj.speed,
            "lastRepeats": action_obj.repeats,
            "lastReasoning": reasoning,
            "gameCompleted": stop}
