import requests


def demonstrate_http_methods():
    url = "http://books.toscrape.com/"

    print("Demonstrating different HTTP methods:")

    print("\n=== GET Request ===")
    get_response = requests.get(url)
    print(f"Status Code: {get_response.status_code}")
    print(f"Response Size: {len(get_response.content)} bytes")
    print(f"Content Type: {get_response.headers.get('Content-Type')}")

    print("\n=== HEAD Request ===")
    head_response = requests.head(url)
    print(f"Status Code: {head_response.status_code}")
    print(f"Response Size: No content retrieved (HEAD request)")
    print("Headers:")
    for key, value in head_response.headers.items():
        print(f"  {key}: {value}")

    print("\n=== POST Request ===")
    try:
        post_response = requests.post(url, data={"test": "data"})
        print(f"Status Code: {post_response.status_code}")
        if post_response.status_code == 405:
            print("POST Method Not Allowed (as expected for a static site)")
        else:
            print(f"Response Size: {len(post_response.content)} bytes")
    except Exception as e:
        print(f"POST request failed: {e}")

    print("\n=== OPTIONS Request ===")
    try:
        options_response = requests.options(url)
        print(f"Status Code: {options_response.status_code}")
        print(f"Allowed Methods: {options_response.headers.get('Allow', 'Not specified')}")
    except Exception as e:
        print(f"OPTIONS request failed: {e}")


if __name__ == "__main__":
    demonstrate_http_methods()