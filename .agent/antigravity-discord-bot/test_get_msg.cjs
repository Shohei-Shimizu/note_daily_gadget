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
            const iframes = document.querySelectorAll('iframe');
            for (let i = 0; i < iframes.length; i++) {
                if (iframes[i].src.includes('cascade-panel')) {
                    try {
                        const doc = iframes[i].contentDocument;
                        
                        // Let's find exactly the message text
                        const allEls = Array.from(doc.querySelectorAll('*'));
                        const els = allEls.filter(el => el.innerText && el.innerText.includes('私が現在読み込んでいるルール'));
                        
                        if (els.length > 0) {
                            // The last one is the deepest (most specific) element containing that text
                            const deepest = els[els.length - 1];
                            
                            // Let's go up the DOM tree and record classes
                            let path = [];
                            let curr = deepest;
                            for(let j=0; j<10 && curr && curr.tagName; j++) {
                                let sel = curr.tagName.toLowerCase();
                                if(curr.className && typeof curr.className === 'string') {
                                    sel += '.' + curr.className.split(' ').join('.').trim();
                                }
                                path.unshift(sel);
                                curr = curr.parentElement;
                            }
                            return 'Found element tree:\\n' + path.join('\\n > ');
                        }
                    } catch(e) {}
                }
            }
            return 'Text not found in DOM';
        })()`;

        const res = await Runtime.evaluate({ expression, returnByValue: true });
        console.log("Result:\\n", res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
