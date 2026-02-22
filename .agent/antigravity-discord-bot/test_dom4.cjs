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
                // "[data-message-role="assistant"]" 要素の中身をすべて確認する
                const assistants = Array.from(doc.querySelectorAll('[data-message-role="assistant"]'));
                if (assistants.length > 0) {
                     const texts = assistants.map(el => {
                         let t = (el.innerText || '').trim();
                         // 長すぎる場合は省略
                         if (t.length > 100) t = t.substring(0, 100) + '...';
                         return t;
                     });
                     return "Found Assistant Role:\\n" + texts.join('\\n-----\\n');
                }
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
