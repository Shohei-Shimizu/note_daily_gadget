const fs = require('fs');
let code = fs.readFileSync('discord_bot.js', 'utf8');
const regex = /<<<<<<< (ours|HEAD)\r?\n([\s\S]*?)=======\r?\n([\s\S]*?)>>>>>>> (theirs|[a-f0-9]+)\r?\n/g;
code = code.replace(regex, (match, m1, A, B, m4) => {
    // Escape backticks and template expressions so they don't break the enclosing template literal (if any)
    const safeB = B.replace(/`/g, '\\`').replace(/\$\{/g, '\\${').replace(/\*\//g, '* /');
    return A + '\n/* ====== THEIRS (CONFLICT) ======\n' + safeB + '\n================================ */\n';
});
fs.writeFileSync('discord_bot.js', code);
console.log('Safely resolved conflicts by commenting out the remote branch changes and escaping backticks.');
