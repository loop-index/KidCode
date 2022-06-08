from queries import lcQuery
import discord
import requests
import random
import time
import json

async def lc(message, wiki):
  #find org page
  q = lcQuery if wiki == 0 else lcQuery.replace("http://scp-wiki.wikidot.com/", "http://scp-vn.wikidot.com") #0 for en 1 for vn
  response = requests.post('https://api.crom.avn.sh/graphql', json={'query': q})
  data = json.loads(response.text)['data']['pages']['edges']

  desc = ''
  for i in [0, 1, 2]:
    d = data[i]['node']
    #hiển thị alt title nếu có
    title = ''
    try:
      title = d["wikidotInfo"]["title"]
      if (title.lower().startswith('scp-')):
        title = d["wikidotInfo"]["title"] + ' - ' + d["alternateTitles"][0]["title"]
      else:
        title = d["alternateTitles"][0]["title"]
    except:
      title = d["wikidotInfo"]["title"]

    url = d['url']
    author = d['wikidotInfo']['createdBy']['name']
    rating = d['wikidotInfo']['rating']

    #mô tả
    desc += "**[{}]({}) (+{})** \n*bởi {}* \n".format(title, url, rating, author)
  
  wikiUrl = "https://scp-wiki.wikidot.com/most-recently-created" if wiki == 0 else "http://scp-vn.wikidot.com/most-recently-created"
  color = discord.Color.blue() if wiki == 0 else 0xFF5733

  embed=discord.Embed(title="Những bài gần đây", url=wikiUrl, description=desc, color=color)

  # #thumbnail
  # thumb = 'https://upload.wikimedia.org/wikipedia/en/0/0a/Logo_of_the_SCP_Foundation.png' if (data["wikidotInfo"]["thumbnailUrl"] is None) else data["wikidotInfo"]["thumbnailUrl"]
  # embed.set_thumbnail(url=thumb)

  await message.channel.send(embed=embed)

  
