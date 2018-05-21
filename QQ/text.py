from os import path
from wordcloud import WordCloud
import jieba

d = path.dirname(__file__)

# Read the whole text.
with open('qq_word.txt', 'r', encoding='utf-8') as f:
    siglist = f.readlines()
    text = "".join(siglist)
    wordlist = jieba.cut(text, cut_all=True)
    word_space_split = " ".join(wordlist)

# Generate a word cloud image
wordcloud = WordCloud().generate(word_space_split)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
#plt.imshow(wordcloud)
#plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_words=65,max_font_size=120,height=600,width=800,font_path="DroidSansFallbackFull.ttf").generate(word_space_split)
plt.figure()
wordcloud.to_file("qq_word.png")
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
