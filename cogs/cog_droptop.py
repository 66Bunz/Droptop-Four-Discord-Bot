'''
Cog Name: Droptop Commands
Commands: 5
Slash Commands: 0
'''


import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, Select, SelectOption
# from discord_slash import SlashCommand, cog_ext, SlashContext
import time
from datetime import date, datetime
import json
import os
import re
import pymongo
from pymongo import MongoClient


now = datetime.now()
cluster = MongoClient(os.getenv("mongodb_id"))
db = cluster["Test_Droptop"]
collection_d = db["BetaPrg"]


class DroptopCommands(commands.Cog, name='Droptop'):
    '''These are the Droptop Commands'''


    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='info', help='This command displays info about Droptop Four', aliases=['Droptop', 'Dt'])
    async def info(self, ctx, arg=None):
        '''Displays info about Droptop Four'''
        
        def check(response):
            return ctx.author == response.user and response.channel == ctx.channel
        
        basic = ['basic', 'Basic', 'base', 'Base']
        supporter = ['supporter', 'Supporter', 'supp', 'Supp', 'sup', 'Sup']

        generic = discord.Embed(title='Droptop Four', color=discord.Color.from_rgb(75, 215, 100))
        generic.set_author(name="Created by Cariboudjan", url=self.bot.dtsite, icon_url='https://cdn.discordapp.com/avatars/584542239900827665/8d070369e6169444ad45c479ef0eec9a.png?size=1024')
        generic.set_thumbnail(url='https://cdn.discordapp.com/icons/800124057923485728/7e8f7f08dce1d220711ee2488d497c8f.webp?size=1024')
        generic.add_field(name="What is it?", value="Droptop Four is a popular dropdown app launcher for Windows & Rainmeter.\nIt is available in two version, a `Basic` one, free, and a `Supporter` one, with a \'pay what you want\' donation.\nBoth versions have 14 system tray apps, the Always Show option to make it accessible everywhere on top of your desktop and a lot more.", inline=False)
        generic.add_field(name="Basic Version", value='The `Basic` version has:\n - 7 home bottons icons\n - 6 fully-customizable toolbars\n - 4 themes to choose from', inline=True)
        generic.add_field(name='Supporter Version', value='The `Supporter` version has:\n - 300 home buttons icons\n - 12 fully-customizable toolbars\n - 22 themes to choose from', inline=True)
        generic.set_footer(text="To see further infos on one of the two versions type `{0}info basic` or `{0}info supporter` or click the buttons below".format(self.bot.command_prefix))

        base = discord.Embed(title='Droptop Four Basic Version', color=discord.Color.from_rgb(75, 215, 100))
        base.set_author(name="Created by Cariboudjan", url=self.bot.dtsite, icon_url='https://cdn.discordapp.com/avatars/584542239900827665/8d070369e6169444ad45c479ef0eec9a.png?size=1024')
        base.set_thumbnail(url='https://cdn.discordapp.com/icons/800124057923485728/7e8f7f08dce1d220711ee2488d497c8f.webp?size=1024')
        base.add_field(name="What is it?", value="This is the Basic and free version of droptop.", inline=False)
        base.add_field(name="Perks", value='The `Basic` version has:\n - 7 home bottons icons\n - 6 fully-customizable toolbars\n - 4 themes to choose from', inline=False)
        base.add_field(name="Download", value='To install it you have to download it on the DeviantArt page of Droptop Four:\nhttps://www.deviantart.com/cariboudjan/art/droptop-four-762812007\nTo see further explanations on download methods type `{}download`'.format(self.bot.command_prefix), inline=False)

        supp = discord.Embed(title='Droptop Four Supporter Version', color=discord.Color.from_rgb(75, 215, 100))
        supp.set_author(name="Created by Cariboudjan", url=self.bot.dtsite, icon_url='https://cdn.discordapp.com/avatars/584542239900827665/8d070369e6169444ad45c479ef0eec9a.png?size=1024')
        supp.set_thumbnail(url='https://cdn.discordapp.com/icons/800124057923485728/7e8f7f08dce1d220711ee2488d497c8f.webp?size=1024')
        supp.add_field(name="What is it?", value="This is the Supporter version of droptop.\nTo download it you can pay what you want through Gumroad.", inline=False)
        supp.add_field(name='Perks', value='The `Supporter` version has:\n - 300 home buttons icons\n - 12 fully-customizable toolbars\n - 22 themes to choose from', inline=False)
        supp.add_field(name="Download", value='To install it you have to:\n1)	download the Basic version on the DeviantArt page of Droptop Four (https://www.deviantart.com/cariboudjan/art/droptop-four-762812007)\n2)	download the Supporter update through Gumroad choosing how much you want to pay for it (from 0$) (https://gumroad.com/l/droptop)\nTo see further explanations on download methods type `{}download`'.format(self.bot.command_prefix), inline=False)

        if arg == None:
            send1 = await ctx.send(embed=generic, components=[[Button(label='Generic Info', id='generic', style=2, disabled=True), Button(label='Base Version Info', id="base", style=1), Button(label='Supporter Version Info', id="supp", style=3)], Button(label='Site', style=5, url=self.bot.dtsite)])

            response = await self.bot.wait_for("button_click", check=check, timeout=60)
            SelectedButton = response.component.id
            await response.respond(type=7, components=[])

            if SelectedButton == "generic":
                await send1.delete()
                await ctx.send(embed=generic)

            elif SelectedButton == "base":
                await send1.delete()
                await ctx.send(embed=base)

            elif SelectedButton == "supp":
                await send1.delete()
                await ctx.send(embed=supp)

            else:
                return

        if arg in basic:
            send2 = await ctx.send(embed=base, components=[[Button(label='Generic Info', id='generic', style=2), Button(label='Base Version Info', id="base", style=1, disabled=True), Button(label='Supporter Version Info', id="supp", style=3)], Button(label='Site', style=5, url=self.bot.dtsite)])

            response = await self.bot.wait_for("button_click", check=check, timeout=60)
            SelectedButton = response.component.id
            await response.respond(type=7, components=[])

            if SelectedButton == "generic":
                await send2.delete()
                await ctx.send(embed=generic)

            elif SelectedButton == "base":
                await send2.delete()
                await ctx.send(embed=base)

            elif SelectedButton == "supp":
                await send2.delete()
                await ctx.send(embed=supp)

            else:
                return

        if arg in supporter:
            send3 = await ctx.send(embed=supp, components=[[Button(label='Generic Info', id='generic', style=2, ), Button(label='Base Version Info', id="base", style=1), Button(label='Supporter Version Info', id="supp", style=3, disabled=True)], Button(label='Site', style=5, url=self.bot.dtsite)])

            response = await self.bot.wait_for("button_click", check=check, timeout=60)
            SelectedButton = response.component.id
            await response.respond(type=7, components=[])

            if SelectedButton == "generic":
                await send3.delete()
                await ctx.send(embed=generic)

            elif SelectedButton == "base":
                await send3.delete()
                await ctx.send(embed=base)

            elif SelectedButton == "supp":
                await send3.delete()
                await ctx.send(embed=supp)

            else:
                return


    # @cog_ext.cog_slash(name="info", description="Returns informations [argument=None, base, supporter]")
    # async def slashinfo(self, ctx):
    #   '''Displays info about Droptop Four'''

    # 	def check(response):
    # 		return ctx.author == response.user and response.channel == ctx.channel

    # 	basic=['basic', 'Basic', 'base', 'Base']
    # 	supporter=['supporter', 'Supporter', 'supp', 'Supp', 'sup', 'Sup']

    # 	generic=discord.Embed(title='Droptop Four', color=discord.Color.from_rgb(75, 215, 100))
    # 	generic.set_author(name="Created by Cariboudjan", url=self.bot.dtsite, icon_url='https://cdn.discordapp.com/avatars/584542239900827665/8d070369e6169444ad45c479ef0eec9a.png?size=1024')
    # 	generic.set_thumbnail(url='https://cdn.discordapp.com/icons/800124057923485728/7e8f7f08dce1d220711ee2488d497c8f.webp?size=1024')
    # 	generic.add_field(name="What is it?", value="Droptop Four is a popular dropdown app launcher for Windows & Rainmeter.\nIt is available in two version, a `Basic` one, free, and a `Supporter` one, with a \'pay what you want\' donation.\nBoth versions have 14 system tray apps, the Always Show option to make it accessible everywhere on top of your desktop and a lot more.", inline=False)
    # 	generic.add_field(name="Basic Version", value='The `Basic` version has:\n - 7 home bottons icons\n - 6 fully-customizable toolbars\n - 4 themes to choose from', inline=True)
    # 	generic.add_field(name='Supporter Version', value='The `Supporter` version has:\n - 300 home buttons icons\n - 12 fully-customizable toolbars\n - 22 themes to choose from', inline=True)
    # 	generic.set_footer(text="To see further infos on one of the two versions type `{0}info basic` or `{0}info supporter` or click the buttons below".format(self.bot.command_prefix))

    # 	base=discord.Embed(title='Droptop Four Basic Version', color=discord.Color.from_rgb(75, 215, 100))
    # 	base.set_author(name="Created by Cariboudjan", url=self.bot.dtsite, icon_url='https://cdn.discordapp.com/avatars/584542239900827665/8d070369e6169444ad45c479ef0eec9a.png?size=1024')
    # 	base.set_thumbnail(url='https://cdn.discordapp.com/icons/800124057923485728/7e8f7f08dce1d220711ee2488d497c8f.webp?size=1024')
    # 	base.add_field(name="What is it?", value="This is the Basic and free version of droptop.", inline=False)
    # 	base.add_field(name="Perks", value='The `Basic` version has:\n - 7 home bottons icons\n - 6 fully-customizable toolbars\n - 4 themes to choose from', inline=False)
    # 	base.add_field(name="Download", value='To install it you have to download it on the DeviantArt page of Droptop Four:\nhttps://www.deviantart.com/cariboudjan/art/droptop-four-762812007\nTo see further explanations on download methods type `{}download`'.format(self.bot.command_prefix), inline=False)

    # 	supp=discord.Embed(title='Droptop Four Supporter Version', color=discord.Color.from_rgb(75, 215, 100))
    # 	supp.set_author(name="Created by Cariboudjan", url=self.bot.dtsite, icon_url='https://cdn.discordapp.com/avatars/584542239900827665/8d070369e6169444ad45c479ef0eec9a.png?size=1024')
    # 	supp.set_thumbnail(url='https://cdn.discordapp.com/icons/800124057923485728/7e8f7f08dce1d220711ee2488d497c8f.webp?size=1024')
    # 	supp.add_field(name="What is it?", value="This is the Supporter version of droptop.\nTo download it you can pay what you want through Gumroad.", inline=False)
    # 	supp.add_field(name='Perks', value='The `Supporter` version has:\n - 300 home buttons icons\n - 12 fully-customizable toolbars\n - 22 themes to choose from', inline=False)
    # 	supp.add_field(name="Download", value='To install it you have to:\n1)	download the Basic version on the DeviantArt page of Droptop Four (https://www.deviantart.com/cariboudjan/art/droptop-four-762812007)\n2)	download the Supporter update through Gumroad choosing how much you want to pay for it (from 0$) (https://gumroad.com/l/droptop)\nTo see further explanations on download methods type `{}download`'.format(self.bot.command_prefix), inline=False)

    # 	send1 = await ctx.send(embed=generic)


    @commands.command(name='download', help='This command returns the download possibilities', aliases=['dl', 'down'])
    async def download(self, ctx):
        '''Returns the download possibilities'''
        
        down = discord.Embed(title='Droptop Four Downloads', color=discord.Color.from_rgb(75, 215, 100))
        down.set_author(name="Created by Cariboudjan", url=self.bot.dtsite, icon_url='https://cdn.discordapp.com/avatars/584542239900827665/8d070369e6169444ad45c479ef0eec9a.png?size=1024')
        down.set_thumbnail(url='https://cdn.discordapp.com/icons/800124057923485728/7e8f7f08dce1d220711ee2488d497c8f.webp?size=1024')
        down.add_field(name="Where to download?", value="The Droptop **Base** version can be downloaded on the DeviantArt page of Droptop *[https://www.deviantart.com/cariboudjan/art/droptop-four-762812007]* or by being redirected to it on the Droptop Official Site *[https://blacksquare88.wixsite.com/droptop4]* (for help about the Base version type `{0}info base`)\n\nThe Droptop **Supporter** version can be downloaded after paying what you want on Gumroad *[https://gumroad.com/l/droptop]* (for help about the Supporter version type `{0}info supporter`)".format(self.bot.command_prefix), inline=False)

        await ctx.send(embed=down, components=[[Button(label='Base', style=5, url="https://www.deviantart.com/cariboudjan/art/droptop-four-762812007"), Button(label='Supporter', style=5, url='https://gumroad.com/l/droptop'), Button(label='Site', style=5, url=self.bot.dtsite)]])


    # @cog_ext.cog_slash(name="download", description="Returns download informations")
    # async def slashdown(self, ctx):
    #   '''Returns the download possibilities'''
    
    # 	down=discord.Embed(title='Droptop Four Downloads', color=discord.Color.from_rgb(75, 215, 100))
    # 	down.set_author(name="Created by Cariboudjan", url=self.bot.dtsite, icon_url='https://cdn.discordapp.com/avatars/584542239900827665/8d070369e6169444ad45c479ef0eec9a.png?size=1024')
    # 	down.set_thumbnail(url='https://cdn.discordapp.com/icons/800124057923485728/7e8f7f08dce1d220711ee2488d497c8f.webp?size=1024')
    # 	down.add_field(name="Where to download?", value="The Droptop **Base** version can be downloaded on the DeviantArt page of Droptop *[https://www.deviantart.com/cariboudjan/art/droptop-four-762812007]* or by being redirected to it on the Droptop Official Site *[https://blacksquare88.wixsite.com/droptop4]* (for help about the Base version type `{0}info base`)\n\nThe Droptop **Supporter** version can be downloaded after paying what you want on Gumroad *[https://gumroad.com/l/droptop]* (for help about the Supporter version type `{0}info supporter`)".format(self.bot.command_prefix), inline=False)

    # 	await ctx.send(embed=down)


    @commands.command(name='faq', help='This command returns the F.A.Q. link', aliases=['f.a.q'])
    async def faq(self, ctx):
        '''Returns the F.A.Q. link'''
        
        faq = discord.Embed(title='Droptop Four F.A.Q.', color=discord.Color.from_rgb(75, 215, 100))

        faq.add_field(name="Where do I find the FAQs?", value="You can find the FAQ at https://blacksquare88.wixsite.com/droptop4/faq.", inline=False)

        await ctx.send(embed=faq, components=[Button(label='FAQs', style=5, url="https://blacksquare88.wixsite.com/droptop4/faq")])


    # @cog_ext.cog_slash(name="faq", description="Returns FAQ link")
    # async def slashfaq(self, ctx):
    #   '''Returns the F.A.Q. link'''
    
    # 	faq=discord.Embed(title='Droptop Four F.A.Q.', color=discord.Color.from_rgb(75, 215, 100))
    # 	faq.add_field(name="Where do I find the FAQs?", value="You can find the FAQ at https://blacksquare88.wixsite.com/droptop4/faq.", inline=False)

    # 	await ctx.send(embed=faq)


    @commands.command(name='beta', help='This command sends informations on how to participate to the beta program', aliases=['beta-tester', 'betatester'])
    async def beta(self, ctx, member: discord.Member = None):
        '''Sends informations on how to participate to the beta program'''

        embed = discord.Embed(title='Beta Program', description='Enroll now to the Droptop Four Beta Program! The procedure is quite easy, just follow the guidelines below!', color=0x409bda)
        embed.set_author(name="Droptop Four", url=self.bot.dtsite, icon_url=self.bot.user.avatar_url)
        embed.add_field(name='How', value='To enroll you have to have a Github account and send me the command `{0}beta-apply \"<name>\" \"<Github name>\"`'.format(self.bot.command_prefix), inline=False)
        embed.add_field(name='Example', value='`{0}beta-apply \"John Doe\" \"johndoe66\"`'.format(self.bot.command_prefix), inline=False)

        if member is not None:
            channel = member.dm_channel
            if channel is None:
                channel = await member.create_dm()
            await channel.send(embed=embed)
        else:
            await ctx.author.send(embed=embed)

        embed2 = discord.Embed(title='CHECK YOUR PMs (Personal Messages)!')
        embsend = await ctx.send(embed=embed2)
        time.sleep(5)
        await embsend.delete()


    # @cog_ext.cog_slash(name="beta", description="Returns beta informations")
    # async def slashbeta(self, ctx, member: discord.Member = None):
    #     '''Sends informations on how to participate to the beta program'''

    #     embed = discord.Embed(title='Beta Program', description='Enroll now to the Droptop Four Beta Program! The procedure is quite easy, just follow the guidelines below!', color=0x409bda)
    #     embed.set_author(name="Droptop Four", url=self.bot.dtsite, icon_url=self.bot.user.avatar_url)
    #     embed.add_field(name='How', value='To enroll you have to have a Github account and send me the command `{0}beta-apply \"<name>\" \"<Github name>\"`'.format(self.bot.command_prefix), inline=False)
    #     embed.add_field(name='Example', value='`{0}beta-apply \"John Doe\" \"johndoe66\"`'.format(self.bot.command_prefix), inline=False)

    #     if member is not None:
    #         channel = member.dm_channel
    #         if channel is None:
    #             channel = await member.create_dm()
    #         await channel.send(embed=embed)

    #     else:
    #         await ctx.author.send(embed=embed)

    #     base = discord.Embed(title='CHECK YOUR PMs (Personal Messages)!')
    #     embsend = await ctx.send(embed=base)
    #     time.sleep(5)
    #     await embsend.delete()


    @commands.command(name='beta-apply', help='This command sends your personal details to participate in the beta program')
    @commands.dm_only()
    async def bapply(self, ctx, name, githubname):
        '''Sends your personal details to participate in the beta program'''

        server = self.bot.get_guild(self.bot.server_id)
        role = discord.utils.get(server.roles, id=self.bot.betarole)
        member = server.get_member(ctx.message.author.id)

        if member:
            if role in member.roles:
                await ctx.send("You already are a beta tester")
            else:
                post = {"DateTime": now.strftime(
					"%d/%m/%Y %H:%M:%S"), "UserID": ctx.author.id, "sID": ctx.author.display_name, "Name": name, "Github Name": githubname}

                embed = discord.Embed(title='Beta Program Enrollment', description='Your informations are being sent...', color=0x409bda)
                embed.add_field(name='Your Informations:', value='```\nUserID: {0}\nsID: {1}\nName: {2}\nGithub Name: {3}\nDateTime: {4} UTC\n```'.format((ctx.author.id), (ctx.author.display_name), (name), (githubname), (now.strftime("%d/%m/%Y %H:%M:%S"))), inline=False)
                await ctx.send(embed=embed)

                collection_d.insert_one(post)

                base = discord.Embed(title='Beta Program Enrollment', description='Registration of <@{0}>'.format(ctx.author.id), color=0x409bda)
                base.add_field(name='Informations:', value='```\nUserID: {0}\nsID: {1}\nName: {2}\nGithub Name: {3}\nDateTime: {4} UTC\n```'.format((ctx.author.id), (ctx.author.display_name), (name), (githubname), (now.strftime("%d/%m/%Y %H:%M:%S"))), inline=False)

                channel = self.bot.get_channel(self.bot.betachannel)
                await channel.send(embed=base)
                # print('valid email')

                await member.add_roles(role)

        else:
            await ctx.send("You are not a member")


    @bapply.error
    async def _bapply_error(self, ctx, error):
        if isinstance(error, commands.PrivateMessageOnly):
            embed = discord.Embed(title='This command can be used only in PMs!', description='Since you have to send personal informations, you have to use this command in a PM (Private Message) with the bot.', color=0xFF2E00)
            embsend = await ctx.send(embed=embed)
            time.sleep(1)
            await ctx.message.delete()
            time.sleep(15)
            await embsend.delete()


def setup(bot):
    bot.add_cog(DroptopCommands(bot))
