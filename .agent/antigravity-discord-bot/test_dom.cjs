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
            
            for (const doc of docs) {
                // "こんにちは" または "何か簡単な返信ください！" へのAIの返答を探す
                // <div> や <p> の中身を見る
                const els = Array.from(doc.querySelectorAll('*'));
                let answers = [];
                for(const el of els) {
                    if(el.children.length === 0 && el.innerText && (el.innerText.includes('こんにちは') || el.innerText.includes('何か簡単な'))) {
                        answers.push(el.className || el.tagName);
                    }
                }
                
                // もう少し広めに親要素のクラスも取得
                return answers.slice(-10).join('\\n');
            }
            return 'not found';
        })()`;
        
        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("DOM Search:\\n", res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
