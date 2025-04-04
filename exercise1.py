import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Define URL
url = "https://zoomer.ge"

# Send GET request
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Identify the main product container (inspect website to confirm class names)
    main_container = soup.find("div", class_="product-list")  # Adjust class name as needed

    if main_container:
        products = main_container.find_all("div", class_="product-item")  # Adjust class name as needed

        # Extract product details
        product_data = []
        for product in products:
            name = product.find("a", class_="title").text.strip() if product.find("a", class_="title") else "N/A"
            price = product.find("span", class_="price").text.strip() if product.find("span", class_="price") else "N/A"
            link = product.find("a", class_="title")["href"] if product.find("a", class_="title") else "#"

            product_data.append({"name": name, "price": price, "link": f"https://zoomer.ge{link}"})

        # Print extracted data
        for item in product_data:
            print(item)
    else:
        print("Error: Main container not found. The website structure may have changed.")
else:
    print(f"Failed to retrieve website. Status code: {response.status_code}")
