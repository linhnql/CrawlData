import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    result = []

    try:
        for item in reviews:
            review = {
                'product': soup.title.text.replace('Amazon.com: Customer reviews:', '').strip(),
                'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                'rating': float(
                    item.find('i', {'data-hook': 'review-star-rating'}).text.replace(' out of 5 stars', '')),
            }
            contents =  item.find('span', {'data-hook': 'review-body'}).find_all('span')
            # for remove images, video tag
            for content in contents:
                if not content.has_attr('class'):
                    review['content'] = content.text.strip()
                    break
            if review['title'] and 'content' in review and review['content']:
                result.append(review)
    except Exception:
        pass
    
    return result

def main():
    with open('crawl_url.txt', 'r') as url_file:
        for url in url_file:
            for i in range(1, 101):
                crawl_url = url.strip() + str(i)
                soup = get_soup(crawl_url)
                df = pd.DataFrame(get_reviews(soup))
                if not df.empty:
                    df.to_csv('data/reviews.csv', mode='a', sep='|', header=False, index=False)


main()
