import requests


BASE = 'http://127.0.0.1:5000'

# response = requests.post(BASE+'/songs', json={"name": "main hu don", "movie":"Don"})

# response = requests.put(BASE+'/song/3', json={"name":"waka waka", "singer":"shakila", "movie": "private"})

# response = requests.delete(BASE+'/song/5')

# response = requests.get(BASE+'/song/6')

response = requests.get(BASE+'/songslist')

print(response.json())