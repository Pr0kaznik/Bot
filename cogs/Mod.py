import asyncio
import datetime
import os
import re

import disnake
from disnake.ext import commands
from pymongo import MongoClient

passw = os.environ.get('passw')
cluster = MongoClient(f"mongodb+srv://cephalon:{passw}@locale.ttokw.mongodb.net/Locale?retryWrites=true&w=majority")
collection = cluster.Locale.locale

friends = [351071668241956865, 417362845303439360]

guilds = [693929822543675455, 735874149578440855, 818758712163827723]

time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        time = 0
        matches = re.findall(time_regex, args)
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                await ctx.send(f'{value} не является правильным аргументом! Правильные: h|m|s|d')
            except ValueError:
                await ctx.send(f'{key} не число!')
        return time

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Модуль Mod загружен')

    @commands.command()
    @commands.has_permissions(view_audit_log = True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dm(self, ctx, member: disnake.Member, * , text):
        emb = disnake.Embed(description = f'{text}', colour = 0x2f3136)
        emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
        await member.send(embed = emb)
        rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if rlocale == 'ru':
            await ctx.send('Сообщение отправлено.')
        if rlocale == 'gnida':
            await ctx.send('Твоя хуйня отправлена')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: disnake.Member, *, reason: str = None):
        rlocale = rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        bot = disnake.utils.get(ctx.guild.members, id = self.client.user.id)
        if member.id != 338714886001524737:
            if reason == None:
                if rlocale == 'ru':
                    reason = 'Не указана.'
                if rlocale == 'gnida':
                    reason = 'Я не ебу'
            if ctx.author == member:
                emb = disnake.Embed(description = 'Ты **не** можешь кикнуть себя.', color = disnake.Color.blurple())
                await ctx.send(embed = emb)
            if ctx.author.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Кик отклонён.', colour = disnake.Color.orange())
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'Твоя высшая роль равна высшей роли {member.mention}. Пошёл нахуй.', colour = disnake.Color.orange())
                    await ctx.send(embed = emb)
            elif member.top_role > ctx.author.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Кик отклонён.', colour = disnake.Color.orange())
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'Твоя высшая роль ниже высшей роли {member.mention}. Пошёл нахуй.', colour = disnake.Color.orange())
                    await ctx.send(embed = emb)
            elif member.top_role > bot.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Кик невозможен.', color = 0xff0000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Сука.', color = 0xff0000)
                    await ctx.send(embed = emb)
            elif member.top_role == bot.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Кик невозможен.', color = 0xff0000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Сука.', color = 0xff0000)
                    await ctx.send(embed = emb)
            else:
                emb = disnake.Embed(colour = member.color)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                emb.add_field(name = 'Был кикнут', value = member.mention)
                emb.add_field(name = 'По причине', value = reason)
                await ctx.send(embed = emb)
                await member.kick(reason = reason)
        else:
            if rlocale == 'ru':
                emb = disnake.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете кикнуть моего создателя!', colour = disnake.Color.orange())
                await ctx.send(embed = emb)
            if rlocale == 'gnida':
                emb = disnake.Embed(description = 'Ого! Пошёл нахуй!', colour = disnake.Color.orange())
                await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: disnake.Member, *, reason: str = None):
        rlocale = rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        bot = disnake.utils.get(ctx.guild.members, id = self.client.user.id)
        if member.id != 338714886001524737:
            if reason == None:
                if rlocale == 'ru':
                    reason = 'Не указана.'
                if rlocale == 'gnida':
                    reason = 'Я не ебу'
            if ctx.author == member:
                emb = disnake.Embed(description = 'Ты **не** можешь забанить себя.', color = disnake.Color.blurple())
                await ctx.send(embed = emb)
            if ctx.author.top_role == member.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Бан отклонён.', colour = disnake.Color.orange())
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'Твоя высшая роль равна высшей роли {member.mention}. Саси.', colour = disnake.Color.orange())
                    await ctx.send(embed = emb)
            elif member.top_role > ctx.author.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Бан отклонён.', colour = disnake.Color.orange())
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    await ctx.send(embed = emb)
            elif member.top_role > bot.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Бан невозможен.', color = 0xff0000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Блять.', color = 0xff0000)
                    await ctx.send(embed = emb)
            elif member.top_role == bot.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Бан невозможен.', color = 0xff0000)
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Блять.', color = 0xff0000)
                    await ctx.send(embed = emb)
            else:
                if '--soft' in reason:
                    emb = disnake.Embed(color = 0x2f3136)
                    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                    emb.add_field(name = 'Упрощённо забанен', value = f'{member.mention} ({member.name})')
                    if '--reason' in reason:
                        reason = reason.strip()[15:].strip()
                    else:
                        if rlocale == 'ru':
                            reason = 'Не указана.'
                        if rlocale == 'gnida':
                            reason == 'Я не ебу'
                    emb.add_field(name = 'По причине', value = reason)
                    await ctx.send(embed = emb)
                    await member.ban(reason = reason)
                    await member.unban(reason = '--softban')
                else:
                    emb = disnake.Embed(colour = 0x2f3136)
                    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                    emb.add_field(name = 'Был забанен', value = member.mention)
                    emb.add_field(name = 'По причине', value = reason)
                    await ctx.send(embed = emb)
                    await member.ban(reason = reason)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def give(self, ctx, member: disnake.Member, role: disnake.Role):
        rlocale = rlocale = collection.find_one({"_id": ctx.author.id})["locale"]
        if role != None:
            if role.name == 'Muted':
                if member.id != self.client.owner_id:
                    await member.add_roles(role)
                    if rlocale == 'ru':
                        emb = disnake.Embed(description = f'{member.mention} был перманентно заглушён {ctx.author.mention}', color = 0x2f3136)
                        return await ctx.send(embed = emb)
                    if rlocale == 'gnida':
                        emb = disnake.Embed(description = f'{member.mention} получает мут в ебало от {ctx.author.mention}', color = 0x2f3136)
                        return await ctx.send(embed = emb)
                else:
                    emb = disnake.Embed(description = 'Ты думал мой Создатель тебе по зубам? ОН!?', color = 0xff0000)
                    return await ctx.send(embed = emb)
            if role > ctx.author.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'Вы не можете выдать {role.mention}, так как она имеет более высокий ранг, чем ваша высшая роль.', color = disnake.Color.orange())
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'Дебилам вроде тебя запрещено выдавать {role.mention}, так как эта роль выше твоей высшей роли.', color = disnake.Color.orange())
                    await ctx.send(embed = emb)
            elif role == ctx.author.top_role:
                if rlocale == 'ru':
                    emb = disnake.Embed(description = f'Вы не можете выдать {role.mention} кому-либо, так как она равна вашей высшей роли.', color = disnake.Color.orange())
                    await ctx.send(embed = emb)
                if rlocale == 'gnida':
                    emb = disnake.Embed(description = f'Дебилам вроде тебя запрещено выдавать {role.mention}, так как она равна твоей высшей роли.', color = disnake.Color.orange())
                    await ctx.send(embed = emb)
            else:
                await member.add_roles(role)
                emb = disnake.Embed(colour = member.color, timestamp = datetime.datetime.utcnow())
                emb.add_field(name = 'ВЫДАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
                emb.add_field(name = 'ВЫДАНА:', value = member.mention, inline = False)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                await ctx.send(embed = emb)
        else:
            emb = disnake.Embed(description = f'{ctx.author.mention}, я не могу найти {role.mention} в списке ролей.', colour = member.color, timestamp = disnake.utils.utcnow())
            await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def take(self, ctx, member: disnake.Member, role: disnake.Role):
        if role != None:
            bot = ctx.guild.get_member(self.client.user.id)
            if role.name == 'Muted':
                await member.remove_roles(role)
                emb = disnake.Embed(description = f'{member.mention} был разглушён {ctx.author.mention}', color = 0x2f3136)
                return await ctx.send(embed = emb)
            if role > ctx.author.top_role and ctx.message.author.id != 338714886001524737:
                emb = disnake.Embed(description = f'Вы не можете забрать {role.mention}, так как она имеет более высокий ранг, чем ваша высшая роль. Забирание роли отменено.', color = 0x2f3136)
                await ctx.send(embed = emb)
            elif role == ctx.author.top_role and ctx.message.author.id != 338714886001524737:
                emb = disnake.Embed(description = f'Вы не можете забрать {role.mention}, так как она равна вашей высшей роли. Забирание роли отменено.', color = 0x2f3136)
                await ctx.send(embed = emb)
            elif member.top_role > bot.top_role:
                emb = disnake.Embed(description = f'МОЯ высшая роль ниже высшей роли {member.mention}. Забрать роль невозможно.', color = 0xff0000)
                await ctx.send(embed = emb)
            elif member.top_role == bot.top_role:
                emb = disnake.Embed(description = f'МОЯ высшая роль идентична высшей роли {member.mention}. Забрать роль невозможно.', color = 0xff0000)
                await ctx.send(embed = emb)
            elif role.is_default():
                emb = disnake.Embed(description = 'Забрать @everyone?', color = 0x2f3136)
                await ctx.send(embed = emb)
            else:
                await member.remove_roles(role)
                emb = disnake.Embed(colour = member.color, timestamp = disnake.utils.utcnow())
                emb.add_field(name = 'ЗАБРАНА_РОЛЬ', value = f'{role.mention} | {role.name} | ID {role.id}')
                emb.add_field(name = 'ЗАБРАНА_У:', value = member.mention, inline = False)
                emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                await ctx.send(embed = emb)
        else:
            emb = disnake.Embed(description = f'{ctx.author.mention}, я не могу найти {role.mention} в списке ролей.', colour = member.color, timestamp = disnake.utils.utcnow())
            await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(view_audit_log = True)
    async def mute(self, ctx, member: disnake.Member, time: TimeConverter, *, reason = None):
        if time < 300:
            color = 0x2f3136
        if time >= 300:
            color = disnake.Color.orange()
        if time >= 1200:
            color = 0xff0000
        if reason == None:
            reason = 'Не указана.'
        role = disnake.utils.get(ctx.guild.roles, name = 'Muted')
        if role in member.roles:
            emb = disnake.Embed(description = 'Роль Muted уже есть в списке ролей участника.', color = 0x2f3136)
            return await ctx.send(embed = emb)
        if member.id != 338714886001524737:
            if ctx.author.top_role == member.top_role and ctx.message.author.id != 338714886001524737:
                emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Заглушение отклонено.', colour = disnake.Color.orange())
                await ctx.send(embed = emb)
            elif ctx.author.top_role < member.top_role and ctx.message.author.id != 338714886001524737:
                emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Заглушение отклонено.', colour = disnake.Color.orange())
                await ctx.send(embed = emb)
            else:
                if role != None:
                    await member.add_roles(role)
                    emb = disnake.Embed(colour = color, timestamp = disnake.utils.utcnow())
                    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                    emb.add_field(name = 'Заглушён', value = f'{member.mention}')
                    emb.add_field(name = 'По причине', value = reason)
                    emb.add_field(name = 'Время заглушения', value = f'{time}s')
                    await ctx.send(embed = emb, delete_after = time)
                    await asyncio.sleep(time)
                    if role != None:
                        if role in member.roles:
                            emb = disnake.Embed(colour = color, timestamp = disnake.utils.utcnow())
                            emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                            emb.add_field(name = 'Был в муте по причине', value = reason)
                            emb.add_field(name = 'Время мута составляло', value = f'{time}s')
                            await member.remove_roles(role)
                            await ctx.send(f'{member.mention}', embed = emb)
                        else:
                            emb = disnake.Embed(description = f'Снятие заглушения для {member.mention} не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = disnake.Color.orange())
                            await ctx.send(embed = emb)
                    else:
                        emb = disnake.Embed(description = f'Невозможно снять заглушение у {member.mention}, т.к. роль Muted была удалена.', colour = disnake.Color.orange(), timestamp = disnake.utils.utcnow())
                        await ctx.send(embed = emb)
                else:
                    role = await ctx.guild.create_role(name = 'Muted', colour = 0x000001, reason = 'Создано автоматически командой mute')
                    await member.add_roles(role)
                    emb = disnake.Embed(colour = color, timestamp = disnake.utils.utcnow())
                    emb.set_author(name = ctx.author, icon_url = ctx.author.avatar.url)
                    emb.add_field(name = 'Заглушён', value = f'{member.mention}')
                    emb.add_field(name = 'По причине', value = reason)
                    emb.add_field(name = 'Время заглушения', value = f'{time}s')
                    await ctx.send(embed = emb, delete_after = time)
                    await asyncio.sleep(time)
                    if role != None:
                        if role in member.roles:
                            emb = disnake.Embed(colour = color, timestamp = disnake.utils.utcnow())
                            emb.add_field(name = 'Размучен по истечению времени', value = member.mention)
                            emb.add_field(name = 'По причине', value = reason)
                            emb.add_field(name = 'Время мута составляло', value = f'{time}s')
                            await ctx.send(f'{member.mention}', embed = emb)
                            await member.remove_roles(role)
                        else:
                            emb = disnake.Embed(description = f'Снятие заглушения для {member.mention} не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = disnake.Color.orange())
                            await ctx.send(embed = emb)
                    else:
                        emb = disnake.Embed(description = f'Невозможно снять заглушение у {member.mention}, т.к. роль Muted была удалена.', colour = disnake.Color.orange(), timestamp = disnake.utils.utcnow())
                        await ctx.send(embed = emb)
        else:
            emb = disnake.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете заглушить моего создателя!', colour = disnake.Color.orange())
            await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def timeout(self, ctx, member: disnake.Member, duration: TimeConverter, *, reason = None):
        if reason == None:
            reason = 'Не указана.'
        if member.id != self.client.owner_id:
            if ctx.author.top_role == member.top_role and ctx.message.author.id != 338714886001524737:
                emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Тайм-аут отклонён.', colour = disnake.Color.orange())
                await ctx.send(embed = emb)
            elif ctx.author.top_role < member.top_role and ctx.message.author.id != 338714886001524737:
                emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Тайм-аут отклонён.', colour = disnake.Color.orange())
                await ctx.send(embed = emb)
            else:
                await member.timeout(reason = reason, duration = duration)
                emb = disnake.Embed(title = f'Тайм-аут участника {member}', color = 0x2f3136, timestamp = disnake.utils.utcnow())
                emb.add_field(name = 'Причина', value = reason)
                emb.add_field(name = 'Время тайм-аута', value = f'{duration}s')
                await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def deaf(self, ctx, member: disnake.Member, *, reason = None):
        role = disnake.utils.get(ctx.guild.roles, name = 'Deafened')
        if reason == None:
            reason = 'Не указана.'
        if role in member.roles:
            emb = disnake.Embed(description = 'Роль Deafened уже есть в списке ролей участника.', color = 0x2f3136)
            return await ctx.send(embed = emb)
        if member.id != self.client.owner_id:
            if ctx.author.top_role == member.top_role and ctx.message.author.id != 338714886001524737:
                emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль равна высшей роли {member.mention}. Заглушение отклонено.', colour = disnake.Color.orange())
                await ctx.send(embed = emb)
            elif ctx.author.top_role < member.top_role and ctx.message.author.id != 338714886001524737:
                emb = disnake.Embed(description = f'{ctx.author.mention}, ваша высшая роль ниже высшей роли {member.mention}. Заглушение отклонено.', colour = disnake.Color.orange())
                await ctx.send(embed = emb)
            else:
                if role != None:
                    await member.add_roles(role)
                    emb = disnake.Embed(color = 0x2f3136, timestamp = disnake.utils.utcnow())
                    emb.add_field(name = 'Заглушён', value = member.mention)
                    emb.add_field(name = 'Причина', value = reason)
                    await ctx.send(embed = emb)
                else:
                    role = await ctx.guild.create_role(name = 'Deafened', color = 0x000001, reason = 'Создано автоматически командой deaf')
                    await member.add_roles(role)
                    emb = disnake.Embed(color = 0x2f3136, timestamp = disnake.utils.utcnow())
                    emb.add_field(name = 'Заглушён', value = member.mention)
                    emb.add_field(name = 'Причина', value = reason)
                    await ctx.send(embed = emb)
        else:
            emb = disnake.Embed(description = f'Извините, {ctx.author.mention}, но вы не можете заглушить моего создателя!', colour = disnake.Color.orange())
            await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def undeaf(self, ctx, member: disnake.Member, *, reason = None):
        role = disnake.utils.get(ctx.guild.roles, name = 'Deafened')
        if reason == None:
            reason = 'Не указана.'
        if member.id != self.client.owner_id:
            if role != None:
                if role in member.roles:
                    await member.remove_roles(role)
                    emb = disnake.Embed(title = f'Принудительное снятие заглушения у {member}', color = 0x2f3136, timestamp = disnake.utils.utcnow())
                    emb.add_field(name = 'Снял заглушение', value = ctx.author.mention)
                    emb.add_field(name = 'Причина', value = reason)
                    await ctx.send(embed = emb)
                else:
                    emb = disnake.Embed(description = 'Снятие заглушения не требуется. Роли Deafened не обнаружено в списке ролей участника.', colour = disnake.Color.orange())
                    await ctx.send(embed = emb)
            else:
                emb = disnake.Embed(description = f'{ctx.author.mention}, Я не могу снять заглушение у {member.mention} из-за того, что роль Deafened была удалена', colour = disnake.Color.orange(), timestamp = disnake.utils.utcnow())
                await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def unmute(self, ctx, member: disnake.Embed, *, reason = None):
        role = disnake.utils.get(ctx.guild.roles, name = 'Muted')
        if role != None:
            if role in member.roles:
                await member.remove_roles(role)
                if reason == None:
                    reason = 'Не указана.'
                emb = disnake.Embed(title = f'Принудительное снятие заглушения у {member}', colour = 0x2f3136, timestamp = disnake.utils.utcnow())
                emb.add_field(name = 'Снял заглушение', value = ctx.author.mention)
                emb.add_field(name = 'По причине', value = reason)
                await ctx.send(embed = emb)
            else:
                emb = disnake.Embed(description = 'Снятие заглушения не требуется. Роли Muted не обнаружено в списке ролей участника.', colour = disnake.Color.orange())
                await ctx.send(embed = emb)
        else:
            emb = disnake.Embed(description = f'{ctx.author.mention}, Я не могу снять заглушение у {member.mention} из-за того, что роль Muted была удалена', colour = disnake.Color.orange(), timestamp = disnake.utils.utcnow())
            await ctx.send(embed = emb)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator = True)
    async def clear(self, ctx, amount: int, members = '--everyone', *, filt = None):
        await ctx.message.delete()
        authors = {}
        if "--everyone" not in members and '--bots' not in members and '--users' not in members and '--silent' not in members:
            member_list = [x.strip() for x in members.split(", ")]
            for member in member_list:
                if "@" in member:
                    member = member[3 if "!" in member else 2:-1]
                if member.isdigit():
                    member_object = ctx.guild.get_member(int(member))
                else:
                    member_object = ctx.guild.get_member_named(member)
                if not member_object:
                    return await ctx.send("Невозможно найти участника.")
        if not '--silent' in members:
            async for message in ctx.channel.history(limit = amount):
                if message.author not in authors:
                    authors[message.author] = 1
                else:
                    authors[message.author] += 1
        if amount == 2472:
            if ctx.author.id == self.client.owner_id:
                await ctx.channel.delete()
                emb = disnake.Embed(description = f'канал `{ctx.channel.name}` удалён.', color = 0x2f3136)
                await ctx.author.send(embed = emb)
            else:
                await ctx.author.send('Как ты узнал об этом?!')
        elif amount >= 300:
            emb = disnake.Embed(description = f'{ctx.author.mention}, при таком числе удаления сообщений ({amount}) возможно большое время ожидания ответа {self.client.user.mention}.', colour = 0x2f3136)
            await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
        elif amount >= 250:
            if ctx.author != ctx.guild.owner:
                emb = disnake.Embed(description = f'{ctx.author.mention}, операция с данным числом ({amount}) доступна только {ctx.guild.owner.mention}.', colour = 0x2f3136)
                await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 5)
            else:
                emb = disnake.Embed(description = f'{ctx.author.mention}, обнаружено слишком большое число для удаления сообщений ({amount}). Возможны дальнейшие ошибки в работе {self.client.user.mention}. Продолжить? (y/n)\n||Отмена через 10 секунд.||', colour = 0x2f3136)
                sent = await ctx.send(embed = emb)
                try:
                    msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel)
                    if msg.content.lower() == 'y' and msg.author.id == ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        if '--silent' not in members:
                            emb = disnake.Embed(description = 'Проверяем..', color = 0x2f3136)
                            sent = await ctx.send(embed = emb)
                            if members == '--bots':
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            elif members == '--users':
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            else:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            try:
                                if '--silent' in members:
                                    return
                                msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                await sent.edit(embed = emb)
                            except asyncio.TimeoutError:
                                await sent.delete()
                        else:
                            if '--bots' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                            elif '--users' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                            elif '--everyone' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                            elif members == '--silent':
                                if filt == None:
                                    await ctx.channel.purge(limit = amount)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                    elif msg.content.lower() == 'n' and msg.author.id == ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'{ctx.guild.owner.mention} отменил запрос.', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    elif msg.content.lower() == 'n' or 'y' and msg.author.id != ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера.', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    else:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                except asyncio.TimeoutError:
                    await sent.delete()
                    emb = disnake.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = 0x2f3136)
                    await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 3)
        elif amount >= 100:
            if ctx.author != ctx.guild.owner:
                emb = disnake.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Мне нужен ответ создателя сервера на это действие. Продолжаем? (y/n)\n||Запрос будет отменён через 1 минуту.||', colour = 0x2f3136)
                sent = await ctx.send(f'{ctx.guild.owner.mention}', embed = emb)
                try:
                    msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                    if msg.content.lower() == 'y':
                        await msg.delete()
                        await sent.delete()
                        if '--silent' not in members:
                            emb = disnake.Embed(description = 'Проверяем..', color = 0x2f3136)
                            sent = await ctx.send(embed = emb)
                            if members == '--bots':
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            elif members == '--users':
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            else:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            try:
                                if '--silent' in members:
                                    return
                                msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                await sent.edit(embed = emb)
                            except asyncio.TimeoutError:
                                await sent.delete()
                        else:
                            if '--bots' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                            elif '--users' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                            elif '--everyone' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                            elif members == '--silent':
                                if filt == None:
                                    await ctx.channel.purge(limit = amount)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                    elif msg.content.lower() == 'n' and msg.author.id == ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'{ctx.guild.owner} отменил запрос.', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    elif msg.content.lower() == 'n' or 'y' and msg.author.id != ctx.guild.owner.id:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'{ctx.author.mention}, ты не являешься владельцем сервера.', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    else:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                except asyncio.TimeoutError:
                    await sent.delete()
                    emb = disnake.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = 0x2f3136)
                    await ctx.send(f'{ctx.guild.owner.mention}', embed = emb, delete_after = 3)
            else:
                emb = disnake.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n||Запрос будет отменён через 10 секунд.||', colour = 0x2f3136)
                sent = await ctx.send(embed = emb)
                try:
                    msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                    if msg.content.lower() == 'y':
                        await msg.delete()
                        await sent.delete()
                        if '--silent' not in members:
                            emb = disnake.Embed(description = 'Проверяем..', color = 0x2f3136)
                            sent = await ctx.send(embed = emb)
                            if members == '--bots':
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            elif members == '--users':
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            else:
                                if filt == None:
                                    cleared = await ctx.channel.purge(limit = amount, before = sent)
                                else:
                                    cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                                await sent.edit(embed = emb)
                            try:
                                if '--silent' in members:
                                    return
                                msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                                emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                                emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                                if filt:
                                    emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                                emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                                await sent.edit(embed = emb)
                            except asyncio.TimeoutError:
                                await sent.delete()
                        else:
                            if '--bots' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                            elif '--users' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                            elif '--everyone' in members:
                                if filt == None:
                                    await ctx.channel.purge(limit = amount)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                            elif members == '--silent':
                                if filt == None:
                                    await ctx.channel.purge(limit = amount)
                                else:
                                    await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                    elif msg.content.lower() == 'n':
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = 'Отменено.', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                    else:
                        await msg.delete()
                        await sent.delete()
                        emb = disnake.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = 0x2f3136)
                        await ctx.send(embed = emb, delete_after = 3)
                except asyncio.TimeoutError:
                    await sent.delete()
                    emb = disnake.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
        elif amount >= 10:
            emb = disnake.Embed(description = f'{ctx.author.mention}, создан запрос на удаление {amount} сообщений. Продолжить? (y/n)\n||Запрос будет отменён через 10 секунд.||', colour = 0x2f3136)
            sent = await ctx.send(embed = emb)
            try:
                msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.author == ctx.author and message.channel == ctx.message.channel)
                if msg.content.lower() == 'y':
                    await msg.delete()
                    await sent.delete()
                    if '--silent' not in members:
                        emb = disnake.Embed(description = 'Проверяем..', color = 0x2f3136)
                        sent = await ctx.send(embed = emb)
                        if members == '--bots':
                            if filt == None:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                            else:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                            emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                            emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        elif members == '--users':
                            if filt == None:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                            else:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                            emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                            emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        else:
                            if filt == None:
                                cleared = await ctx.channel.purge(limit = amount, before = sent)
                            else:
                                cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                            emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                            emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                            await sent.edit(embed = emb)
                        try:
                            if '--silent' in members:
                                return
                            msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                            emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                            emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                            if filt:
                                emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                            emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                            await sent.edit(embed = emb)
                        except asyncio.TimeoutError:
                            await sent.delete()
                    else:
                        if '--bots' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                        elif '--users' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                        elif '--everyone' in members:
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                        elif members == '--silent':
                            if filt == None:
                                await ctx.channel.purge(limit = amount)
                            else:
                                await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                elif msg.content.lower() == 'n':
                    await msg.delete()
                    await sent.delete()
                    emb = disnake.Embed(description = 'Отменено.', colour = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
                else:
                    await msg.delete()
                    await sent.delete()
                    emb = disnake.Embed(description = f'Обнаружен недопустимый ответ ({msg.content})', colour = 0x2f3136)
                    await ctx.send(embed = emb, delete_after = 3)
            except asyncio.TimeoutError:
                await sent.delete()
                emb = disnake.Embed(description = f'{ctx.author.mention}, Время вышло.', colour = 0x2f3136)
                await ctx.send(embed = emb, delete_after = 3)
        elif amount == 0:
            emb = disnake.Embed(description = 'Удалять 0 сообщений? Ты еблан?', colour = 0x2f3136)
            await ctx.send(embed = emb, delete_after = 1)
        else:
            if '--silent' not in members:
                emb = disnake.Embed(description = 'Проверяем..', color = 0x2f3136)
                sent = await ctx.send(embed = emb)
                if '--bots' in members:
                    if filt == None:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True, before = sent)
                    else:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True, before = sent)
                    emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                    emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                    if filt:
                        emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                    emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                    await sent.edit(embed = emb)
                elif '--users' in members:
                    if filt == None:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False, before = sent)
                    else:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower(), before = sent)
                    emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                    emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                    if filt:
                        emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                    emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                    await sent.edit(embed = emb)
                elif members == '--everyone':
                    if filt == None:
                        cleared = await ctx.channel.purge(limit = amount, before = sent)
                    else:
                        cleared = await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower(), before = sent)
                    emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                    emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                    if filt:
                        emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                    emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                    emb.set_footer(text = 'Это сообщение удалится через 10 секунд. Для отмены напишите "c".')
                    await sent.edit(embed = emb)
                try:
                    if '--silent' in members:
                        return
                    msg = await self.client.wait_for('message', timeout = 10, check = lambda message: message.channel == ctx.message.channel and message.author == ctx.author and message.content.lower() == 'c')
                    emb = disnake.Embed(title = 'Результаты удаления сообщений', color = 0x2f3136)
                    emb.add_field(name = 'Удалено сообщений', value = f'```ARM\n{len(cleared)}```')
                    if filt:
                        emb.add_field(name = 'Применён фильтр:', value = f'```{filt}``` ({members})', inline = True)
                    emb.add_field(name = 'Проверены сообщения от:', value = ''.join([f"```ARM\n{author} : {amount}```" for author, amount in authors.items()]), inline = False)
                    await sent.edit(embed = emb)
                except asyncio.TimeoutError:
                    await sent.delete()
            else:
                if '--bots' in members:
                    if filt == None:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == True)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower() and m.author.bot == True)
                elif '--users' in members:
                    if filt == None:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.author.bot == False and m.content.lower() == filt.lower())
                elif '--everyone' in members:
                    if filt == None:
                        await ctx.channel.purge(limit = amount)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())
                elif members == '--silent':
                    if filt == None:
                        await ctx.channel.purge(limit = amount)
                    else:
                        await ctx.channel.purge(limit = amount, check = lambda m: m.content.lower() == filt.lower())

def setup(client):
    client.add_cog(Mod(client))
