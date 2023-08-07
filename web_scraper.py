import requests
from bs4 import BeautifulSoup
import csv

resp = requests.get('https://www.trustpilot.com/review/www.rbcroyalbank.com?languages=all&sort=recency')

html_code = resp.text

with open('resp.html', 'w') as f:
    f.write(resp.text)
    
soup = BeautifulSoup(html_code, "lxml")

def get_num_reviews(soup):
    """
    Extract the number of reviews.
    
        Parameters:
            soup: A BeautifulSoup instance containing data pulling from the url
            
        Returns:
            The page number of the last page in integer.
    """
    links = soup.find_all('p')
    for link in links:
        if link.get('data-reviews-count-typography'):
            num_reviews = link.contents[0]
    return num_reviews

num_reviews = get_num_reviews(soup)
print('Total number reviews are', num_reviews)

def get_last_page_num(soup):
    """
    Extract the number of the last page.
    
        Parameters:
            soup: A BeautifulSoup instance containing data pulling from the url
            
        Returns:
            The number of the last page in integer.
    """
    links = soup.find_all('a')
    for link in links:
        if link.get('name') == 'pagination-button-last':
            return int(link.contents[0].contents[0])

num_pages = get_last_page_num(soup)

companyName = ['RBC' for i in range(int(num_reviews))]
datePublished = []
ratingValue = []
reviewBody = []

first_page = 'https://www.trustpilot.com/review/www.rbcroyalbank.com'
all_language = '?languages=all'
page_extension = '&page='
sort = '&sort=recency'

for i in range(num_pages):
    if i == 0:
        resp = requests.get(first_page + all_language + sort)
        html_code = resp.text
        
        links = soup.find_all('div', class_="styles_reviewContent__0Q2Tg")
        for link in links: 
            datePublished.append(link.contents[-1].contents[3])
            if len(link.contents) == 3:
                reviewBody.append(link.contents[1].contents[0])
            else:
                reviewBody.append(link.contents[0].contents[0].contents[0])
        
        
        rating_links = soup.find_all('div', class_="styles_reviewHeader__iU9Px")
        for link in rating_links:
            ratingValue.append(int(link.get('data-service-review-rating')))
                
    else:
        resp = requests.get(first_page + all_language + page_extension + str(i+1) + sort)
        html_code = resp.text
        soup = BeautifulSoup(html_code, "lxml")
        
        links = soup.find_all('div', class_="styles_reviewContent__0Q2Tg")
        
        for link in links:
            datePublished.append(link.contents[-1].contents[3])
            if len(link.contents) == 3:
                reviewBody.append(link.contents[1].contents[0])
            else:
                reviewBody.append(link.contents[0].contents[0].contents[0])
        
        
        rating_links = soup.find_all('div', class_="styles_reviewHeader__iU9Px")
        for link in rating_links:
            ratingValue.append(int(link.get('data-service-review-rating')))
            
f = open("reviews.csv", 'w')

writer = csv.writer(f, delimiter=',')

writer.writerow(["companyName", "datePublished", "ratingValue", "reviewBody"])

for i in range(len(datePublished)):
    writer.writerow([companyName[i], datePublished[i], ratingValue[i], reviewBody[i]])

f.close()

