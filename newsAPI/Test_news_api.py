import requests
response = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=1a204d2b61214f0f8c80f6a8b8107cbd")
data = response.json()
print(data)