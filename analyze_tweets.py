import arabic_reshaper
from bidi.algorithm import get_display

import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

# ---- Load and Process JSON ----
with open('result.json', encoding='utf-8') as f:
    data = json.load(f)

df = pd.json_normalize(data)
df['parsed_tweetDate'] = pd.to_datetime(df['tweetDate'], format='%a %b %d %H:%M:%S %z %Y', errors='coerce')
# Only keep rows with valid parsed dates (already done earlier)
df['date_only'] = df['parsed_tweetDate'].dt.date
df.to_csv('tweets_arabic.csv', index=False, encoding='utf-8-sig')
print("✅ CSV saved as tweets_arabic.csv")

# ---- Arabic Word Frequency ----
arabic_words = []
for text in df['content'].dropna():
    words = re.findall(r'\b[\u0600-\u06FF]{2,}\b', text)
    arabic_words.extend(words)

top_words = Counter(arabic_words).most_common(10)
print("\n🔠 Top Arabic words:")
for word, freq in top_words:
    print(f"{word}: {freq}")

# Only keep rows with valid parsed dates (already done earlier)
df['date_only'] = df['parsed_tweetDate'].dt.date
timeline = df.groupby('date_only').size()

timeline.plot(kind='line', title='Number of Tweets Over Time', figsize=(10,5))
plt.xlabel('Date')
plt.ylabel('Tweet Count')
plt.grid(True)
plt.tight_layout()
plt.savefig('tweet_frequency_chart.png', dpi=300, bbox_inches='tight')
print("📈 Tweet frequency chart saved as tweet_frequency_chart.png")


# ---- Hashtag Frequency Analysis ----
hashtags = []
for text in df['content'].dropna():
    found = re.findall(r'#\w+', text)
    hashtags.extend(found)

top_hashtags = Counter(hashtags).most_common(20)

tags, freqs = zip(*top_hashtags)

# Reshape Arabic hashtags for proper display (RTL and joined letters)
reshaped_tags = [get_display(arabic_reshaper.reshape(tag)) for tag in tags]

plt.figure(figsize=(12, 6))
plt.barh(reshaped_tags[::-1], freqs[::-1])  # Reverse for highest on top
plt.title('🔝 أكثر الهاشتاقات شيوعاً', fontsize=14)
plt.xlabel('عدد التكرارات')
plt.ylabel('الهاشتاق')
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.savefig('top_hashtags_chart_fixed.png', dpi=300, bbox_inches='tight')
print("📸 Fixed Arabic hashtag chart saved as top_hashtags_chart_fixed.png")

# ---- Hashtag Bar Chart ----
tags, freqs = zip(*top_hashtags)

# Reshape Arabic text for correct RTL display
reshaped_tags = [get_display(arabic_reshaper.reshape(tag)) for tag in tags]

plt.barh(reshaped_tags[::-1], freqs[::-1])

plt.title('🔝 Top 20 Hashtags')
plt.xlabel('Frequency')
plt.ylabel('Hashtag')
plt.tight_layout()
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.savefig('top_hashtags_chart.png', dpi=300, bbox_inches='tight')
print("📸 Chart saved as top_hashtags_chart.png")
from wordcloud import WordCloud

# Join all Arabic words into one string
reshaped_words = [get_display(arabic_reshaper.reshape(w)) for w in arabic_words]
arabic_text = ' '.join(reshaped_words)

# Generate the word cloud
wordcloud = WordCloud(font_path='C:/Windows/Fonts/arial.ttf', width=1000, height=600, background_color='white').generate(arabic_text)

# Save it as an image
wordcloud.to_file('arabic_wordcloud.png')
print("🌥️ Word cloud saved as arabic_wordcloud.png")

# Mentions Analysis
mentions = []
for text in df['content'].dropna():
    mentions.extend(re.findall(r'@\w+', text))

top_mentions = Counter(mentions).most_common(20)
print("\n👥 Top Mentions:")
for mention, count in top_mentions:
    print(f"{mention}: {count}")
pd.DataFrame(top_mentions, columns=["User", "Frequency"]).to_csv("top_mentions.csv", index=False, encoding='utf-8-sig')

#Retweet Analysis
retweets = df['content'].dropna().str.startswith("RT @")
retweet_count = retweets.sum()
total_tweets = len(df)

print(f"\n🔁 Retweets: {retweet_count} / {total_tweets} tweets ({retweet_count/total_tweets:.2%})")

# Hashtag Clustering by Theme
clusters = {
    "grief": ["#صرخات_احلام", "#صرخات", "#صرخة_احلام"],
    "femicide": ["#اوقفوا_قتل_النساء", "#جرائم_قتل_النساء"],
    "support": ["#وقفة_للنساء", "#مع_المعلم"],
    "jordan": ["#الاردن", "#صرخات_الأردنيات"]
}

for theme, tags in clusters.items():
    total = sum([freq for tag, freq in top_hashtags if tag in tags])
    print(f"{theme.title()} Cluster: {total}")
print("\n📌 Top Hashtags (for reference):")
for tag, freq in top_hashtags:
    print(f"{tag}: {freq}")

import matplotlib.pyplot as plt

target_tag = "#صرخات_احلام"

# Filter tweets containing the target hashtag
df['contains_tag'] = df['content'].dropna().apply(lambda x: target_tag in x)
hashtag_timeline = df[df['contains_tag']].groupby('date_only').size()

# Plot
plt.rcParams['font.family'] = 'Arial'
plt.figure(figsize=(10, 4))
plt.plot(hashtag_timeline, marker='o')
for date, count in hashtag_timeline.items():
    plt.text(date, count + 0.5, str(count), ha='center', fontsize=8)

reshaped_title = get_display(arabic_reshaper.reshape(f"تسلسل زمني لـ {target_tag}"))
plt.title(reshaped_title, fontsize=14, fontname='Arial')
plt.xlabel("Date")
plt.ylabel("Mentions")
plt.grid(True)
plt.tight_layout()

# Save the figure
plt.savefig("hashtag_timeline.png", dpi=300, bbox_inches='tight')
print("📉 Hashtag timeline saved as hashtag_timeline.png")
