import json
with open("tweets_merged.json", encoding="utf-8") as f:
    data = json.load(f)
print(len(data))