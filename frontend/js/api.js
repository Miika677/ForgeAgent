import { UI } from "./ui.js"
import { API_BASE, ERROR_MESSAGES } from "./config.js";

export async function apiRequest(endpoint, options = {}) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, options);

        if (!res.ok) {
            UI.errorSpan.innerText = ERROR_MESSAGES.http;
            return null;
        }

        //Catch if JSON is empty (e.g. reset game button POST)
        try {
            return await res.json();
        } catch {
            console.log("catch success")
            return null;
        }

    } catch (err) {
        UI.errorSpan.innerText = ERROR_MESSAGES.network;
        console.error(err);
        return null;
    }
}