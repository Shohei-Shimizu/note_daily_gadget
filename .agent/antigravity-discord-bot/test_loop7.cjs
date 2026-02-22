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
                     // 親要素のクラスや、含まれるSVGの違いを探す
                     // 実際には、現在表示されている方の親要素が opacity-100 になり、隠れている方が opacity-0 や pointer-events-none になっているはず
                     // これを親をたどっていって確認する
                     let curC = cancelBtn.parentElement;
                     let cancelClasses = [];
                     while(curC && curC.tagName !== 'DIV') { cancelClasses.push(curC.className); curC = curC.parentElement; }
                     if(curC) cancelClasses.push(curC.className);

                     let curS = sendBtn.parentElement;
                     let sendClasses = [];
                     while(curS && curS.tagName !== 'DIV') { sendClasses.push(curS.className); curS = curS.parentElement; }
                     if(curS) sendClasses.push(curS.className);

                     return {
                         cancelWrapperClasses: cancelClasses.join(' | '),
                         sendWrapperClasses: sendClasses.join(' | ')
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
