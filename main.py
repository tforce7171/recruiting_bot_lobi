import time
from io import BytesIO
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import discord
import os

TOKEN = os.environ['TOKEN']
client = discord.Client()

@client.event
async def on_ready():
    print('logged in')

@client.event
async def on_message(message):
    if message.embeds:
        print(message.embeds)
        for embed in message.embeds:
            if "https://stratsketch.com/" in embed.url and embed.url != "https://stratsketch.com/":
                await message.add_reaction("☑")

@client.event
async def on_message_edit(before, after):
    if after.embeds:
        print(after.embeds)
        for embed in after.embeds:
            if "https://stratsketch.com/" in embed.url and embed.url != "https://stratsketch.com/":
                await after.add_reaction("☑")

@client.event
async def on_reaction_add(reaction, user):
    if reaction.count == 2 and reaction.message.embeds:
        for embed in reaction.message.embeds:
            if "https://stratsketch.com/" in embed.url and embed.url != "https://stratsketch.com/":
                await reaction.message.add_reaction("🆗")
                options = Options()
                options.add_argument('--headless')
                options.add_argument("window-size=1920x1080")
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                options.add_argument("--disable-blink-features=AutomationControlled")
                driver = webdriver.Chrome(options=options)
                driver.implicitly_wait(10)
                driver.get(embed.url)
                # time.sleep(3)
                welcome_window_close_btn = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[2]")
                welcome_window_close_btn.click()
                map_name_element = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/strong[1]")
                print(map_name_element)
                map_name = map_name_element.text.replace(' ', '')
                brief_title_element = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/h2")
                brief_title = brief_title_element.text.replace(' ', '')
                slides = driver.find_elements_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[1]/div/div[2]/div[2]/div")
                for slide in slides:
                    slide_name = slide.text
                    title = map_name + "_" + brief_title + "_" + slide_name + ".png"
                    slide.click()
                    slide_img = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[2]/div")
                    img_binary = slide_img.screenshot_as_png
                    await reaction.message.channel.send(file=discord.File(BytesIO(img_binary), title))
                driver.quit()

client.run(TOKEN)
