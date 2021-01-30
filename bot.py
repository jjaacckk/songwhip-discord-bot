# bot.py
# 2021-01-28
# github.com/jjaacckk


import discord, requests
from re import findall
from os import getenv
from dotenv import load_dotenv
from datetime import datetime


def songwhip(url):
    # attemps to get SongWhip URL
    data = '{"url": "' + url + '"}'
    response = requests.post('https://songwhip.com/', data=data)

    if response.status_code == 200:
        return response.json()
    
    return False


def contains_music_link(message):
    # attemps to match each message with the RegEx pattern
    pat = "(?:http:\/\/|https:\/\/)?(?:[a-z0-9]*[\-\.])*(?:apple|spotify|youtube|bandcamp|tidal|pandora|napster|yandex|amazon|deezer|jiosaavn|audius|gaana|soundcloud|page)\.(?:com|co|link)(?:\/[^ |\n|\t|\"|\']*)+"
    matches = findall(pat, message)
    return matches
    
   
client = discord.Client()
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # checks for match on each new message
    matches = contains_music_link(message.content) 
    
    reply_message = []
    
    # if there are multiple matches (multiple song links in the same message) it will loop through each match
    for m in matches:
        #attempts to get SongWhip URL
        songwhip_JSON = songwhip(m)
        
        #if successfull, replies to original message with the SongWhip URL in an embed
        if songwhip_JSON != False:
            
            if songwhip_JSON["type"] == "artist":
                description = songwhip_JSON["description"] 
                if len(description) > 300:
                    description = description[:300] + "...."
                
                embed=discord.Embed(title=songwhip_JSON["name"], 
                                    url=songwhip_JSON["url"], 
                                    description=description, 
                                    color=0xff0088)
                embed.set_thumbnail(url=songwhip_JSON["image"])
                embed.set_footer(text="powered by SongWhip")
                
            else:
                release_time = datetime.strptime(songwhip_JSON["releaseDate"], '%Y-%m-%dT%H:%M:%S.%fZ')
                description = songwhip_JSON["artists"][0]["description"] 
                if len(description) > 300:
                    description = description[:300] + "...."
                                    
                embed=discord.Embed(title= songwhip_JSON["name"], 
                                    url=songwhip_JSON["url"], 
                                    description=songwhip_JSON["type"].title() + " · " + str(release_time.date().year), 
                                    color=0xff0088)
                embed.add_field(name="About Artist:", value=description, inline=False)
                embed.set_author(name=songwhip_JSON["artists"][0]["name"], 
                                 url="https://songwhip.com/" + songwhip_JSON["artists"][0]["url"], 
                                 icon_url=songwhip_JSON["artists"][0]["image"])
                embed.set_thumbnail(url=songwhip_JSON["image"])
                embed.set_footer(text="powered by SongWhip")

                
            await message.reply(embed=embed)


if __name__ == "__main__":
    print("running....")
    # Discord token loaded into a .env file
    # create .env file in the same path as this file and add: DISCORD_TOKEN=YOUR-TOKEN-HERE
    load_dotenv()
    TOKEN = getenv('DISCORD_TOKEN')
    
    client.run(TOKEN)



# SongWhip supported services (sometimes still unable to convert):

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

