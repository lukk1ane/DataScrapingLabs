import requests

def demonstrate_http_methods(url):
    """Demonstrate different HTTP methods and their responses."""
    print(f"Demonstrating HTTP methods for: {url}\n")
    
    # GET request
    print("=== GET Request ===")
    get_response = requests.get(url)
    print(f"Status Code: {get_response.status_code}")
    print(f"Response Size: {len(get_response.content)} bytes")
    print(f"Content Type: {get_response.headers.get('Content-Type')}")
    print("\n")
    
    # HEAD request - similar to GET but without response body
    print("=== HEAD Request ===")
    head_response = requests.head(url)
    print(f"Status Code: {head_response.status_code}")
    print("Headers received:")
    for key, value in head_response.headers.items():
        print(f"  {key}: {value}")
    print("\n")
    
   
    print("=== OPTIONS Request ===")
    try:
        options_response = requests.options(url)
        print(f"Status Code: {options_response.status_code}")
        print(f"Allowed Methods: {options_response.headers.get('Allow', 'Not specified')}")
        print("\n")
    except Exception as e:
        print(f"OPTIONS request failed: {e}\n")
    

    print("=== POST Request ===")
    try:
        post_data = {"test": "data"}
        post_response = requests.post(url, data=post_data)
        print(f"Status Code: {post_response.status_code}")
        print(f"Response Size: {len(post_response.content)} bytes")
        print("\n")
    except Exception as e:
        print(f"POST request failed: {e}\n")

def main():
    url = "http://books.toscrape.com/"
    demonstrate_http_methods(url)

if __name__ == "__main__":
    main()