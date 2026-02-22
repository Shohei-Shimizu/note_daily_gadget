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
        
        // 実際にdiscord_bot.jsで使われている checkIsGenerating のロジックをテスト
        const EXP = `(() => {
            function getTargetDoc() {
                const iframes = document.querySelectorAll('iframe');
                for (let i = 0; i < iframes.length; i++) {
                    if (iframes[i].src.includes('cascade-panel')) {
                        try { return iframes[i].contentDocument; } catch(e) {}
                    }
                }
                return document;
            }
            const doc = getTargetDoc();
            const cancel = doc.querySelector('[data-tooltip-id="input-send-button-cancel-tooltip"]');
            if (cancel && cancel.offsetParent !== null) return true;
            
            // キャンセルボタンが見つからない場合、Stopボタンがないか探す
            const buttons = doc.querySelectorAll('button');
            for (const btn of buttons) {
                const txt = (btn.innerText || '').trim().toLowerCase();
                if (txt === 'stop' || txt === '停止') {
                    if (btn.offsetParent !== null) return true;
                }
            }
            return false;
        })()`;
        
        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("Is Generating?:", res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
