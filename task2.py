import requests
from bs4 import BeautifulSoup
import json 


URL = "https://www.swoop.ge/category/2/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print(f"Requesting data from: {URL}")
try:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status() 
    print("Request successful.")

    soup = BeautifulSoup(response.content, 'html.parser')

    deal_containers = soup.find_all('div', class_='syndicated-deal')
    print(f"Found {len(deal_containers)} deal containers.")

    if not deal_containers:
        print("No deal containers found. The website structure might have changed.")
        exit()

    scraped_data = []

   
    for container in deal_containers[:5]:
        deal_info = {}

      
        title_div = container.find('div', class_='deal-voucher-title')
        title_element = title_div.find('p') if title_div else None
        deal_info['title'] = title_element.text.strip() if title_element else 'N/A'
        
        price_div = container.find('div', class_='deal-voucher-price')
        
        price_element = price_div.select_one('span.discounted-price') if price_div else None
        deal_info['price'] = price_element.text.strip() if price_element else 'N/A'
       
        price_div_for_sibling = container.find('div', class_='deal-voucher-price')
        location_div = None
        if price_div_for_sibling:
            
             location_div = price_div_for_sibling.find_next_sibling('div', class_='merchant-address-box')
            
             if not location_div:
                  location_div = price_div_for_sibling.find_next_sibling('div') 

        location_element = location_div.find('p') if location_div else None 
        deal_info['location'] = location_element.text.strip() if location_element else 'N/A'
       
        info_container = container.find('div', class_='deal-voucher-info')
        image_container = None
        if info_container:
          
            image_container = info_container.find_previous_sibling('div', class_='deal-voucher-img') 
            if not image_container:
                 image_container = info_container.find_previous_sibling('div') 

       
        link_element = container.select_one('a[href]')
        deal_url = link_element['href'] if link_element and link_element.has_attr('href') else 'N/A'
      
        if deal_url.startswith('/'):
            deal_url = f"https://www.swoop.ge{deal_url}"
        deal_info['url'] = deal_url
        

        
        original_price_element = container.select_one('span.old-price')
        deal_info['original_price'] = original_price_element.text.strip() if original_price_element else 'N/A'
        
        scraped_data.append(deal_info)

except requests.exceptions.RequestException as e:
    print(f"Error during requests to {URL}: {e}")
except Exception as e:
    print(f"An error occurred: {e}")


if scraped_data:
    print("\n--- Scraped Data (First 5 Deals) ---")

    print(json.dumps(scraped_data, indent=4, ensure_ascii=False))
else:
    print("\nNo data was scraped.")