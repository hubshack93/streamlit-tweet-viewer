import json
with open("israa_tweets.json", encoding="utf-8") as f:
    data = json.load(f)
print(len(data))