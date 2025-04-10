import json

# Load each JSON file
with open('ahlam.json', encoding='utf-8') as f1:
    ahlam_data = json.load(f1)

with open('israa.json', encoding='utf-8') as f2:
    israa_data = json.load(f2)

# Add a source label to each tweet
for tweet in ahlam_data:
    tweet['source'] = 'ahlam'
    tweet['hashtags_source'] = ['#صرخات_احلام']

for tweet in israa_data:
    tweet['source'] = 'israa'
    tweet['hashtags_source'] = ['#اسراء_غريب', '#كلنا_اسراء_الغريب']

# Merge the datasets
merged_data = ahlam_data + israa_data

# Save to a new JSON file
with open('merged_tweets.json', 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)

print("✅ Merged JSON saved as merged_tweets.json")