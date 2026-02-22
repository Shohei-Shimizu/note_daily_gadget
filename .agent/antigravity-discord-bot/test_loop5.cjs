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
                const tooltips = Array.from(doc.querySelectorAll('[data-tooltip-id]'));
                const matched = tooltips.filter(el => el.getAttribute('data-tooltip-id').includes('input-send-button'));

                if(matched.length > 0) {
                    let result = [];
                    for(const el of matched) {
                        const style = window.getComputedStyle(el);
                        // 要素が非表示になっていないか（クラスにhiddenがないか、display:noneではないか、サイズがあるか）
                        const isVisible = style.display !== 'none' && el.offsetWidth > 0;
                        const parentStyle = el.parentElement ? window.getComputedStyle(el.parentElement).display : 'unknown';
                        result.push({
                            id: el.getAttribute('data-tooltip-id'),
                            isVisible: isVisible,
                            display: style.display,
                            parentDisplay: parentStyle
                        });
                    }
                    return result;
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
