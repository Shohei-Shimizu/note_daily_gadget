const chromeRemoteInterface = require('chrome-remote-interface');

(async () => {
    let client;
    try {
        const targets = await chromeRemoteInterface.List({ port: 9222 });
        // find a webview or iframe target (cascade-panel or similar)
        // or just workbench
        const target = targets.find(t => t.url && t.url.includes('workbench.html'));
        if (!target) {
            console.log("No workbench.html target found");
            return;
        }
        client = await chromeRemoteInterface({ target: target, port: 9222 });
        const { Runtime } = client;

        const expression = `(() => {
            let html = [];
            const iframes = document.querySelectorAll('iframe');
            for (let i = 0; i < iframes.length; i++) {
                if (iframes[i].src.includes('cascade-panel')) {
                    try {
                        const doc = iframes[i].contentDocument;
                        // let's grab the HTML of the entire body to parse it locally
                        const els = doc.querySelectorAll('div, li, p');
                        const classes = Array.from(els).map(e => e.className).filter(c => typeof c === 'string' && c.length > 0);
                        html.push([...new Set(classes)].join('\\n'));
                    } catch(e) {}
                }
            }
            return html.join('\\n---IFRAME---\\n');
        })()`;

        const res = await Runtime.evaluate({ expression, returnByValue: true });
        console.log("Classes found:\\n", res.result.value);

        // Let's also try to find elements with markdown rendering
        const exp2 = `(() => {
            const iframes = document.querySelectorAll('iframe');
            for (let i = 0; i < iframes.length; i++) {
                if (iframes[i].src.includes('cascade-panel')) {
                    try {
                        const doc = iframes[i].contentDocument;
                        // look for markdown wrappers
                        const items = doc.querySelectorAll('.markdown-body, .prose, [data-message-role], div[style*="whitespace-pre-wrap"]');
                        return Array.from(items).map(e => e.className + " | textLength: " + e.innerText.length).join('\\n');
                    } catch(e) {}
                }
            }
            return 'not found';
        })()`;
        const res2 = await Runtime.evaluate({ expression: exp2, returnByValue: true });
        console.log("Markdown containers:\\n", res2.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
