import { apiRequest } from "./api.js";

//DOM into UI object
export const UI = {
    manualRepeatsField: document.getElementById("manualRepeats"),
    manualSpeedField: document.getElementById("manualSpeed"),
    progressBar: document.getElementById("progressBar"),
    heatBar: document.getElementById("heatBar"),
    loader: document.getElementById("loader"),
    errorSpan: document.getElementById("errorSpan"),
    actionMessage : document.getElementById("actionMessage")
};

//Max values for UI elements
let maxValues = {
    progress : 0,
    heat : 0,
    failCount : 0
}

//Fetch initial values inside the game, update the DOM accordingly and store them for later use
export function setupInitialValues(initialValues) {
    console.log("starting initial")
    for (const [key, value] of Object.entries(initialValues)) {
        const el = document.getElementById(key);
        el.innerText = value;

        maxValues[key.replace(/Max$/, "")] = value;
    }

    progressBar.setAttribute("aria-valuemax", `${maxValues.progress}`);
    heatBar.setAttribute("aria-valuemax", `${maxValues.heat}`);
}

//Updates fields with player's progress on the game
//If an action name is provided, display it in the actionMessage field
let prevFailCount = 0;
export async function updateState(action) {
    const state = await apiRequest("/state", {})

    let actionFlair = "";

    if (state.progress >= maxValues.progress) {
        actionFlair = "VICTORY";
        toggleButtons(".action-button, .auto-button", false);

    } else if (state.failCount >= maxValues.failCount) {
        actionFlair = "LOSS";
        toggleButtons(".action-button, .auto-button", false);

    } else {
        if (prevFailCount < Number(state.failCount)) {
            actionFlair = "FAIL";
        } else if (["hammer", "grind", "polish"].includes(action)) {
            actionFlair = "SUCCESS";
        } else {
            actionFlair = "";
        }

    }

    prevFailCount = Number(state.failCount);
    updateElements(state, actionFlair);
}

export function resetFailCount() {
    prevFailCount = 0;
}


//Update DOM elements with fetched state
function updateElements(data, actionFlair) {
    for (const [key, value] of Object.entries(data)) {
        const el = document.getElementById(key);
        el.innerText = value;
    }

    UI.progressBar.setAttribute("aria-valuenow", `${data.progress}`);
    UI.heatBar.setAttribute("aria-valuenow", `${data.heat}`);
    
    const heatPercent = Math.ceil((Number(data.heat) * 100) / maxValues.heat)
    UI.heatBar.setAttribute("style", `width:${heatPercent}%`);
    const progressPercent = Math.ceil((Number(data.progress) * 100) / maxValues.progress)
    UI.progressBar.setAttribute("style", `width:${progressPercent}%`);

    UI.actionMessage.innerText = actionFlair;
}

//Update the AI action info panel
export function lastAIActionUpdate(data) {
    for (const [key, value] of Object.entries(data)) {
        const el = document.getElementById(key);
        if (!el) continue;
        el.innerText = value;}
}

export function toggleButtons(buttons, isEnabled, optionalButton = null) {
    const allButtons = document.querySelectorAll(buttons);
    allButtons.forEach(btn => btn.disabled = !isEnabled);

    if (optionalButton) {
        optionalButton.disabled = !isEnabled;
    }
}