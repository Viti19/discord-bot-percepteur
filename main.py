import discord
from discord.ext import commands
import os
from flask import Flask
import threading
import asyncio
import logging
from views import MessageButtonView
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('discord_bot')
# Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
ALERT_CHANNEL_ID = int(os.getenv('ALERT_CHANNEL_ID', '1408473953277841570'))
# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
# Flask app for Render health check
app = Flask(__name__)
@app.route('/')
def home():
    return "🚨 Alerte Percepteur Bot is running on Render! 🚨"
@app.route('/health')
def health():
    return {"status": "online", "bot": "Alerte Percepteur"}
def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
# Discord bot events
@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')
    
    # Add persistent view
    bot.add_view(MessageButtonView())
    
    # Sync commands
    try:
        synced = await bot.tree.sync()
        logger.info(f'Synced {len(synced)} command(s)')
    except Exception as e:
        logger.error(f'Failed to sync commands: {e}')
@bot.tree.command(name="ping", description="Test du bot")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("🚨 Alerte Percepteur is online on Render! 🚨", ephemeral=True)
@bot.tree.command(name="hello", description="Dire bonjour")
async def hello_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"👋 Salut {interaction.user.mention} ! Je suis prêt pour les alertes !", ephemeral=True)
@bot.tree.command(name="buttons", description="Affiche les boutons d'alerte")
async def buttons_slash(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🚨 Centre de Contrôle - Alerte Percepteur",
        description="Cliquez sur le bouton ci-dessous pour déclencher une alerte d'attaque percepteur",
        color=discord.Color.red()
    )
    embed.add_field(
        name="🎯 Fonction",
        value="• **Attaque Percepteur** : Alerte immédiate avec ping @Niv200",
        inline=False
    )
    embed.set_footer(text="Bot hébergé sur Render.com | Alerte Percepteur")
    
    view = MessageButtonView()
    await interaction.response.send_message(embed=embed, view=view)
if __name__ == '__main__':
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN environment variable is required!")
        exit(1)
    
    # Start Flask server in background
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("Flask server started for Render health checks")
    
    # Start Discord bot
    logger.info("Starting Discord bot...")
    bot.run(DISCORD_TOKEN)
