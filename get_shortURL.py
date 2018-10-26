import requests
import json

url = requests.get('http://api.weibo.com/2/short_url/shorten.json?source=2849184197&url_long={query}')
if url.status_code ==200:
    data = json.loads(url.text)
    output = data['urls'][0]['url_short']
    print(output)
else:
    print("error!"+status_code)
