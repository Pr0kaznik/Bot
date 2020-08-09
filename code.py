import youtube_dl
import asyncio
import random
import datetime
import os
import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = commands.when_mentioned_or('cy/'))
client.remove_command('help')
client.owner_id = 338714886001524737

#test commands space

#test commands space

@client.command(aliases = ['Info', 'INFO'])
async def info(ctx):
    await ctx.channel.purge(limit = 1)
    await ctx.send(f'Cy в сети, пинг равен `{round(client.latency * 1000)} ms`')
    
@client.command()
@commands.cooldown(5, 5, commands.BucketType.default)
async def remind(ctx, arg, time:int, *):
	await ctx.channel.purge(limit = 1)
    emb = discord.Embed(title = None, colour = ctx.author.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'Напомню через', value = f'{time} минут(у, ы)')
    emb.add_field(name = 'О чём напомню?', value = arg)
    emb.add_field(name = 'Кому?', value = ctx.author.mention)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    await asyncio.sleep(time*60)
    await ctx.send(f'{ctx.author.mention}')
    emb = discord.Embed(title = 'Напоминание', colour = ctx.author.color)
    emb.add_field(name = 'Напомнил через', value = f'{time} минут(у, ы)')
    emb.add_field(name = 'Напоминаю о', value = arg)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb) 
   
