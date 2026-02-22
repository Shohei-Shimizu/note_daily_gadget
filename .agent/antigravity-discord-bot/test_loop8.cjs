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
                     // SVG要素の有無と中身を確認
                     const cancelSvg = cancelBtn.querySelector('svg');
                     const sendSvg = sendBtn.querySelector('svg');
                     
                     // opacityやクラス構成自体に差がないかボタン自身で再確認
                     // よく見ると、一方は opacity-0 などになっているはず
                     // Tailwindクラスを抽出
                     const getOpacity = (el) => {
                         let val = '1';
                         el.classList.forEach(c => {
                             if(c.startsWith('opacity-')) val = c;
                         });
                         return val;
                     };
                     
                     let obj = {
                         cancelOpacityClass: getOpacity(cancelBtn),
                         cancelDisplay: window.getComputedStyle(cancelBtn).display,
                         sendOpacityClass: getOpacity(sendBtn),
                         sendDisplay: window.getComputedStyle(sendBtn).display
                     };

                     // もし本当に同じなら、DOM構造上のSVGの違いを見る
                     if (cancelSvg) obj.cancelHasSvg = true;
                     if (sendSvg) obj.sendHasSvg = true;

                     return obj;
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
