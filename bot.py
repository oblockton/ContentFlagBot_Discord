# Content Flagging Bot for Discord
# Created by: Oblockton github.com/Oblockton
import os
import datetime
import joblib
import discord
from discord.ext import commands
import erasehate as eh


token = os.environ.get('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix='_')

results_channel = 'none set'

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord hoe!!!')

# Print to console and log when client joins a guild
@client.event
async def on_guild_join(guild):
    now = datetime.datetime.now().strftime('%Y-%M-%d')
    print(f'{client.user} has joined: {guild.name} (id: {guild.id}) @{now}')
    with open('guild_join_log.txt','a') as f:
        print(f'Connected to guild: {guild.name} (id: {guild.id}) @{now}', file=f)

# Print to console and log when client is removed from a guild
@client.event
async def on_guild_remove(guild):
    now = datetime.datetime.now().strftime('%Y-%M-%d')
    print(f'{client.user} has has been removed from {guild.name} (id: {giuld.id}) @{now}')
    with open('guild_revmove_log.txt','a') as f:
        print(f'Removed from guild:{guild.name}(id: {guild.id}) @{now}', file=f)


@bot.command(name='response-channel',pass_context=True, help='Sets the channel the bot should respond in. All bot responses happen in this one channel.')
@commands.has_persmissions(administrator=True, manage_channels=True)
async def _set_response_channel(ctx, action, channel_name):
    action = action.lower()
    if action != 'set' or action != 'create':
        await ctx.send('Incorrect response-channel command arguments,options: Set or Create')
    else:
        if action == 'create':
            guild = ctx.guild
            existing_channel = discord.utils.get(guild.channels, name=channel_name)
            if not existing_channel:
                msg=await bot.say("Creating channel for flags: {}",format(channel_name))
                if ctx.message.server.me.server_permissions.administrator or ctx.message.server.me.server_permissions.manage_channels:
                    try:
                        await guild.create_text_channel(channel_name)
                        response_channel_list = joblib.load("guild_respone_channels.pkl")
                        created_channel = discord.utils.get(guild.channels, name=channel_name)
                        response_channel_list.append([guild.name,guild.id,created_channel.name,created_channel.id])
                        joblib.dump(response_channel_list,'guild_response_channels.pkl')
                        await bot.edit_message(msg, new_content='Channel {} create successfully!'.format(channel_name))
                    except Exception:
                        await bot.edit_message(msg, new_content='I was unable to create the channel. ')
                else:
                    await bot.edit_message(msg, new_content='I(bot) do not have permission to create channels. :/ ')
        elif action = 'set':
            response_channel_list = joblib.load("guild_respone_channels.pkl")
            if guild.id not in [x[1] for x in response_channel_list]:
                created_channel = discord.utils.get(guild.channels, name=channel_name)
                response_channel_list.append([guild.name,guild.id,created_channel.name, created_channel.id])
                joblib.dump(response_channel_list,'guild_response_channels.pkl')
            else:
                for guild_item in response_channel_list:
                    if guild_item[1]== guild.id:
                        guild_item[2], guild_item[3] = discord.utils.get(guild.channels,name=channel_name).name, discord.utils.get(guild.channels,name=channel_name).id

#Handle user permission and argument errors for response-channel command.
@_set_response_channel.error
async def set_channel_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        text = "Sorry {}, you or I do not have permissions to do that! Check you have permission to manage channel. Check that I also have manage_channels permission".format(ctx.message.author)
        await ctx.send(text)
    elif isinstance(error,commands.MissingRequiredArgument):
        if error.param.name == 'action':
            await ctx.send("""I need to know if you want to create a new channel for flags(create), or send flags to an existing channel(set)\n
            Command Example: _response-channel set nameofchannel""")
        elif error.param.name == 'channel_name':
            await ctx.send('No channel name specified. Command Example: _response-channel set channelname or _response-channel create channelname')





# # @client.event
# # async def on_message(message):
#     if message.author != client.user:
#         # Send message to api
#         # if any results are hateful or offensive, create the results response.
#         if results_channel != 'none set':
#             # respond in channel specified by results_channel:
#         else:
#             message.channel.send(results)

        ####Send to EH App
        ## If any to be flagged,respond in Admins chosen response channel.

client.run(token)
bot.run(token)
