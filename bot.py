import discord
import os
import asyncio
from response_generator import ResponseGenerator
from dotenv import load_dotenv
load_dotenv() #This code loads the environment variables from the system environment.

# Initialize your Discord bot and the response generator
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
response_generator = ResponseGenerator()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Avoid responding to messages from the bot itself
    if message.author == client.user:
        return
    
    # Check if the message starts with your command prefix (assumed '/')
    if message.content.startswith('/'):
        user_input = message.content[1:]  # Extract command or prompt after '/'
        loop = asyncio.get_event_loop()
        
        # Correctly call generate_response method in response_generator
        # Using loop.run_in_executor to run the synchronous function in an async manner
        response_text = await loop.run_in_executor(None, response_generator.generate_response, user_input)
        
        await message.channel.send(response_text)

# Run the client using the bot token from your environment variables
client.run(os.getenv('DISCORD_BOT_TOKEN'))

