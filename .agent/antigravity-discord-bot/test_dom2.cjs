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
                // "何か簡単な返信ください！" と書かれたユーザー投稿を探す
                const els = Array.from(doc.querySelectorAll('*'));
                let userMsgEl = null;
                for(const el of els) {
                    if(el.children.length === 0 && el.innerText && el.innerText.includes('何か簡単な返信ください！')) {
                        userMsgEl = el;
                    }
                }
                
                if (userMsgEl) {
                    // その要素から一番近いメッセージコンテナを探す
                    let container = userMsgEl.parentElement;
                    let classes = [];
                    for(let i=0; i<10; i++) {
                        if(container) {
                            classes.push(container.tagName + "." + Array.from(container.classList).join('.'));
                            container = container.parentElement;
                        }
                    }
                    
                    // さらに、そこから少し後ろ（DOM上）にあるAIの返答要素を探す
                    return "User Msg Container Ancestors:\\n" + classes.join('\\n');
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
