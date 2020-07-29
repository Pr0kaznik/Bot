import asyncio
import random
import datetime
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = commands.when_mentioned_or('cephalon/'))
client.remove_command('help')

#test commands space

#test commands space

@client.command()
async def info(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send(f'Cy в сети, пинг равен `{round(client.latency * 1000)} ms`')
    
@client.command()
@commands.has_permissions(manage_roles = True)
@commands.cooldown(1, 5, commands.BucketType.default)
async def about(ctx, member:discord.Member = None, amount = 1):
    await ctx.channel.purge(limit = amount)
    if member == None:
        member = ctx.message.author
    emb = discord.Embed(title = f'Информация о {member.name}', colour = member.color)
    emb.add_field(name = 'ID', value = member.id)
    emb.add_field(name = 'Создан', value = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
    emb.add_field(name = 'Вошёл', value = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
    emb.add_field(name = 'Упоминание', value = member.mention)
    emb.add_field(name = 'Имя', value = member.name)
    emb.add_field(name = 'Никнейм', value = member.nick)
    emb.add_field(name = 'Статус', value = member.status)
    emb.add_field(name = f'Роли [{len(member.roles)-1}]', value=' '.join([role.mention for role in member.roles[1:]]))
    emb.add_field(name = 'Высшая Роль', value = member.top_role.mention, inline = False)
    emb.add_field(name = 'Бот?', value = member.bot)
    emb.set_thumbnail(url = member.avatar_url)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command()
@commands.has_permissions(administrator = True)
@commands.cooldown(1, 10, commands.BucketType.default)
async def mute(ctx, member: discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = f'Мут от {ctx.author.name}', colour = member.color)
    role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
    await member.add_roles(role)
    emb.add_field(name = 'В муте', value = '{}'.format(member.mention))
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command()
@commands.has_permissions(manage_roles = True)
async def give(ctx, *, arg, member:discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    role = discord.utils.get(ctx.message.guild.roles, name = arg)
    await member.add_roles(role)
    channel = client.get_channel(714175791033876490)
    await channel.send(f'{ctx.author.mention} дал {arg} {member.mention}')
    
@client.command()
@commands.has_permissions(manage_roles = True)
async def take(ctx, *, arg, member:discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    role = discord.utils.get(ctx.message.guild.roles, name = arg)
    await member.remove_roles(role)
    channel = client.get_channel(714175791033876490)
    await channel.send(f'{ctx.author.mention} забрал {arg} у {member.mention}')
    
@client.command()
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1, 5, commands.BucketType.default)
async def image(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.set_image(url = arg)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command()
@commands.has_permissions(mention_everyone = True)
@commands.cooldown(1, 20, commands.BucketType.default)
async def gaystvo_embed(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send('@everyone')
    await asyncio.sleep(0,1)
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.add_field(name = 'Cephalon', value = arg)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command()
@commands.has_permissions(manage_messages = True)
@commands.cooldown(1, 10, commands.BucketType.default)
async def embed(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.add_field(name = 'Cephalon', value = arg)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

@client.command()
@commands.cooldown(1, 20, commands.BucketType.default)
@commands.has_permissions(mention_everyone = True)
async def gaystvo(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send('@everyone ' + arg)
    
@client.command()
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(manage_messages = True)
async def say(ctx, *, arg, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.send(arg)
    
@client.command()
@commands.cooldown(5, 10, commands.BucketType.default)
async def coinflip(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    choices = ['Орёл!', 'Решка!']
    rancoin = random.choice(choices)
    await ctx.send(rancoin)

#получение роли по эмодзи       
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 707496056505761802:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'strashilka':
            role = discord.utils.get(guild.roles, name = 'Пробивший дно')

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 707496056505761802:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'strashilka':
            role = discord.utils.get(guild.roles, name = 'Пробивший дно')

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)        
    
#бесполезное говно
@client.command()
async def join(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
    else:
        await ctx.send("Ты должен быть в канале, чтобы использовать это.")
        return
    global vc
    try:
        vc = await channel.connect()
    except:
        TimeoutError

@client.command()
async def leave(ctx):
    try:
        if vc.is_connected():
            await vc.disconnect()
    except:
        pass

@client.command()
@commands.has_permissions(administrator = True)
@commands.cooldown(1, 10, commands.BucketType.default)
async def pm(ctx, member: discord.Member, amount = 1):
    await ctx.channel.purge(limit = amount)
    await member.send(f'ты кок сакер')

@client.event
async def on_member_join(member):
    channel = client.get_channel(693929823030214658)

    role = discord.utils.get(member.guild.roles, id = 693933516294979704)
    role1 = discord.utils.get(member.guild.roles, id = 693933510523879454)
    role2 = discord.utils.get(member.guild.roles, id = 693933514198089838)

    await member.add_roles(role, role1, role2)
    await channel.send(embed = discord.Embed(description = f'{member.name} Зашёл в комплекс, 👋', colour = discord.Color.orange()))

@client.event
async def on_member_remove(member):
    channel = client.get_channel(693929823030214658)
    await channel.send(embed = discord.Embed(description = f'{member.name} Вышел из комплекса...', colour = discord.Color.red()))
    
#help command
@client.command()
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(manage_messages = True)
async def help(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(title = "Меню команд для администраторов", colour = discord.Color.orange())
    emb.add_field(name = 'Инфо', value = "Cy, или же сай - бот, написанный сасиска")
    emb.add_field(name = '{}info'.format('cephalon/'), value = 'команда для определения, в сети ли бот', inline = False)
    emb.add_field(name = "{}clear".format("cephalon/"), value = "очистка чата")
    emb.add_field(name = "{}ban".format("cephalon/"), value = "бан игрока")
    emb.add_field(name = "{}kick".format("cephalon/"), value = "кик игрока")
    emb.add_field(name = '{}mute'.format('cephalon/'), value = 'мут игрока')
    emb.add_field(name = '{}say'.format('cephalon/'), value = 'пишет сообщение от лица бота. Всё.')
    emb.add_field(name = '{}gaystvo'.format('cephalon/'), value = 'пишет от лица бота и пингует @everyone')
    emb.add_field(name = '{}embed'.format('cephalon/'), value = 'от лица бота отправляется эмбед')
    emb.add_field(name = '{}gaystvo_embed'.format('cephalon/'), value = 'Совмещает в себе команды gaystvo и embed')
    emb.add_field(name = '{}image'.format('cephalon/'), value = 'бот может прикрепить изображение, в аргумент нужно указать ссылку')
    emb.add_field(name = '{}about'.format('cephalon/'), value = 'показывает инфу о человеке.')
    emb.add_field(name = '{}join'.format('cephalon/'), value = 'приказывает зайти боту в голосовой канал')
    emb.add_field(name = '{}leave'.format('cephalon/'), value = 'приказывает боту выйти из голосового канала')
    emb.add_field(name = '{}give'.format('cephalon/'), value = 'выдаёт роль, писать в формате: give (выдаваемая роль) (пинг пользователя)', inline = False)
    emb.add_field(name = '{}take'.format('cephalon/'), value = 'забирает роль, писать в формате: take (забираемая роль) (пинг пользователя)', inline = False)
    emb.add_field(name = 'жыж', value = 'также, для написания команд необязательно писать префикс, можно пингануть ~~@everyone~~ бота')
    emb.add_field(name = 'жопа', value = 'у всех команд есть кд, для команд, пингующих @everyone - 20 секунд, для остальных 10, для about - 5, для coinflip - 5 раз в 10 секунд')
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

@client.command()
async def time(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    emb = discord.Embed(colour = discord.Color.orange())
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472')
    now_date = datetime.datetime.now()
    emb.add_field(name = 'Время по Гринвичу равняется ', value = '{}'.format(now_date))
    await ctx.author.send(embed = emb)

#проверка на подключение
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Game('Discord API'))

#kick
@client.command()
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(kick_members = True)
async def kick(ctx , member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(title = f'Кик от {ctx.author.name}', colour = member.color)
    await member.kick(reason = reason)
    emb.add_field(name = 'Кикнут', value = '{}'.format(member.mention))
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

#ban
@client.command()
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(ban_members = True)
async def ban(ctx , member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(title = f'Бан от {ctx.author.name}', colour = member.color)
    await member.ban(reason = reason)
    emb.add_field(name = 'Забанен', value = '{}'.format(member.mention))
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

#message delete
@client.command()
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount + 1)
    if amount == 1:
        await ctx.send(f'удалено {amount} сообщение')
    elif amount == 2:
        await ctx.send(f'удалено {amount} сообщения')
    elif amount == 3:
        await ctx.send(f'удалено {amount} сообщения')
    elif amount == 4:
        await ctx.send(f'удалено {amount} сообщения')
    else:
        await ctx.send(f'удалено {amount} сообщений')
    await asyncio.sleep(1)
    await ctx.channel.purge(limit = 1)
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{ctx.author.mention}, чё это за команда?')
        
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'{ctx.author.mention}, команда в кд, потерпи чутка!')
    
@image.error
async def image_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, чё прикрепить то?')
        
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать команду image. Хаха')
    
@about.error
async def about_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, о ком инфа то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду about. Хаха')
    
@pm.error
async def pm_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, кому написать то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Pm. Хаха')
        
@gaystvo_embed.error
async def gaystvo_embed_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, чё сказать то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду gaystvo_embed. Хаха')
        
@embed.error
async def embed_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, чё сказать то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Embed. Хаха')

@gaystvo.error
async def gaystvo_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, ты так не шути')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался пингануть \@everyone. Ой')

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, чё сказать то?')
            
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Say. Хаха')
        
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, кого мутить то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Mute. Хаха')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, кого кикать то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{cctx.author.mention} пытался вызвать комманду Kick. Хаха')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, кого банить то?')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Ban. Хаха')

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, нет аргумента!')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'{ctx.author.mention} пытался вызвать комманду Clear. Хаха')
        
    if isinstance(error, commands.BadArgument):
        await ctx.send(f'{ctx.author.mention}, это не число!')
    
t = os.environ.get('t')

client.run(t)
