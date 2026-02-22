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
                const cancel = doc.querySelector('[data-tooltip-id="input-send-button-cancel-tooltip"]');
                const send = doc.querySelector('[data-tooltip-id="input-send-button-tooltip"]');
                
                if (cancel && send) {
                    // Sendボタンは display:flex 等で表示され、Cancelボタンは hidden 等になっているか確認する
                    const isCancelHidden = window.getComputedStyle(cancel).display === 'none' || cancel.classList.contains('hidden');
                    const isSendHidden = window.getComputedStyle(send).display === 'none' || send.classList.contains('hidden');
                    
                    // Cancelボタンの親の親（ボタンを囲むラッパー）がhiddenかどうかの判定が有効
                    let cancelWrapperHidden = false;
                    if(cancel.parentElement && cancel.parentElement.parentElement) {
                        cancelWrapperHidden = window.getComputedStyle(cancel.parentElement.parentElement).display === 'none';
                    }
                    
                    return {
                        cancelHidden: isCancelHidden,
                        sendHidden: isSendHidden,
                        cancelWrapperHidden: cancelWrapperHidden,
                        cancelParentDisplay: cancel.parentElement ? window.getComputedStyle(cancel.parentElement).display : 'unknown'
                    };
                }
            }
            return 'not found';
        })()`;
        
        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("Result:\\n", res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
