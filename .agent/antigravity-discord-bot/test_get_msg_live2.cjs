const chromeRemoteInterface = require('chrome-remote-interface');

(async () => {
    let client;
    try {
        const targets = await chromeRemoteInterface.List({ port: 9222 });
        const target = targets.find(t => t.url && (t.url.includes('workbench.html') || t.title.includes('Antigravity') || t.title.includes('Cascade')));
        client = await chromeRemoteInterface({ target: target, port: 9222 });
        const { Runtime } = client;
        
        const EXP = `(() => {
            const docs = [document];
            const iframes = document.querySelectorAll('iframe');
            for(let i=0; i<iframes.length; i++) {
                try { if(iframes[i].contentDocument) docs.push(iframes[i].contentDocument); } catch(e){}
            }
            
            let allText = [];
            for (const doc of docs) {
                // look for specific container classes that might hold messages
                const msgContainers = Array.from(doc.querySelectorAll('.chat-message, [data-message-role="assistant"], .prose, .markdown-body, div.flex.flex-col.gap-2.border-gray-500\\\\/25'));
                
                msgContainers.forEach(container => {
                    if (container.innerText && container.innerText.trim().length > 10) {
                         allText.push(container.innerText.trim().substring(0, 50).replace(/\\n/g, ' '));
                    }
                });
            }
            return allText;
        })()`;
        
        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("Message containers found:", res.result.value);
    } catch (e) { console.error(e); } finally { if (client) await client.close(); }
})();
