const chromeRemoteInterface = require('chrome-remote-interface');

(async () => {
    let client;
    try {
        const targets = await chromeRemoteInterface.List({ port: 9222 });
        const target = targets.find(t => t.url && t.url.includes('workbench.html'));
        if (!target) {
            console.log("No workbench.html target found");
            return;
        }
        client = await chromeRemoteInterface({ target: target, port: 9222 });
        const { Runtime } = client;
        
        const EXP = `(() => {
            const docs = [document];
            const iframes = document.querySelectorAll('iframe');
            for(let i=0; i<iframes.length; i++) {
                if(iframes[i].src.includes('cascade-panel')) {
                    try { if(iframes[i].contentDocument) docs.push(iframes[i].contentDocument); } catch(e){}
                }
            }
            
            let found = [];
            for (const doc of docs) {
                const cancel = doc.querySelector('[data-tooltip-id="input-send-button-cancel-tooltip"]');
                if (cancel) {
                    found.push("Cancel found, offsetParent: " + (cancel.offsetParent !== null));
                }
                 
                const buttons = Array.from(doc.querySelectorAll('button'));
                for (const btn of buttons) {
                    const txt = (btn.innerText || '').trim().toLowerCase();
                    if ((txt === 'stop' || txt === '停止')) {
                        found.push("Stop found, offsetParent: " + (btn.offsetParent !== null));
                    }
                }
            }
            return found.join('\\n');
        })()`;
        
        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("Found buttons:\\n", res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
