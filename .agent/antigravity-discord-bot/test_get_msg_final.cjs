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
        
        const expression = `(() => {
            const docs = [document];
            const iframes = document.querySelectorAll('iframe');
            for (let i = 0; i < iframes.length; i++) {
                try { if (iframes[i].contentDocument) docs.push(iframes[i].contentDocument); } catch(e) {}
            }
            
            for (const doc of docs) {
                // Look for the typical message list container
                const messages = Array.from(doc.querySelectorAll('[data-message-role="assistant"], .prose, .markdown-body, div[style*="word-break: break-word"]'));
                if (messages.length > 0) {
                    // Try to filter out system messages or logs if possible, just get the last one
                    const lastMsg = messages[messages.length - 1];
                    const text = lastMsg.innerText || '';
                    if (text.trim().length > 0) {
                        return text;
                    }
                }
            }
            
            // Fallback: look for generic blocks
            for (const doc of docs) {
                const els = Array.from(doc.querySelectorAll('div'));
                const candidates = els.filter(el => {
                    const txt = el.innerText || '';
                    // arbitrary heuristic to find the long reply
                    return txt.includes('私が現在読み込んでいるルール（Rules）の内容は');
                });
                
                if (candidates.length > 0) {
                    // Sort descending by depth/length to find the most specific container
                    const sorted = candidates.sort((a,b) => a.innerText.length - b.innerText.length);
                    return sorted[0].innerText;
                }
            }
            
            return 'Text not found in DOM';
        })()`;
        
        const res = await Runtime.evaluate({ expression, returnByValue: true });
        console.log("Result text length:", res.result.value.length);
        console.log("Result text excerpt:\\n", res.result.value.substring(0, 150));

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
