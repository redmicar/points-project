import discord
from discord.ext import commands
from discord import app_commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot setup
bot = commands.Bot(command_prefix="/", intents=intents)

# Storing points in memory (can be replaced with a database like SQLite later)
user_points = {}

# Emojis
point_emoji = "💎"
success_emoji = "✅"
error_emoji = "❌"

# Function to send messages inside an Embed
async def send_embed(interaction: discord.Interaction, title, description, color=discord.Color.blue()):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)  # using interaction.user
    await interaction.response.send_message(embed=embed)

# /give command to distribute points (admin only)
@bot.tree.command(name="give", description="Give points to a specific user")
@app_commands.describe(user="The user you want to give points to", points="The number of points")
async def give_points(interaction: discord.Interaction, user: discord.Member, points: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You do not have administrator permissions to perform this action.", ephemeral=True)
        return
    
    if user.id not in user_points:
        user_points[user.id] = 0
    user_points[user.id] += points
    await send_embed(interaction, "**Points Added** ", f"<:arrow_gx:1239184074992779296> **{points}** points have been added to ||{user.mention}|| 🎉", color=discord.Color.green())

# /remove command to remove points
@bot.tree.command(name="remove", description="Remove points from a specific user")
@app_commands.describe(user="The user you want to remove points from", points="The number of points")
async def remove_points(interaction: discord.Interaction, user: discord.Member, points: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You do not have administrator permissions to perform this action.", ephemeral=True)
        return

    if user.id not in user_points or user_points[user.id] < points:
        await interaction.response.send_message(f"<:arrow_gx:1239184074992779296> {user.mention} does not have enough points <:circle:1238429329231314974>", ephemeral=True)
        return
    
    user_points[user.id] -= points
    await send_embed(interaction, "Points Removed!", f"<:arrow_gx:1239184074992779296> **{points}** points have been removed from {user.mention} <:circle:1238429329231314974>", color=discord.Color.red())

# /points command to check the user's points
@bot.tree.command(name="points", description="Check your current points")
async def check_points(interaction: discord.Interaction):
    points = user_points.get(interaction.user.id, 0)
    await send_embed(interaction, "Your Current Points", f"<:arrow_gx:1239184074992779296> You have {points} points currently <:circle:1238429329231314974>", color=discord.Color.purple())

# /rules command to display the points rules
@bot.tree.command(name="rules", description="Display the points rules")
async def rules(interaction: discord.Interaction):
    rules_text = """
    **Points Rules <:alert:1254763946343137300>**
    <:circle:1238429329231314974> Only administrators can use the add and remove points commands.
    <:circle:1238429329231314974> Points are used as rewards and can be granted or deducted based on activity.
    <:circle:1238429329231314974> Each person can only see their own points.
    """
    await send_embed(interaction, "Points Rules", rules_text, color=discord.Color.orange())

# /point-tlist command to display points of all members in the server
@bot.tree.command(name="point-list", description="Display points of all members in the server")
async def point_tlist(interaction: discord.Interaction):
    members_points = []

    # Retrieve points for each member in the server
    for member in interaction.guild.members:
        if member.id in user_points:
            points = user_points[member.id]
            if points > 0:
                members_points.append(f"{member.mention}: **{points} <:credits:1238429509795971116>**")
            else:
                members_points.append(f"")  # If they have no points, just show the mention
  # If they have no points, just show the mention

    # If the list is empty
    if not members_points:
        await interaction.response.send_message("❌ No one has points in the server.", ephemeral=True)
        return

    # Split the list if it's too long (to comply with the 2048 character limit for messages)
    members_points_text = "\n".join(members_points)
    if len(members_points_text) > 2048:
        members_points_text = members_points_text[:2045] + "..."

    # Send the points list in an Embed
    await send_embed(interaction, "Server Members' Points", members_points_text, color=discord.Color.blue())

# Sync commands with Discord
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}!")


# تشغيل البوت
bot.run("حظ التوكن هنا")
