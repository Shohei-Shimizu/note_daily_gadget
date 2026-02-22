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
            function getTargetDoc() {
                const iframes = document.querySelectorAll('iframe');
                for(let i=0; i<iframes.length; i++) {
                    if(iframes[i].src.includes('cascade-panel')) {
                        try { return iframes[i].contentDocument; } catch(e){}
                    }
                }
                return document; 
            }
            const doc = getTargetDoc();
            if (!doc) return null;

            const approvalKeywords = [
                'run', 'approve', 'allow', 'yes', 'accept', 'confirm', 
                'save', 'apply', 'create', 'update', 'delete', 'remove', 'submit', 'send', 'retry', 'continue',
                'always allow', 'allow once', 'allow this conversation',
                '実行', '許可', '承認', 'はい', '同意', '保存', '適用', '作成', '更新', '削除', '送信', '再試行', '続行'
            ];
            const anchorKeywords = ['cancel', 'reject', 'deny', 'ignore', 'キャンセル', '拒否', '無視', 'いいえ', '不許可'];
            const ignoreKeywords = ['all', 'すべて', '一括', 'auto'];

            let found = [];

            function scan(root) {
                if (!root) return;
                
                const potentialAnchors = Array.from(root.querySelectorAll ? root.querySelectorAll('button, [role="button"], .cursor-pointer') : []).filter(el => {
                    if (el.offsetWidth === 0 || el.offsetHeight === 0) return false;
                    const txt = (el.innerText || '').trim().toLowerCase();
                    return anchorKeywords.some(kw => txt === kw || txt.startsWith(kw + ' '));
                });

                for (const anchor of potentialAnchors) {
                    const container = anchor.closest('.flex') || anchor.parentElement;
                    if (!container) continue;

                    const parent = container.parentElement;
                    if (!parent) continue;

                    const searchScope = parent.parentElement || parent;
                    const buttons = Array.from(searchScope.querySelectorAll('button, [role="button"], .cursor-pointer'));
                    
                    const approvalButton = buttons.find(btn => {
                        if (btn === anchor) return false;
                        if (btn.offsetWidth === 0) return false;
                        
                        const txt = (btn.innerText || '').toLowerCase().trim();
                        const aria = (btn.getAttribute('aria-label') || '').toLowerCase().trim();
                        const title = (btn.getAttribute('title') || '').toLowerCase().trim();
                        const combined = txt + ' ' + aria + ' ' + title;
                        
                        return approvalKeywords.some(kw => combined.includes(kw)) && 
                               !ignoreKeywords.some(kw => combined.includes(kw));
                    });

                    if (approvalButton) {
                        found.push({
                            anchorText: anchor.innerText.trim(),
                            approvalText: approvalButton.innerText.trim(),
                            approvalAria: approvalButton.getAttribute('aria-label') || ''
                        });
                    }
                }

                try {
                    const walker = doc.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, null, false);
                    let n;
                    while (n = walker.nextNode()) {
                        if (n.shadowRoot) scan(n.shadowRoot);
                    }
                } catch(e){}
            }

            scan(doc.body);
            return found;
        })()`;
        
        const res = await Runtime.evaluate({ expression: EXP, returnByValue: true });
        console.log("Approval Logic Test Output:\\n", res.result.value);

    } catch (e) {
        console.error(e);
    } finally {
        if (client) await client.close();
    }
})();
