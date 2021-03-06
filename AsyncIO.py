"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import requests
import pprint
import os
import re
from bs4 import BeautifulSoup as BSoup
from Spotify_API import search_song
from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize bot and dispatcher
API_TOKEN = os.getenv('TGBOT_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

mode = os.getenv('MODE')


def get_dog_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def get_cat_url():
    contents = requests.get('http://aws.random.cat/meow').json()
    url = contents['file']
    return url


def get_youtube_vid(name):
    search_query = 'https://www.youtube.com/results?search_query=' + name.replace(' ', '+')
    search_content = requests.get(search_query)
    soup = BSoup(search_content.text, 'html.parser')
    all_h3 = soup.find_all('h3')
    search_results = []
    first_href = ''
    for ele in all_h3:
        if 'href' in str(ele):
            search_results.append(ele)
    first_result = str(search_results[0]).split(' ')
    for element in first_result:
        if 'href' in element:
            first_href = element[6:-1]
            break
    first_video_url = 'https://www.youtube.com' + first_href
    return first_video_url


def get_definition(word, lang):
    if lang.lower() == 'en':
        definition_url = 'https://www.wordreference.com/definition/' + str(word)
    elif lang.lower() == 'es':
        definition_url = 'https://www.wordreference.com/definicion/' + str(word)
    else:
        return ['Please provide a valid language']
    content = requests.get(definition_url)
    soup = BSoup(content.text, 'html.parser')
    def_result = soup.find_all('ol')
    if def_result:
        results = []
        no = 1
        for search_result in def_result[:2]:
            results.append(str(no))
            listed_elements = search_result.find_all('li')
            for element in listed_elements[:3]:
                def_string = str(element)
                def_string = re.sub(r'<.*?>|\[.*?\]|:.*', '', def_string)
                results.append(def_string.replace('.', '. \n'))
            results.append('\n')
            no += 1
        results.append('From: ' + str(definition_url))
        return results
    else:
        return ['Word not found']


@dp.message_handler(commands=['cat', 'puss'])
async def cats(message: types.Message):
    url = get_cat_url()
    if 'gif' in url:
        await message.reply_animation(animation=url)
    elif 'mp4' in url or 'webm' in url:
        await message.reply_video(video=url)
    else:
        await message.reply_photo(photo=url)


@dp.message_handler(commands=['dog'])
async def dogs(message: types.Message):
    url = get_dog_url()
    if 'gif' in url:
        await message.reply_animation(animation=url)
    elif 'mp4' in url or 'webm' in url:
        await message.reply_video(video=url)
    else:
        await message.reply_photo(photo=url)


@dp.message_handler(commands=['spotify'])
async def spotify(message: types.Message):
    chatid = message.chat.id
    search = message.get_full_command()[-1]
    song_info, preview = search_song(search)
    pprint.pprint(song_info)
    item = song_info[0]
    md_song = f"[{item['song']['name']}]({item['song']['url']})"
    artists = []
    for artist in item['artists']:
        md_artist = f"[{artist['name']}]({artist['url']})"
        artists.append(md_artist)
    md_artists = ', '.join(artists)
    result = md_song + ' by ' + md_artists
    await bot.send_message(chatid, result, parse_mode='Markdown',)

# @dp.message_handler(commands=['define'])
# async def define(message: types.Message):
#     def_query = message.get_args()
#     all_args = def_query.split(' ')
#     def_word = all_args[0]
#     lang = all_args[-1]
#     definitions = get_definition(def_word, lang)
#     await message.reply('\n'.join(definitions))


@dp.message_handler(commands=['youtube'])
async def youtube(message: types.Message):
    search = message.get_full_command()[-1]
    video_url, name = get_youtube_vid(search)
    await message.reply(video_url)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
