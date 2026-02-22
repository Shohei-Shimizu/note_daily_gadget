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
                // 返信が期待される "こんにちは" という短いテキスト要素を探す
                const els = Array.from(doc.querySelectorAll('*'));
                for(const el of els) {
                    if(el.children.length === 0 && el.innerText && el.innerText.trim() === 'こんにちは') {
                        // この要素の親要素を遡り、どのような属性（data-message-roleや特定のクラス）を持っているか調べる
                        let container = el.parentElement;
                        let classes = [];
                        for(let i=0; i<10; i++) {
                            if(container) {
                                let tag = container.tagName;
                                let cls = Array.from(container.classList).join('.');
                                let role = container.getAttribute('data-message-role') || '';
                                classes.push(tag + "." + cls + (role ? "[role=" + role + "]" : ""));
                                container = container.parentElement;
                            }
                        }
                        return "Found 'こんにちは'. Ancestors:\\n" + classes.join('\\n');
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
