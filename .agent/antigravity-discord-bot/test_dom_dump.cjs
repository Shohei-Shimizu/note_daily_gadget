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
                if(iframes[i].src.includes('cascade-panel')) {
                    try { if(iframes[i].contentDocument) docs.push(iframes[i].contentDocument); } catch(e){}
                }
            }
            
            for (const doc of docs) {
                // look for "何か返信して" or "こんにちは" or "テスト"
                const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT, null, false);
                let node;
                while (node = walker.nextNode()) {
                    if (node.nodeValue && (node.nodeValue.includes('何か返信して') || node.nodeValue.includes('こんにちは'))) {
                         let container = node.parentElement;
                         let classes = [];
                         for(let i=0; i<8; i++) {
                             if(container) {
                                 let tag = container.tagName;
                                 let cls = Array.from(container.classList).join('.');
                                 let dataRole = container.getAttribute('data-message-role') || '';
                                 classes.push(tag + "." + cls + (dataRole ? "[data-message-role=" + dataRole + "]" : ""));
                                 container = container.parentElement;
                             }
                         }
                         return "Found text node:\\n" + classes.join('\\n');
                    }
                }
            }
            return 'not found';
        })()`;
        
        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("DOM Search:\\n", res.result.value);
    } catch (e) { console.error(e); } finally { if (client) await client.close(); }
})();
