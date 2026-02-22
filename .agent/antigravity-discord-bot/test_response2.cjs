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
            
            // ユーザー名をヒントにして、チャット履歴の中から回答らしい部分を探す
            for (const doc of docs) {
                const els = Array.from(doc.querySelectorAll('div'));
                const candidates = els.filter(el => {
                    const txt = el.innerText || '';
                    // ユーザーの入力（こんにちは等）のすぐ下にある長いテキストを探す
                    return txt.includes('こんにちは') && txt.length > 50;
                });
                
                if (candidates.length > 0) {
                    const deepest = candidates.sort((a,b) => a.innerText.length - b.innerText.length)[0];
                    return { foundBy: 'heuristic', tagName: deepest.tagName, className: deepest.className, textLength: deepest.innerText.length, textPreview: deepest.innerText.substring(0, 150) };
                }
            }
            return null;
        })()`;
        
        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("Heuristic Test:\\n", res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
