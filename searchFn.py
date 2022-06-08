from queries import authorQuery, scpEnQuery, scpVnQuery
import discord
import requests
import random
import time
import json

async def engSearch(message, item):
  #find org page
  q = scpEnQuery.replace('flawed', item)
  response = requests.post('https://api.crom.avn.sh/graphql', json={'query': q})
  data = json.loads(response.text)['data']['searchPages'][0]

  #hiển thị alt title nếu có
  title = ''
  try:
    title = data["alternateTitles"][0]["title"]
  except:
    title = data["wikidotInfo"]["title"]

  #mô tả
  desc = "**Tác giả:** " + data['wikidotInfo']["createdBy"]["name"] \
  + "\nĐánh giá: " + str(data['wikidotInfo']['rating'])

  embed=discord.Embed(title=title, url=data['url'], description=desc, color=discord.Color.blue())

  #thumbnail
  thumb = 'https://upload.wikimedia.org/wikipedia/en/0/0a/Logo_of_the_SCP_Foundation.png' if (data["wikidotInfo"]["thumbnailUrl"] is None) else data["wikidotInfo"]["thumbnailUrl"]
  embed.set_thumbnail(url=thumb)

  await message.channel.send(embed=embed)

  #find translation
  try: 
    #tìm bản dịch vn.
    for t in data['translations']:
      if (t['url'].startswith('http://scp-vn.wikidot.com/')):
        title2 = ''
        try:
          title2 = t["alternateTitles"][0]['title']
        except:
          title2 = t["wikidotInfo"]["title"]

        desc = "**Dịch giả:** " + t['wikidotInfo']["createdBy"]["name"] \
  + "\nĐánh giá: " + str(t['wikidotInfo']['rating'])
        
        embed=discord.Embed(title=title2, url=t['url'], description=desc, color=0xFF5733)
  
        embed.set_thumbnail(url=thumb)

        await message.channel.send(embed=embed)
        break
  except:
    print('no translations')



async def vnSearch(message, item):
  #find org page
  q = scpVnQuery.replace('flawed', item)
  response = requests.post('https://api.crom.avn.sh/graphql', json={'query': q})
  data = json.loads(response.text)['data']['searchPages'][0]

  #hiển thị alt title nếu có
  title = ''
  try:
    title = data["alternateTitles"][0]["title"]
  except:
    title = data["wikidotInfo"]["title"]

  #nếu có bản dịch tiếng anh thì hiện dịch giả, không thì là tác giả.
  author = 'Tác giả' if (data['translationOf'] is None) else 'Dịch giả'
  desc = "**" + author + ":** " + data['wikidotInfo']["createdBy"]["name"] \
+ "\nĐánh giá: " + str(data['wikidotInfo']['rating'])

  embed=discord.Embed(title=title, url=data['url'], description=desc, color=0xFF5733)

  #thumbnail
  thumb = 'https://upload.wikimedia.org/wikipedia/en/0/0a/Logo_of_the_SCP_Foundation.png' if (data["wikidotInfo"]["thumbnailUrl"] is None) else data["wikidotInfo"]["thumbnailUrl"]
  embed.set_thumbnail(url=thumb)

  await message.channel.send(embed=embed)

  #find translation
  try: 
    t = data['translationOf']
    #tìm bản gốc tiếng anh
    if (t['url'].startswith('http://scp-wiki.wikidot.com/')):
      title2 = ''
      try:
        title2 = t["alternateTitles"][0]['title']
      except:
        title2 = t["wikidotInfo"]["title"]

      desc = "**Tác giả:** " + t['wikidotInfo']["createdBy"]["name"] \
+ "\nĐánh giá: " + str(t['wikidotInfo']['rating'])

      embed=discord.Embed(title=title2, url=t['url'], description=desc, color=discord.Color.blue())

      embed.set_thumbnail(url=thumb)
      await message.channel.send(embed=embed)
  except:
    print('no translations')


async def auSearch(message, author):
  q = authorQuery.replace('flawed', author)
  r = requests.post('https://api.crom.avn.sh/graphql', json={'query': q})
  data = json.loads(r.text)['data']['searchUsers'][0]

  #nếu có author page thì hiện, không thì hiện wikidot profile. để ý cách/-/+.
  page = ''
  try:
    page = data["authorInfos"][0]["authorPage"]['url']
    title = data["authorInfos"][0]["authorPage"]['wikidotInfo']['title']
  except:
    page = 'http://www.wikidot.com/user:info/' + data['name'].replace(' ', '-')
    title = data['name']

  #page count.
  enCount = data["en"]["pageCount"]
  vnCount = data["vn"]["pageCount"]

  desc = ''

  if enCount > 0:
    desc += "**Wiki EN:** " + str(enCount) + ' trang, đánh giá: ' + str(data['en']['totalRating']) + "\n"

  if vnCount > 0:
    desc += "**Wiki VN:** " + str(vnCount) + ' trang, đánh giá: ' + str(data['vn']['totalRating'])

  embed=discord.Embed(title=title, url=page, description=desc, color=0xFF5733)

  #nghiên cứu thêm ảnh đại diện.
  # print("http://www.wikidot.com/avatar.php?userid=" + str(data["wikidotInfo"]['wikidotId']))
  #"http://www.wikidot.com/avatar.php?userid=" + data["wikidotInfo"]['wikidotId']
  embed.set_author(name=data['name'], url=page, icon_url='https://upload.wikimedia.org/wikipedia/en/0/0a/Logo_of_the_SCP_Foundation.png')
  await message.channel.send(embed=embed)
