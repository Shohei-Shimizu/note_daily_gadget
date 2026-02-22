const chromeRemoteInterface = require('chrome-remote-interface');

(async () => {
    let client;
    try {
        const targets = await chromeRemoteInterface.List({ port: 9222 });
        const target = targets.find(t => t.url && (t.url.includes('workbench.html') || t.title.includes('Antigravity') || t.title.includes('Cascade')));
        client = await chromeRemoteInterface({ target: target, port: 9222 });
        const { Runtime, Input } = client;
        
        const FOCUS_EXP = `(() => {
            const doc = document;
            const editors = Array.from(doc.querySelectorAll('div[role="textbox"] [contenteditable="plaintext-only"], div[role="textbox"]:not(.xterm-helper-textarea)'));
            const valid = editors.filter(e => e.offsetParent !== null);
            if(valid.length > 0) {
                valid[valid.length - 1].focus();
                return "Focused";
            }
            return "Not found";
        })()`;
        
        const res = await Runtime.evaluate({ expression: FOCUS_EXP, returnByValue: true });
        console.log("Focus:", res.result.value);
        
        if (res.result.value === "Focused") {
            console.log("Typing 'こんにちは'...");
            for (const char of "こんにちは") {
                await Input.dispatchKeyEvent({ type: 'char', text: char });
                await new Promise(r => setTimeout(r, 50));
            }
            
            console.log("Waiting 500ms then pressing Enter...");
            await new Promise(r => setTimeout(r, 500));
            await Input.dispatchKeyEvent({ type: 'keyDown', key: 'Enter', code: 'Enter', text: '\r' });
            await Input.dispatchKeyEvent({ type: 'keyUp', key: 'Enter', code: 'Enter' });
            
            console.log("Done typing");
        }
    } catch (e) { console.error(e); } finally { if (client) await client.close(); }
})();
