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

        const expression = `(() => {
            let result = "";
            let texts = [];
            
            // Collect text from main doc
            const mainEls = Array.from(document.querySelectorAll('div'));
            for(const el of mainEls) {
                if(el.innerText && el.innerText.length > 50) {
                     texts.push({ loc: 'main', class: el.className, text: el.innerText.substring(0, 100).replace(/\\n/g, ' ') });
                }
            }

            // Collect text from iframes
            const iframes = document.querySelectorAll('iframe');
            for (let i = 0; i < iframes.length; i++) {
                try {
                    const doc = iframes[i].contentDocument;
                    if (!doc) continue;
                    const iframeEls = Array.from(doc.querySelectorAll('div'));
                    for(const el of iframeEls) {
                        if(el.innerText && el.innerText.length > 50) {
                             texts.push({ loc: 'iframe_' + i, class: el.className, text: el.innerText.substring(0, 100).replace(/\\n/g, ' ') });
                        }
                    }
                } catch(e) {}
            }
            
            // Filter unique texts to avoid explosion
            let unique = [];
            let seen = new Set();
            for(let t of texts) {
                if(!seen.has(t.text)) {
                    seen.add(t.text);
                    unique.push(t);
                }
            }
            
            return JSON.stringify(unique, null, 2);
        })()`;

        const res = await Runtime.evaluate({ expression, returnByValue: true });
        console.log("Result length:", res.result.value ? res.result.value.length : 0);
        console.log(res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
