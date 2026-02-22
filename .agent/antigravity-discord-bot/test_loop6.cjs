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
                // UI下部の入力ボックス内にあるボタン全体を調べる
                const cancelBtn = doc.querySelector('[data-tooltip-id="input-send-button-cancel-tooltip"]');
                const sendBtn   = doc.querySelector('[data-tooltip-id="input-send-button-tooltip"]') || doc.querySelector('[data-tooltip-id="input-send-button-pending-tooltip"]');
                
                if (cancelBtn && sendBtn) {
                     // 「Stop」の正方形アイコン（Cancel）と、「↑」の上向き矢印（Send / Pending）が含まれる親要素を比較
                     // 実際にはSVGが描画されている方のみ opacity が高いなど、親のクラス構成が変化する
                     return {
                         cancelW: cancelBtn.offsetWidth,
                         cancelH: cancelBtn.offsetHeight,
                         cancelOp: window.getComputedStyle(cancelBtn).opacity,
                         sendW: sendBtn.offsetWidth,
                         sendH: sendBtn.offsetHeight,
                         sendOp: window.getComputedStyle(sendBtn).opacity,
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
