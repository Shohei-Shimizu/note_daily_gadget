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
            
            let bestCandidate = null;
            for (const doc of docs) {
                const sels = ['[data-message-role="assistant"]', '.prose', '.markdown-body', '.chat-message.assistant'];
                for (const sel of sels) {
                    const els = Array.from(doc.querySelectorAll(sel));
                    if (els.length > 0) {
                        const txt = els[els.length - 1].innerText;
                        if (txt && txt.trim().length > 0) {
                            return { method: 'sels', textLength: txt.length, content: txt.substring(0, 100) };
                        }
                    }
                }
            }

            for (const doc of docs) {
                const els = Array.from(doc.querySelectorAll('div'));
                const candidates = els.filter(el => {
                    const txt = el.innerText || '';
                    return txt.trim().length > 20 && el.children.length < 5;
                });
                
                if (candidates.length > 0) {
                    const sorted = candidates.sort((a,b) => a.innerText.length - b.innerText.length);
                    const best = sorted[Math.min(sorted.length - 1, 2)];
                    return { method: 'fallback', textLength: best.innerText.length, content: best.innerText.substring(0, 100) };
                }
            }

            return 'not found';
        })()`;
        
        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("GetLastResponse Output:\\n", res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
