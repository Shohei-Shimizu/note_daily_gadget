const chromeRemoteInterface = require('chrome-remote-interface');

(async () => {
    let client;
    try {
        const targets = await chromeRemoteInterface.List({ port: 9222 });
        const target = targets.find(t => t.url && (t.url.includes('workbench.html') || t.title.includes('Antigravity') || t.title.includes('Cascade')));
        if (!target) {
            console.log("No suitable target found");
            return;
        }
        client = await chromeRemoteInterface({ target: target, port: 9222 });
        const { Runtime } = client;
        
        const EXP = `(() => {
            const docs = [document];
            const iframes = document.querySelectorAll('iframe');
            for (let i = 0; i < iframes.length; i++) {
                try { if (iframes[i].contentDocument) docs.push(iframes[i].contentDocument); } catch(e) {}
            }
            
            let results = [];
            for (const doc of docs) {
                const els = Array.from(doc.querySelectorAll('[data-message-role="assistant"], .prose, .markdown-body, .chat-message.assistant'));
                els.forEach(el => {
                    results.push(el.innerText);
                });
                
                if (results.length === 0) {
                     // try fallback
                     const allEls = Array.from(doc.querySelectorAll('div, p, span'));
                     const candidates = allEls.filter(el => {
                         const txt = el.innerText || '';
                         if (txt.trim().length === 0) return false;
                         if (typeof el.className === 'string' && el.className.includes('monaco')) return false;
                         if (el.querySelector('style') || el.tagName.toLowerCase() === 'style') return false;
                         return el.children.length < 10;
                     });
                     if (candidates.length > 0) {
                         results.push("FALLBACK CANDIDATE: " + candidates[candidates.length - 1].innerText);
                     }
                }
            }
            return results;
        })()`;
        
        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("getLastResponse simulation results:", res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
