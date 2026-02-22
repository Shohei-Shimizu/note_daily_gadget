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
        
        // 実際にdiscord_bot.jsで使われているgetLastResponseのロジックをテスト
        const EXP = `(() => {
            const docs = [document];
            const iframes = document.querySelectorAll('iframe');
            for (let i = 0; i < iframes.length; i++) {
                try { if (iframes[i].contentDocument) docs.push(iframes[i].contentDocument); } catch(e) {}
            }
            
            let bestCandidate = null;

            for (const doc of docs) {
                const sels = ['[data-message-role="assistant"]', '.prose', '.markdown-body', '.chat-message.assistant'];
                for (const sel of sels) {
                    const els = Array.from(doc.querySelectorAll(sel));
                    if (els.length > 0) {
                        const txt = els[els.length - 1].innerText;
                        if (txt && txt.trim().length > 0) {
                            bestCandidate = els[els.length - 1];
                            return { foundBy: sel, textLength: txt.length, textPreview: txt.substring(0, 100) };
                        }
                    }
                }
            }

            if (!bestCandidate) {
                for (const doc of docs) {
                    const els = Array.from(doc.querySelectorAll('div, p, span'));
                    const candidates = els.filter(el => {
                        const txt = el.innerText || '';
                        return txt.trim().length > 20 && el.children.length < 5;
                    });
                    
                    if (candidates.length > 0) {
                        bestCandidate = candidates[candidates.length - 1];
                        return { foundBy: 'generic', tagName: bestCandidate.tagName, className: bestCandidate.className, textLength: bestCandidate.innerText.length, textPreview: bestCandidate.innerText.substring(0, 100) };
                    }
                }
            }
            
            return null;
        })()`;
        
        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("GetLastResponse Logic Test:\\n", res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
