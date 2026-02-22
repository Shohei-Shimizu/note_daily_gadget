require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
    ]
});

client.once('ready', async () => {
    console.log(`Logged in as ${client.user.tag}!`);
    try {
        // すべてのサーバー（Guild）を取得し、テキストチャンネルを探す
        let sent = false;
        for (const guild of client.guilds.cache.values()) {
            const channels = guild.channels.cache.values();
            for (const channel of channels) {
                if (channel.isTextBased() && channel.permissionsFor(client.user).has('SendMessages')) {
                    await channel.send("🤖 **Antigravityからのお知らせ:**\nこれはBotからの直接送信テストです！この文字がDiscord上で読めていれば、Bot自体の『書き込み権限』と『送信機能』は完璧に動作しています！🌟");
                    console.log(`Successfully sent message to channel: ${channel.name} in guild: ${guild.name}`);
                    sent = true;
                    break;
                }
            }
            if (sent) break;
        }
        if (!sent) {
            console.log("Could not find a suitable text channel to send the message.");
        }
    } catch (error) {
        console.error("Failed to send message:", error);
    } finally {
        client.destroy();
    }
});

client.login(process.env.DISCORD_BOT_TOKEN);
