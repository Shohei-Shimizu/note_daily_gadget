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
                if (cancel) {
                    // SVGや中のアイコンも含めて実際の表示状態を確認
                    const style = window.getComputedStyle(cancel);
                    const isVisible = style.display !== 'none' && style.visibility !== 'hidden' && cancel.offsetWidth > 0 && cancel.offsetHeight > 0;
                    
                    // Stopボタン（四角形アイコン）が表示されているか、送信ボタン（上向き矢印等）が表示されているかで判別
                    // 実際にはCancelボタンと同じコンテナにある別のsend-tooltipと比較する
                    const send = doc.querySelector('[data-tooltip-id="input-send-button-tooltip"]');
                    const sendVisible = send ? (window.getComputedStyle(send).display !== 'none' && send.offsetWidth > 0) : true;
                    
                    return "Cancel Vis: " + isVisible + " Width: " + cancel.offsetWidth + " sendVisible: " + sendVisible + ", class: " + cancel.className;
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
