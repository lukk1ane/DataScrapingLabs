import requests


def send_get_request():
    url = "http://books.toscrape.com/"

    response = requests.get(url)

    print(f"Status Code: {response.status_code}")

    print("\nResponse Headers:")
    for header, value in response.headers.items():
        print(f"{header}: {value}")


if __name__ == "__main__":
    send_get_request()