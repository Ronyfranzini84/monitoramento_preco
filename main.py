from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
from urllib.parse import urljoin


# url of the website to scrape
url ='https://books.toscrape.com/'


# send a GET request to the website
response = requests.get(url, timeout=15)
# set the response encoding to UTF-8
response.encoding = 'utf-8'
# parse the HTML content of the page with BeautifulSoup
soup = BS(response.text, 'html.parser')

# find the first product on the page and extract its name
product = soup.find('article', class_='product_pod')
# extract the product name from the HTML element
product_name = product.find('h3').find('a')['title']
# extract the product price from the HTML element
product_price = product.find('p', class_='price_color').get_text(strip=True)
# convert the product price to a float after removing the currency symbol
product_price = float(product_price.replace('£', ''))
# extract the product availability from the HTML element
product_availability = product.find('p', class_ = 'availability').get_text(strip=True)
# extract the product rating from the HTML element
product_rating = product.find('p', class_='star-rating')
# get the textual representation of the product rating (e.g., 'One', 'Two', etc.)
rating_text = product_rating.get('class')[1]
# map the textual rating to a numerical value
rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
# get the numerical rating from the textual representation
rating_number = rating_map[rating_text]
# find all products on the page and store them in a list
products = soup.find_all('article', class_='product_pod')
# create an empty list to store product information
product_list = []
# iterate over all products and print their names and prices
for product in products:
    product_name = product.find('h3').find('a').get('title')
    product_price = product.find('p', class_='price_color').get_text(strip=True)
    product_price = float(product_price.replace('£', ''))
    product_availability = product.find('p', class_ = 'availability').get_text(strip=True)
    product_rating = product.find('p', class_='star-rating')
    rating_text = product_rating.get('class')[1]
    rating_number = rating_map[rating_text]
    # adds the name, the price, the availability, and the rating to the empty list
    product_list.append({'name': product_name, 
                        'price': product_price,
                        'availability': product_availability,
                        'rating': rating_number})
# function to extract product information from a list of products
def extract_products(products):
    product_list = []
    for product in products:
        product_name = product.find('h3').find('a').get('title')
        product_price = product.find('p', class_='price_color').get_text(strip=True)
        product_price = float(product_price.replace('£', ''))
        product_availability = product.find('p', class_ = 'availability').get_text(strip=True)
        product_rating = product.find('p', class_='star-rating')
        rating_text = product_rating.get('class')[1]
        rating_number = rating_map[rating_text]
        # adds the name, the price, the availability, and the rating to the empty list
        product_list.append({'name': product_name, 
                            'price': product_price,
                            'availability': product_availability,
                            'rating': rating_number,
        })
    return product_list
# extract product information from the second page
extract_product = extract_products(products)

df_products = pd.DataFrame(extract_product)

next_page = soup.find('li', class_='next')
next_page_url = next_page.find('a').get('href')
full_url = urljoin(url, next_page_url)

response_page2 = requests.get(full_url, timeout=15)

soup_page2 = BS(response_page2.content, 'html.parser')

product_page2 = soup_page2.find_all('article', class_='product_pod')

extracted_page2 = extract_products(product_page2)

df_page2 = pd.DataFrame(extracted_page2)

df_all_products = pd.concat(
    [df_products, df_page2],
    ignore_index=True
)

current_url = "https://books.toscrape.com/"
page_number = 1
all_products = []

while page_number:
    response = requests.get(current_url, timeout=15)
    response.raise_for_status()

    soup = BS(response.content, 'html.parser')

    products =soup.find_all(
        'article', class_= 'product_pod'
    )

    extracted_products = extract_products(products)
    all_products.extend(extracted_products)

    print(f"Page {page_number}: {len(extracted_products)} products")

    next_page = soup.find('li', class_='next')

    if next_page is None:
        break

    next_page_url = next_page.find('a').get('href')
    current_url = urljoin(current_url, next_page_url)

    page_number += 1

df_all_products = pd.DataFrame(all_products)

print(f"Total pages: {page_number}")
print(f"Total products: {len(df_all_products)}")
print(df_all_products.shape)

file_name = 'books_catalog.xlsx'

df_all_products.to_excel(file_name, index=False)

print(f'File saved as {file_name}')



