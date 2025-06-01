import requests


def send_request(method, url, headers=None, data=None, params=None):
    try:
        # using request library with support for GET, POST, PUT, and DELETE requests
        response = requests.request(method, url, headers=headers, data=data, params=params, timeout=10, verify=True)
        response.raise_for_status() # raising status code
        return response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text
    # watch out! error handling below:
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError:
        return "Connection error. Please check your internet connection."
    except requests.exceptions.Timeout:
        return "Request timed out. Try again later."
    except requests.exceptions.RequestException as err:
        return f"An error occurred: {err}"


def get_request(url, headers=None, params=None):
    return send_request("GET", url, headers=headers, params=params)


def post_request(url, data, headers=None):
    return send_request("POST", url, headers=headers, data=data)


def put_request(url, data, headers=None):
    return send_request("PUT", url, headers=headers, data=data)


def delete_request(url, headers=None):
    return send_request("DELETE", url, headers=headers)


# Example usage
if __name__ == "__main__":
    url = "https://jsonplaceholder.typicode.com/posts/1"
    print("GET request:", get_request(url))

    post_url = "https://jsonplaceholder.typicode.com/posts"
    post_data = {"title": "foo", "body": "bar", "userId": 1}
    headers = {"Content-Type": "application/json"}
    print("POST request:", post_request(post_url, post_data, headers))
