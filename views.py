import discord
from discord.ext import commands
import logging
import os
logger = logging.getLogger('discord_bot')
class MessageButtonView(discord.ui.View):
    """Vue contenant le bouton d'alerte pour Render"""
    
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="🚨 Attaque Percepteur🚨",
        style=discord.ButtonStyle.danger,
        custom_id="alert_button"
    )
    async def alert_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Bouton pour déclencher une alerte d'attaque percepteur"""
        try:
            # Channel d'alerte configuré via variable d'environnement
            channel_id = int(os.getenv('ALERT_CHANNEL_ID', '1408473953277841570'))
            channel = interaction.client.get_channel(channel_id)
            
            if not channel:
                await interaction.response.send_message(
                    "❌ Channel d'alerte non trouvé! Vérifiez la configuration.",
                    ephemeral=True
                )
                return
            
            # Vérifier que c'est un channel de texte
            if not isinstance(channel, discord.TextChannel):
                await interaction.response.send_message(
                    "❌ Le channel configuré n'est pas un channel de texte!",
                    ephemeral=True
                )
                return
            
            # Message d'alerte avec ping @Niv200
            message_content = f"🚨 **ATTAQUE PERCEPTEUR**\n\n{interaction.user.mention} a déclenché l'alerte ! <@&1342890492463022121> si vous le pouvez venez défendre !"
            
            # Créer l'embed
            embed = discord.Embed(
                description=message_content,
                color=discord.Color.red(),
                timestamp=discord.utils.utcnow()
            )
            embed.set_footer(
                text=f"Alerte déclenchée par {interaction.user.display_name} | Hébergé sur Render",
                icon_url=interaction.user.display_avatar.url
            )
            
            # Envoyer l'alerte
            sent_message = await channel.send(embed=embed)
            
            # Confirmer à l'utilisateur
            success_embed = discord.Embed(
                title="✅ Alerte Envoyée!",
                description=f"**Attaque Percepteur signalée!**\n"
                           f"**Channel:** {channel.mention}\n"
                           f"**Message:** [Voir l'alerte]({sent_message.jump_url})",
                color=discord.Color.green()
            )
            
            await interaction.response.send_message(embed=success_embed, ephemeral=True)
            logger.info(f"Alerte envoyée par {interaction.user} dans {channel.name}")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'alerte: {e}")
            await interaction.response.send_message(
                "❌ Une erreur s'est produite lors de l'envoi de l'alerte.",
                ephemeral=True
            )
