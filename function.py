from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from nltk_utils import bag_of_words, tokenize
import json
import urllib  as t
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('no-sandbox')
options.add_argument('disable-dev-shm-usage')
driver=webdriver.Chrome(ChromeDriverManager().install(),options=options)
stocklist=[]
l=[]
l2=[]
l3=[]
def news1():
  driver=webdriver.Chrome(ChromeDriverManager().install(),options=options)
  driver.get('https://www.investopedia.com/')
  images = driver.find_elements_by_xpath('//*[@id="card--inset-title_1-0"]/div[1]/div/div/img')
  x=0
  for image in images:
    if(x==3):
      break
    else:
      x=x+1
    src=image.get_attribute('src')
  t.request.urlretrieve(src,"D:/Users/youss/Documents/GitHub/project/static/assets/img/accueil/news1.jpg")
  header=driver.find_elements_by_xpath('//*[@id="card--inset-title_1-0"]/div[2]/span/span')
  news=driver.find_elements_by_xpath('//*[@id="card__summary_1-0"]')
  l.append(header[0])
  l.append(news[0])

  return l
def news2():
  driver=webdriver.Chrome(ChromeDriverManager().install(),options=options)
  driver.get('https://www.investopedia.com/')
  images = driver.find_elements_by_xpath('//*[@id="card--inset-title_1-0-1"]/div[1]/div/div/img')
  x=0
  for image in images:
    if(x==3):
      break
    else:
      x=x+1
    src=image.get_attribute('src')
  t.request.urlretrieve(str(src),"D:/Users/youss/Documents/GitHub/project/static/assets/img/accueil/news2.jpg")
  header2=driver.find_elements_by_xpath('//*[@id="card--inset-title_1-0-1"]/div[2]/span/span')
  news2=driver.find_elements_by_xpath('//*[@id="card__summary_1-0-1"]')
  l2.append(header2[0])
  l2.append(news2[0])
  return l2
def news3():
  driver=webdriver.Chrome(ChromeDriverManager().install(),options=options)
  driver.get('https://www.wsj.com/news/economy?mod=djmc_DGEcon&gclsrc=aw.ds')
  images=driver.find_elements_by_xpath('//*[@id="top-news"]/article/div[1]/a/img')
  x=0
  for image in images:
    if(x==3):
      break
    else:
      x=x+1
    src=image.get_attribute('src')
  t.request.urlretrieve(str(src),"D:/Users/youss/Documents/GitHub/project/static/assets/img/accueil/news3.jpg")
  header3=driver.find_elements_by_xpath('//*[@id="top-news"]/article/div[3]/h2/a/span')
  news3=driver.find_elements_by_xpath('//*[@id="top-news"]/article/p/span[1]')
  l3.append(header3[0])
  l3.append(news3[0])

  return l3
def Gsearch(query,elem):
  listObj = []
  intents=[]
  with open('General_finance.json') as json_data:
      intents = json.load(json_data)
  for i in range(len(intents)):
    if elem == intents[i]['tag']:
      return intents[i]['response']
    elif(i==len(intents)-1):
      count = 0
      from googlesearch import search
      for i in search("site:https://www.investopedia.com "+query,tld='co.in',lang='en',num=5,stop=None,pause=5):
        count += 1
        if 'https://www.investopedia.com/' in i:
                driver=webdriver.Chrome(ChromeDriverManager().install(),options=options)
                driver.get(str(i))
                block1=driver.find_elements_by_xpath('//*[@id="mntl-sc-block_1-0-1"]')
          
                if(block1[0].text):
                  with open('General_finance.json') as json_data:
                    listObj = json.load(json_data)
                  listObj.append({"tag": elem,"response" : block1[0].text})
                  with open("General_finance.json", "w") as out_file:
                    json.dump(listObj, out_file, indent = 6,separators=(',',': '))
                  return block1[0].text
                else:
                  return "I found this on the web: "+str(i)
        elif(count==20):
            return "Sorry!, I didn't Understand"
def stocks(query):
  stocklist.clear()
  driver.get("https://www.google.com/search?q="+query)
  stock=driver.find_elements_by_xpath('//*[@id="knowledge-finance-wholepage__entity-summary"]/div[3]/g-card-section/div/g-card-section/div[2]/div[1]/span[1]/span')
  for s in stock:
    stocklist.append(s.text)
  if(len(stocklist)!=0):
      return stocklist[0]
      




