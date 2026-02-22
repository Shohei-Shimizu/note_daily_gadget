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
                     // SVGの有無で判定
                     const cancelSvg = cancelBtn.querySelector('svg');
                     if (cancelSvg) {
                         // さらに、SVGが実際に表示されているか親要素のopacityも見るのがより安全
                         // DOMの中にSVGがある＝Cancelボタンが表示されている＝生成中
                         return true;
                     } else {
                         return false; 
                     }
                }
            }
            return false;
        })()`;
        
        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("IsGenerating Result:\\n", res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
