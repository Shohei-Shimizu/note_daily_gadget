const fs = require('fs');
let content = fs.readFileSync('discord_bot.js', 'utf8');
const conflictRegex = /<<<<<<< (HEAD|ours)\r?\n([\s\S]*?)=======\r?\n([\s\S]*?)>>>>>>> (theirs|[a-f0-9]+)\r?\n/g;
content = content.replace(conflictRegex, (match, m1, blockA, blockB) => blockA + blockB);
// Fix the unclosed template string caused by keeping both in injectMessage
content = content.replace(/return \{ ok: true, method: "focus" \};\r?\n    const safeText = JSON.stringify\(text\);/,
    'return { ok: true, method: "focus" };\n    })();`\n    const safeText = JSON.stringify(text);');
fs.writeFileSync('discord_bot.js', content);
console.log('Conflicts resolved by keeping both.');
