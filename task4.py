import requests

base_url = "http://books.toscrape.com/"

print("Performing GET request...")
response_get = requests.get(base_url)
print(f"GET Status Code: {response_get.status_code}")
print(f"GET Response Headers: {response_get.headers}\n")

print("Performing HEAD request...")
response_head = requests.head(base_url)
print(f"HEAD Status Code: {response_head.status_code}")
print(f"HEAD Response Headers: {response_head.headers}\n")

print("Performing POST request...")
post_data = {"example_key": "example_value"}
response_post = requests.post(base_url, data=post_data)
print(f"POST Status Code: {response_post.status_code}")
print(f"POST Response Headers: {response_post.headers}")
print(f"POST Response Body: {response_post.text[:500]}...\n")
