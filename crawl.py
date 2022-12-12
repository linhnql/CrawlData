import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from os import read

pagesToGet = 52

upperframe = []  
i = 0
for page in range(2, pagesToGet):
    print('processing page :', page)
    url = 'https://vnexpress.net/the-thao-p' + str(page)
    print(url)

    try:
        page = requests.get(url)                            
    
    except Exception as e:                                  
        error_type, error_obj, error_info = sys.exc_info()      
        print ('ERROR FOR LINK:', url)                          
        print (error_type, 'Line:', error_info.tb_lineno)    
        continue                                              
    time.sleep(2)   
    soup = BeautifulSoup(page.text, 'html.parser')
    frame = []
    links = soup.find_all('h2', attrs = {'class':'title-news'})
    print(len(links))

    # filename = "VNExpress.csv"
    # f = open(filename, "w", encoding = 'utf-8')
    # headers = "Link\n"
    # f.write(headers)
    
    for j in links:
        # Statement = j.find("h2", attrs = {'class':'title-news'}).text.strip()
        Link = j.find('a')['href'].strip()
        frame.append((Link))
        page = requests.get(Link)
        bsobj = BeautifulSoup(page.content)
        filename = str(i) + '.txt'
        i = i + 1
        f = open(filename,"w", encoding = 'utf-8')
        for news in bsobj.findAll('h1', {'class': 'title-detail'}):
            f.write(news.text.strip() + '\n')
        for news in bsobj.findAll('p', {'class': 'description'}):
            f.write(news.text.strip() + '\n')
        completed_lines_hash = set()
        for news in bsobj.findAll('p', {'class': 'Normal'}):
            if news not in completed_lines_hash:
                f.write(news.text.strip() + '\n')
                completed_lines_hash.add(news)
        f.close()
# upperframe.extend(frame)
# data = pd.DataFrame(upperframe, columns=['Link'])
# data.head()

# path = 'D:\Visual Code\Python'
# data.to_csv(os.path.join(path, r'VNExpress.csv'))