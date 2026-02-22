const chromeRemoteInterface = require('chrome-remote-interface');
const fs = require('fs');

(async () => {
    let client;
    try {
        const targets = await chromeRemoteInterface.List({ port: 9222 });
        const target = targets.find(t => t.url && (t.url.includes('workbench.html') || t.title.includes('Antigravity') || t.title.includes('Cascade')));
        client = await chromeRemoteInterface({ target: target, port: 9222 });
        const { Page } = client;
        await Page.enable();
        const { data } = await Page.captureScreenshot({ format: 'png' });
        fs.writeFileSync('screenshot_debug.png', Buffer.from(data, 'base64'));
        console.log("Screenshot saved to screenshot_debug.png");
    } catch (e) { console.error(e); } finally { if (client) await client.close(); }
})();
