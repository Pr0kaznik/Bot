import discord
from discord.ext import commands

class Cephalon(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Дополнение Cephalon успешно загружено.')

    @commands.command(aliases = ['Info', 'INFO'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def info(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(title = 'Welcome to the cum zone', colour = discord.Color.orange())
        emb.set_author(name = client.user.name, url = 'https://warframe.fandom.com/wiki/Cephalon_Cy', icon_url = client.user.avatar_url)
        emb.add_field(name = 'Версия', value = '0.12.7.8824')
        emb.add_field(name = 'Написан на', value = 'discord.py')
        emb.add_field(name = 'Разработчик', value = 'Написано в футере, ха!')
        emb.add_field(name = 'Веб-сайт', value = '```http://ru-unioncraft.ru/```')
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def aliases(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(description = 'Неочевидные *никнеймы* команд', colour = discord.Color.orange())
        emb.add_field(name = 'invite_cy', value = 'invite, invcy')
        emb.add_field(name = 'rap', value = '.rap')
        emb.add_field(name = 'about', value = 'me')
        emb.add_field(name = 'image', value = 'img&')
        emb.add_field(name = 'emb_edit', value = 'emb_ed')
        emb.add_field(name = 'embed', value = 'emb')
        emb.add_field(name = 'coinflip', value = 'c, coin')
        emb.add_field(name = 'content', value = 'ctx')
        emb.add_field(name = 'А также', value = 'Для остальных команд также есть *никнеймы*, их можно писать с заглавной буквы или полностью капсом')
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
    @commands.command(aliases = ['invite', 'invcy'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def invite_cy(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(description = '[Ссылка](https://discordapp.com/oauth2/authorize?&client_id=694170281270312991&scope=bot&permissions=8) для приглашения Cy на сервера', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
    @commands.command(aliases = ['Ping', 'PING'])
    @commands.cooldown(1, 5, commands.BucketType.default)
    async def ping(self, ctx):
        await ctx.message.delete()
        emb = discord.Embed(description = f'Pong! `{round(client.latency * 1000)} ms`', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
        emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
        await ctx.send(embed = emb)
    
    @commads.command(aliases = ['Join', 'JOIN'])
    async def join(self, ctx):
        await ctx.message.delete()
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        else:
            emb = discord.Embed(description = 'Ты должен быть в канале, чтобы использовать это.', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)
            return
        global vc
        vc = await channel.connect()

    @commands.command(aliases = ['Leave', 'LEAVE'])
    async def leave(self, ctx):
        await ctx.message.delete()
        if vc.is_connected():
            await vc.disconnect()
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.delete()
            emb = discord.Embed(description = f'{ctx.author.mention}, команда в кд, потерпи чутка!', colour = discord.Color.orange())
            emb.set_footer(text = 'Cephalon Cy by сасиска#2472')
            await ctx.send(embed = emb)

def setup(client):
    client.add_cog(Cephalon(client))
