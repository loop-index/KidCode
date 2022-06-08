from keep_alive import keep_alive
from searchFn import engSearch, vnSearch, auSearch
from pageFn import lc
import discord
import requests
import random
import time
import json
import os


ethiclim = 3
ethic = True
starttime = 0

client = discord.Client()


#test link availability
# def checkLink(url):
#   response = requests.get(url)
#   return response.status_code < 400


async def embed(ctx):
    embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    await ctx.send(embed=embed)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower()
  
    #title search
    if msg.startswith('.s '):
      item = msg[3:].strip()
      try:
        await engSearch(message, item)
        return
      except:
        await message.channel.send('Không tìm được bài viết chứa từ khóa trên.')
        return


    #vn wiki search
    if msg.startswith('.sv '):
      item = msg[4:].strip()
      try:
        await vnSearch(message, item)
        return
      except:
        await message.channel.send('Không tìm được bài viết chứa từ khóa trên.')
        return

    #author search
    if msg.startswith('.au '):
      author = msg[4:]
      try:
        await auSearch(message, author)
        return
      except:
        await message.channel.send('Không tìm được người dùng.')
        return

    #lc
    if msg.startswith('.new'):
      await lc(message, 0)
      return
    if msg.startswith('.vnew'):
      await lc(message, 1)
      return
      
    #help
    if msg.startswith('.help'):
      helpText = "**.s** (tra wiki En, kèm bản dịch nếu có) \
      \n `.s 001` \
      \n`.s the sculpture` \
      \n \n **.sv** (tra wiki Vn, kèm bản gốc nếu có) \
      \n `.sv 002-vn` \
      \n `.sv rừng bức xạ` \
      \n \n **.au** (tra cứu người dùng wiki) \
      \n `.au flawed` \
      \n \n **.ethics** (đề xuất với Ủy ban Đạo đức) \
      \n `.ethics xóa bot` \
      \n \n **.new** (xem các bài mới từ wiki En) \
      \n \n **.vnew** (xem các bài mới từ wiki Vn) \
      "
      embed=discord.Embed(title="Kid.AIC", url="https://discord.gg/Uwst2qqec3", description=helpText, color=0xE11584)
      embed.set_thumbnail(url='http://scp-wiki.wdfiles.com/local--files/fragment:djkaktus-s-proposal-iii-22/3red.png')

      await message.channel.send(embed=embed)
      return

    #ethics
    global ethic
    if ethic and msg[0:8].lower() == '.ethics ':
      global ethiclim
      vote = msg[8:]
      agree = random.randrange(0, 13)
      disagree = 13 - agree
      verdict = 'THÔNG QUA.' if agree >= 7 else 'TỪ CHỐI.'
      await message.channel.send('Đề xuất: ' + vote + "\nPhiếu thuận: " + str(agree) + '. Phiếu chống: ' + str(disagree) + '. \nQuyết định: ' + verdict)
      ethiclim -= 1
      await message.channel.send('Giới hạn lần bỏ phiếu: ' + str(ethiclim) + ' lần.')
      return

    global starttime
    if ethiclim <= 0 and ethic:
      ethic = False
      starttime = time.time()
      return

    if ethic == False and (time.time() - starttime) > 60:
      ethic = True
      ethiclim = 3

    # #killcount
    # if msg[0:7].lower() == '.kills ':
    #   kills = random.randrange (100000)
    #   await message.channel.send(str(kills) + " mạng Azerbaijan.")
    #   return

    # #comedy
    # if msg.startswith('.comedy'):
    #   joke = ''
    #   rate = ['<:pepedafuq:800747810449260555>', '<:sorrybro:800705043975897130>', '<:classd:800296926247124993>', '<:dogelul:800747812211785759>', '<:lulkek:800747812186095626>']
    #   await message.channel.send(rate[random.randrange(0, 4)])
    #   return


keep_alive()
client.run(os.getenv('TOKEN'))