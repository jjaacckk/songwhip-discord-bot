# bot.py


import os, discord, requests, re
from dotenv import load_dotenv


def songwhip(url):
    data = '{"url": "' + url + '"}'
    response = requests.post('https://songwhip.com/', data=data)

    if response.status_code == 200:
        return response.json()["url"]
    
    return False


def containsMusicLink(message):
    pat = "(?:http:\/\/|https:\/\/)?(?:[a-z0-9]*[\-\.])*(?:apple|spotify|youtube|bandcamp|tidal|pandora|napster|yandex|amazon|deezer|jiosaavn|audius|gaana|soundcloud|page)\.(?:com|co|link)(?:\/[^ |\n|\t]*)+"
    matches = re.findall(pat, message)
    return matches
    


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
   
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    
    matches = containsMusicLink(message.content)
    for m in matches:
        songwhipURL = songwhip(m)
        if songwhipURL != False:
            await message.reply("Click here to listen on other platforms: " + songwhipURL)
    

        
client.run(TOKEN)


# spotify.com
# music.apple.com
# youtube.com
# music.youtube.com
# bandcamp.com
# tidal.com
# pandora.com
# napster.com
# yandex.com
# amazon.com
# deezer.com / deezer.page.link
# jiosaavn.com
# audius.co
# gaana.com
# soundcloud.com


 #(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?([a-z0-9]*[\-\.])*(apple|spotify|youtube|bandcamp|tidal|pandora|napster|yandex|amazon|deezer|jiosaavn|audius|gaana|soundcloud)\.(com|co)(\/[^ | \n | \t].*)+