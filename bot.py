import nextcord
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Bot, cooldown, BucketType
from nextcord.voice_client import VoiceClient
from nextcord.ext.tasks import loop
import asyncio
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import json


TOKEN = "token" #insert token here
intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!') #insert prefix here
bot = commands.Bot(command_prefix='!', intents=intents)
command_prefix='!'

chatbot = ChatBot('Insert Name here')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
for i in range(5):
    trainer.train("chatterbot.corpus.english")

trainer = ListTrainer(chatbot)

@bot.event
async def on_message(message):

    if message.author.id == client.user.id: #prevents bot from responding to itself
        return
    
    #checks if message is in talk-with-chatbot
    if message.channel.name == "talk-with-chatbot" and message.author.id != client.user.id:
        channel = message.channel
        #Adds message to a json to train
        with open('trainingwords.json') as f:
            data = json.load(f)
            if message.content not in data["words"]:
            #adds message to json
                data["words"].append(message.content)
                #trains bot

        with open('trainingwords.json', 'w') as f:
            json.dump(data, f)
        
        await channel.send(chatbot.get_response(message.content))

        

@tasks.loop(minutes= 5.0)
async def train():
    with open('trainingwords.json') as f:
        data = json.load(f)
        trainer.train(data["words"])

#on server join make a channel called talk-with-chatbot
@bot.event
async def on_guild_join(guild):
    channel = await guild.create_text_channel('talk-with-chatbot')
    await channel.send('Hello!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    game = nextcord.Game("status")
    train.start()
    await bot.change_presence(status=nextcord.Status.online, activity=game)

bot.run(TOKEN) 