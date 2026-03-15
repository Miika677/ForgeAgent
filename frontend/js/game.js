import { apiRequest } from "./api.js";
import { setupInitialValues, updateState, lastAIActionUpdate, toggleButtons, resetFailCount, UI } from "./ui.js";

//Fetch initial static values from the game; needed progress, max amount of fails
export async function initiateValues() {
    const initialValues = await apiRequest("/initiatevalues", {});
    setupInitialValues(initialValues);
    await updateState();
}

export async function manualAction(action) {
    const actionMessageResponse = await apiRequest("/manualaction", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
            action_name: action,
            speed: Number(UI.manualSpeedField.value),
            repeats: Number(UI.manualRepeatsField.value)})
        });
        await updateState(actionMessageResponse.action_name);
}

export async function aiAction(pressedButton) {
    //Disable all action buttons during the AI api call
    toggleButtons(".action-button, .auto-button, .reset-button", false);
    pressedButton.textContent = "Processing...";
    UI.loader.style.display = "grid";

    //Wait for redraw before fetching
    await new Promise(resolve => requestAnimationFrame(resolve));

    const resJSON = await apiRequest("/aiaction", {method: "post"})
    if (resJSON) {
        await updateState(resJSON.lastAction);
        lastAIActionUpdate(resJSON);
    }

    toggleButtons(".action-button, .auto-button, .reset-button", true);
    pressedButton.textContent = "Let AI Act";
    UI.loader.style.display = "none";
    console.log("All done");
}

let autoCompleteRunning = false;
export async function aiActionToGoal(pressedButton) {
    if (!autoCompleteRunning) {
        console.log("Started");
        autoCompleteRunning = true;

        //Disable all action buttons except this one during the AI api call
        toggleButtons(".action-button, .reset-button", false);
        pressedButton.textContent = "Stop AI";

        UI.loader.style.display = "grid";

        //Wait for redraw before starting fetch loop
        await new Promise(resolve => requestAnimationFrame(resolve));

        let resJSON = {};
        while (autoCompleteRunning) {
            resJSON = await apiRequest("/aiaction", {method: "post"})
            if (resJSON) {
                await updateState(resJSON.lastAction);
                lastAIActionUpdate(resJSON);

                if (resJSON.gameCompleted) {
                    autoCompleteRunning = false;
                    break;
                }
            
                } else if (!resJSON) {
                    autoCompleteRunning = false;
                }
        }

        if (!autoCompleteRunning) {
            UI.loader.style.display = "none";

                    if (!resJSON.gameCompleted) {
                        //Enable buttons if game still in progress
                        toggleButtons(".action-button, .auto-button, .reset-button", true);
                        pressedButton.textContent = "Finish with AI";
                    } else {
                        //Keep all buttons disabled except reset if game is complete
                        toggleButtons(".reset-button", true);
                    }
                } 

    //Same button handles stopping the auto-completion loop prematurely
    } else if (autoCompleteRunning) {
        console.log("Stopping");
        pressedButton.disabled = true;
        pressedButton.textContent = "Stopping AI...";
        autoCompleteRunning = false;
        }
}

export async function resetGame() {
    await apiRequest("/reset", {method: "post"})
    toggleButtons(".action-button, .auto-button", true);
    resetFailCount();
    await updateState();
}
