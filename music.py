from discord.ext import commands
import lavalink
from discord import utils

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.music = lavalink.Client(self.bot.user.id)
        self.bot.music.add_node('localhost', 7000, 'testing', 'na', 'ZepexNPCMusic')
        self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
        self.bot.music.add_event_hook(self.track_hook)

@commands.command(name='join')
async def join(self, ctx):
    print("Joined Voice Channel")
    member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
    if member is not None and member.voice is not None:
        vc = member.voice.channel
        player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        if not player.is_connected:
            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(vc.id))

@commands.command(name='play')
async def play(self, *, query):
    try:
        player = self.bot.music.player_manager.get(ctx.guild.id)
        query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)
        print(results)
    except Exception as error:
        print(Error)

async def track_hook(self, event):
    if isinstance(event, lavalink.events.QueueEndEvent):
        guild_id = int(event.player.guild_id)
        await self.connect_to(guild_id, None)

def setup(bot):
    bot.add_cog(MusicCog(bot))
