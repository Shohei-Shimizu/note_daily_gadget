const fs = require('fs');
let content = fs.readFileSync('discord_bot.js', 'utf8');

// The regex matches conflict markers
const conflictRegex = /<<<<<<< HEAD\r?\n([\s\S]*?)=======\r?\n([\s\S]*?)>>>>>>> [a-f0-9]+\r?\n/g;

content = content.replace(conflictRegex, (match, blockA, blockB) => {
    // Return both blocks sequentially
    return blockA + blockB;
});

fs.writeFileSync('discord_bot.js', content);
console.log('Conflicts resolved by keeping both.');