@client.command(aliases = ['Guild', 'GUILD'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def guild(ctx, guild : discord.Guild = None):
    guild = ctx.guild if not guild else guild
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(titile = f'Информация о {guild}', colour = discord.Color.orange(), timestamp = ctx.message.created_at)
    emb.add_field(name = 'ID сервера', value = guild.id)
    emb.add_field(name = 'Уровень сервера', value = guild.premium_tier)
    emb.add_field(name = 'Люди, бустящие сервер', value = guild.premium_subscribers)
    emb.add_field(name = 'Владелец сервера', value = guild.owner.mention, inline = False)
    emb.add_field(name = 'Количество человек на сервере', value = guild.member_count)
    emb.add_field(name = 'Дата создания сервера', value = guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
    emb.set_thumbnail(url = guild.icon_url)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['.rap'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def rap(ctx):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(colour = ctx.author.color, timestamp = ctx.message.created_at)
    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.set_image(url = 'https://thumbs.gfycat.com/MessyCarefreeHousefly-size_restricted.gif')
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['me', 'Me', 'ME', 'About', 'ABOUT'])
@commands.cooldown(1, 5, commands.BucketType.default)
async def about(ctx, member:discord.Member = None):
    await ctx.channel.purge(limit = 1)
    if member == None:
        member = ctx.message.author
    emb = discord.Embed(title = f'Информация о {member.name}', colour = member.color, timestamp = ctx.message.created_at)
    emb.add_field(name = 'ID', value = member.id)
    emb.add_field(name = 'Создан', value = member.created_at.strftime("%A, %#d %B %Y, %I:%M %p UTC"), inline = False)
    emb.add_field(name = 'Вошёл', value = member.joined_at.strftime("%A, %#d %B %Y, %I:%M %p UTC"), inline = False)
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
    
@client.command(aliases = ['Unmute', 'UNMUTE'])
@commands.has_permissions(manage_channels = True)
async def unmute(ctx, member : discord.Member):
    await ctx.channel.purge(limit = 1)
    role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
    if role is not None:
        await member.remove_roles(role)
        emb = discord.Embed(title = f'Принудительное снятие мута у {member.name}', colour = member.color, timestamp = ctx.message.created_at)
        emb.add_field(name = 'Снял мут', value = ctx.author.mention)
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
    else:
        await ctx.send(f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль Muted была удалена/отредактирована!')
        
    
@client.command(aliases = ['Mute', 'MUTE'])
@commands.has_permissions(manage_channels = True)
@commands.cooldown(1, 10, commands.BucketType.default)
async def mute(ctx, member: discord.Member, time : int):
    await ctx.channel.purge(limit = 1)
    if member.id != client.owner_id:
        role = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
        if role is not None:
            await member.add_roles(role)
            emb = discord.Embed(title = f'Мут от {ctx.author.name}', colour = member.color, timestamp = ctx.message.created_at)
            emb.add_field(name = 'В муте', value = f'{member.mention}')
            emb.add_field(name = 'Время мута в минутах', value = time)
            emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
            await ctx.send(embed = emb)
            await asyncio.sleep(time*60)
            mrole = discord.utils.get(ctx.message.guild.roles, name = 'Muted')
            if mrole is not None:
                await ctx.send(f'{member.mention}')
                emb = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)
                emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                emb.add_field(name = 'Время мута в минутах составляло', value = time)
                emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
                await ctx.send(embed = emb)
                await member.remove_roles(mrole)
            else:
                await ctx.send(f'{ctx.author.mention}, Я не могу снять мут у {member.mention} из-за того, что роль Muted была удалена/отредактирована!')
        else:
            await ctx.send(f'{ctx.author.mention}, Я не смог найти подходящую для этой команды роль. Роль должна называться Muted')
    else:
        await ctx.send(f'Извините, {ctx.author.mention}, но вы не можете замутить моего создателя!')
        
@client.command(aliases = ['Give', 'GIVE'])
@commands.has_permissions(manage_channels = True)
async def give(ctx, arg, member: discord.Member):
    await ctx.channel.purge(limit = 1)
    role = discord.utils.get(ctx.message.guild.roles, name = arg)
    await member.add_roles(role)
    channel = client.get_channel(714175791033876490)
    await channel.send(f'{ctx.author.mention} дал @{role} {member.mention}')
    
@client.command(aliases = ['Take', 'TAKE'])
@commands.has_permissions(manage_channels = True)
async def take(ctx, arg, member: discord.Member):
    await ctx.channel.purge(limit = 1)
    role = discord.utils.get(ctx.message.guild.roles, name = arg)
    await member.remove_roles(role)
    channel = client.get_channel(714175791033876490)
    await channel.send(f'{ctx.author.mention} забрал @{role} у {member.mention}')
    
@client.command(aliases = ['img&'])
@commands.has_permissions(manage_channels = True)
async def image(ctx, arg, *):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.set_image(url = arg)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['emb_g'])
@commands.has_permissions(mention_everyone = True)
@commands.cooldown(1, 20, commands.BucketType.default)
async def gaystvo_embed(ctx, d, t, img, f, *):
    await ctx.channel.purge(limit = 1)
    await ctx.send('@everyone')
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.add_field(name = d, value = t)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)
    
@client.command(aliases = ['Embed', 'EMBED', 'emb' , 'Emb', 'EMB'])
@commands.has_permissions(manage_channels = True)
async def embed(ctx, d, t, img, f, *):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(colour = ctx.author.color)
    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    emb.add_field(name = d, value = t)
    emb.set_image(url = img)
    emb.set_thumbnail(url = f)
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

@client.command(aliases = ['Gaystvo', 'GAYSTVO'])
@commands.cooldown(1, 20, commands.BucketType.default)
@commands.has_permissions(mention_everyone = True)
async def gaystvo(ctx, *, arg):
    await ctx.channel.purge(limit = 1)
    await ctx.send('@everyone ' + arg)
    
@client.command(aliases = ['Say', 'SAY'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(manage_channels = True)
async def say(ctx, *, arg):
    await ctx.channel.purge(limit = 1)
    await ctx.send(arg)
    
@client.command(aliases = ['c', 'C', 'coin', 'Coin', 'COIN', 'Coinflip', 'COINFLIP'])
@commands.cooldown(5, 10, commands.BucketType.default)
async def coinflip(ctx):
    await ctx.channel.purge(limit = 1)
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
@client.command(aliases = ['Join', 'JOIN'])
async def join(ctx):
	await ctx.channel.purge(limit = 1)
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
    else:
        await ctx.send("Ты должен быть в канале, чтобы использовать это.")
        return
    global vc
    try:
        vc = await channel.connect()
        await change_voice_state(self_deaf = True)
    except:
        pass

@client.command(aliases = ['Leave', 'LEAVE'])
async def leave(ctx):
	await ctx.channel.purge(limit = 1)
    try:
        if vc.is_connected():
            await vc.disconnect()
    except:
        pass

@client.command()
@commands.has_permissions(administrator = True)
@commands.cooldown(1, 5, commands.BucketType.default)
async def pm(ctx, member: discord.Member, arg):
    await ctx.channel.purge(limit = 1)
    await member.send(f'{arg}')

@client.event
async def on_member_join(member):
    channel = client.get_channel(693929823030214658)
    role = discord.utils.get(member.guild.roles, id = 693933516294979704)
    role1 = discord.utils.get(member.guild.roles, id = 693933510523879454)
    role2 = discord.utils.get(member.guild.roles, id = 693933514198089838)
    if role is not None:
        await member.add_roles(role, role1, role2)
    await channel.send(embed = discord.Embed(description = f'{member.name} Has entered the facility, 👋', colour = discord.Color.orange()))

@client.event
async def on_member_remove(member):
    channel = client.get_channel(693929823030214658)
    await channel.send(embed = discord.Embed(description = f'{member.name} Has exited the facility...', colour = discord.Color.red()))
   
@client.event
async def on_message(message):
	guild = message.guild
	channel = client.get_channel(714175791033876490)
	if channel is None:
		await client.process_commands(message)
		return
	if not message.author.bot:
		emb = discord.Embed(colour = discord.Color.orange(), timestamp = datetime.datetime.utcnow())
		emb.set_author(name = message.author, icon_url = message.author.avatar_url)
		emb.add_field(name = 'В канале', value = message.channel.mention)
		emb.add_field(name = 'Было написано', value = message.content)
		emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
		if len(message.attachments) > 0:
			embed.set_image(url = message.attachments[0].url)
		await channel.send(embed = emb)
		await client.process_commands(message)
	
#help command
@client.command(aliases = ['Help', 'HELP'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(kick_members = True)
async def help(ctx):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(title = "Меню команд для администраторов", colour = discord.Color.orange())
    emb.add_field(name = 'Инфо', value = 'Cy, или же сай - бот, написанный сасиска#2472')
    emb.add_field(name = 'cy/info', value = 'Команда для определения, в сети ли бот', inline = False)
    emb.add_field(name = 'cy/clear', value = 'Очистка чата.')
    emb.add_field(name = 'cy/rap', value = '.rap')
    emb.add_field(name = 'cy/ban', value = 'Бан игрока.')
    emb.add_field(name = 'cy/kick', value = 'Кик игрока.')
    emb.add_field(name = 'cy/mute', value = 'Мут игрока. Пример: cy/mute @StakanDudka64 10 (время измеряется в минутах). По прошествии времени мут автоматически слетает.', inline = False)
    emb.add_field(name = 'cy/unmute', value = 'Размут игрока.')
    emb.add_field(name = 'cy/remind', value = 'Может напомнить вам что угодно, даже suck some dick. Формат - cy/remind "suck some dick" 10')
    emb.add_field(name = 'cy/say', value = 'Пишет сообщение от лица бота. Всё.')
    emb.add_field(name = 'cy/gaystvo', value = 'Пишет от лица бота и пингует @everyone')
    emb.add_field(name = 'cy/embed', value = 'От лица бота отправляется эмбед. Прочтите #инструкции-cy-бот , чтобы узнать подробнее.')
    emb.add_field(name = 'cy/gaystvo_embed', value = 'Совмещает в себе команды gaystvo и embed.')
    emb.add_field(name = 'cy/image', value = 'Бот может прикрепить изображение, в аргумент нужно указать ссылку.')
    emb.add_field(name = 'cy/about', value = 'Показывает информацию о человеке.')
    emb.add_field(name = 'cy/guild', value = 'Показывает информацию о сервере.')
    emb.add_field(name = 'cy/pm', value = 'Пишет участнику любой написанный текст. Формат - cy/pm @пинг "сообщение"')
    emb.add_field(name = 'cy/join', value = 'Бот заходит в голосовой канал.')
    emb.add_field(name = 'cy/leave', value = 'Бот выходит из голосового канала.')
    emb.add_field(name = 'cy/give', value = 'Выдаёт роль, писать в формате: give ("выдаваемая роль"(кавычки обязательны для ролей с пробелами)) (пинг пользователя)', inline = False)
    emb.add_field(name = 'cy/take', value = 'Забирает роль, писать в формате: take ("забираемая роль"(кавычки обязательны для ролей с пробелами)) (пинг пользователя)', inline = False)
    emb.add_field(name = 'Послесловие', value = 'Также, для написания команд необязательно писать префикс, можно пингануть бота.')
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
    await ctx.send(embed = emb)

@client.command()
async def time(ctx):
    await ctx.channel.purge(limit = 1)
    emb = discord.Embed(colour = discord.Color.orange())
    emb.set_footer(text = 'Cephalon Cy от сасиска#2472')
    now_date = datetime.datetime.now()
    emb.add_field(name = 'Время по Гринвичу равняется', value = now_date)
    await ctx.author.send(embed = emb)

#проверка на подключение
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Game('Discord API'))

#kick
@client.command(aliases = ['Kick', 'KICK'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(kick_members = True)
async def kick(ctx , member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    if member.id != client.owner_id:
        emb = discord.Embed(title = f'Кик от {ctx.author.name}', colour = member.color)
        await member.kick(reason = reason)
        emb.add_field(name = 'Кикнут', value = member.mention)
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
    else:
        await ctx.send(f'Извините, {ctx.author.mention}, но вы не можете кикнуть моего создателя!')
#ban
@client.command(aliases = ['Ban', 'BAN'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(ban_members = True)
async def ban(ctx, reason, member: discord.Member, *):
    await ctx.channel.purge(limit = 1)
    if member.id != client.owner_id:
        emb = discord.Embed(title = f'Бан от {ctx.author.name}', colour = member.color)
        await member.ban(reason = reason)
        emb.add_field(name = 'Забанен', value = member.mention)
        emb.set_footer(text = 'Cephalon Cy от сасиска#2472. Secured by Knox')
        await ctx.send(embed = emb)
    else:
        await ctx.send(f'Извините, {ctx.author.mention}, но вы не можете забанить моего создателя!')
        
#message delete
@client.command(aliases = ['Clear', 'CLEAR'])
@commands.cooldown(1, 10, commands.BucketType.default)
@commands.has_permissions(administrator = True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount + 1)
    if amount == 1:
        await ctx.send(f'удалено {amount} сообщение', delete_after = 1)
    elif amount == 2:
        await ctx.send(f'удалено {amount} сообщения', delete_after = 1)
    elif amount == 3:
        await ctx.send(f'удалено {amount} сообщения', delete_after = 1)
    elif amount == 4:
        await ctx.send(f'удалено {amount} сообщения', delete_after = 1)
    else:
        await ctx.send(f'удалено {amount} сообщений', delete_after = 1)
    
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{ctx.author.mention}, чё это за команда?')
        
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'{ctx.author.mention}, команда в кд, потерпи чутка!')
    
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
        await ctx.send(f'{ctx.author.mention}, кого и на сколько мутить то?')
        
    if isinstance(error, commands.BadArgument):
        await ctx.send(f'{ctx.author.mention}, проверьте правильность написания команды')
                       
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
