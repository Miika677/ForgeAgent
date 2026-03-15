import * as Game from "./game.js";

window.manualAction = Game.manualAction;
window.aiActionToGoal = Game.aiActionToGoal;
window.aiAction = Game.aiAction;
window.resetGame = Game.resetGame;


//Set initial values in HTML
window.addEventListener("DOMContentLoaded", async () => {
    await Game.initiateValues();
});







