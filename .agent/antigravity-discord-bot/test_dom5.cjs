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
                // "こんにちは" が含まれるテキストノードを探し、その親の構造をすべて返す
                const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT, null, false);
                let node;
                while (node = walker.nextNode()) {
                    if (node.nodeValue && node.nodeValue.includes('こんにちは')) {
                         let container = node.parentElement;
                         let classes = [];
                         for(let i=0; i<15; i++) {
                             if(container) {
                                 let tag = container.tagName;
                                 let cls = Array.from(container.classList).join('.');
                                 classes.push(tag + "." + cls);
                                 container = container.parentElement;
                             }
                         }
                         return "Found text node 'こんにちは'. Ancestors:\\n" + classes.join('\\n');
                    }
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
