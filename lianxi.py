import string
import random
from PIL import Image, ImageFont, ImageDraw
from bs4 import BeautifulSoup
import os
import re
from collections import Counter
import mysql.connector
#import matplotlib as mpl
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg


def gencode(nums, lens):
    pool = list(string.ascii_uppercase)
    result = {}
    while len(result)<nums:
        key = ''
        for i in range(lens):
            key += random.choice(pool)
        if key not in result:
            result[key] = 1
    return [key for key in result]
print(gencode(4,5))



font = ImageFont.truetype('cambriaz.ttf', 54)
img = Image.open(r'1.jpg')
draw = ImageDraw.Draw(img)
draw.text((img.size[0]*0.85, img.size[1]*0.05), u'5', font=font, fill=(255,0,0))
img.save('2.jpg')
#lena = mpimg.imread('2.jpg')
#plt.imshow(lena)
#plt.show()

def code2sql():
    db = mysql.connector.connect(user='',password='',host='',database='')
    cur = db.cursor()
    cur.execute("drop table if exists acode")
    cur.execute('create acode(id int primary key, code varchar(20))')
    for key in gencode(4,5):
        cur.execute("insert into acode(code) values('%s')",key)
    cur.close()

	
def countwd(filename):
    txt = open(filename,'r').read().lower()
    pat = r'[a-zA-Z-]+'
    words = re.findall(pat,txt)
    return(Counter(words).items())
	
def changephsize(oldir,weight,height,newdir):
    photos = os.listdir(oldir)
    for photo in photos:
        phpath = os.path.join(oldir,photo)
        if os.path.isfile(phpath):
            im = Image.open(phpath)
            newim = im.resize((weight,height))
            newpath = os.path.join(newdir,photo)
            newim.save(newpath)
			
def countcode(path):
    common_lines = 0
    code_lines = 0
    for root, dirs,files in os.walk(path):
        for file in files:
            file_abs_path = os.path.join(root,file)
            if os.path.splitext(file_abs_path)[1] == '.py':
                with open(file_abs_path,'rb') as f:
                    while True:
                        line = f.readline().decode('utf-8')
                        if not line:
                            break
                        elif line.strip().startswith('#'):
                            common_lines += 1
                        elif line.strip().startswith("'''") or line.strip().startswith('"""'):
                            common_lines += 1
                            if line.count('"""') ==1 or line.count("'''") ==1:
                                while True:
                                    line = fp.readline()
                                    common_lines += 1
                                    if ("'''" in line) or ('"""' in line):
                                        break
                        elif line.strip():
                            code_lines += 1
    return common_lines, code_lines
	
def partext(path):
    text = []
    url = []
    with open(path,encoding='utf-8') as f:
        html = BeautifulSoup(f, 'html.parser')
        content = html.select('.content p')
        for p in content:
            text.append(p.text)
        href = html.find_all('a')
        for each in href:  
            if str(each.get('href'))[:4]=='http':  
                url.append(each.get('href'))
        return text,url
		