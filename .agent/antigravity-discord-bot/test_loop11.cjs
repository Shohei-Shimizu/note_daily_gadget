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
                        if (txt && txt.trim().length > 10) {
                            return { match: 'sels', textLength: txt.length, content: txt.substring(0, 100).replace(/\n/g, ' ') };
                        }
                    }
                }
            }

            for (const doc of docs) {
                const els = Array.from(doc.querySelectorAll('div, p, span'));
                const candidates = els.filter(el => {
                    const txt = el.innerText || '';
                    return txt.trim().length > 50 && el.children.length < 10;
                });
                
                if (candidates.length > 0) {
                    const bestCandidate = candidates[candidates.length - 1];
                    let finalTxt = bestCandidate.innerText.trim();
                    if (finalTxt.length < 30 && (finalTxt.includes('Gemini') || finalTxt.includes('Claude') || finalTxt.includes('GPT') || finalTxt.includes('Model'))) {
                        return null;
                    }
                    const lines = finalTxt.split('\\n');
                    const cleanLines = lines.filter(l => !l.startsWith('Injecting message') && !l.startsWith('[INJECT]') && !l.includes('Context: '));
                    finalTxt = cleanLines.join('\\n').trim();

                    return { match: 'fallback', textLength: finalTxt.length, content: finalTxt.substring(0, 100).replace(/\n/g, ' ') };
                }
            }

            return 'not found';
        })()`;

        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("Final Logic Test Output:\\n", res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
