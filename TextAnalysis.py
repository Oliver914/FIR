'''
In order to facilitate text analysis, we separately extract ['title'] from the table.
'''

import re
import nltk
from collections import Counter
from wordcloud import WordCloud # using python 3.7
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


NEGWORDS = ["not", "no", "none", "neither", "never", "nobody", "n't", 'nor']
STOPWORDS = ["an", "a", "the", "or", "and", "thou", "must", "that", "this", "self", "unless", "behind", "for", "which",
             "whose", "can", "else", "some", "will", "so", "from", "to", "by", "within", "of", "upon", "th", "with",
             "it"] + NEGWORDS


def _remove_stopwords(txt):
    """Delete from txt all words contained in STOPWORDS."""
    words = txt.split()
    # words = txt.split(" ")
    for i, word in enumerate(words):
        if word in STOPWORDS:
            words[i] = " "
    return (" ".join(words))

with open('SNP Election - title.csv', 'r', encoding='utf-8') as news_read:
    # read(n) method will put n characters into a string
    news_string = news_read.read()

news_split = str.split(news_string, sep=',')
print('----------------------------------------------------------------------')
print(news_split)
len(news_split)
doc_out = []
for k in news_split:
    cleantextprep = str(k)
        # Regex cleaning
    expression = "[^a-zA-Z ]"  # keep only letters, numbers and whitespace
    cleantextCAP = re.sub(expression, '', cleantextprep)  # apply regex
    cleantext = cleantextCAP.lower()  # lower case
    cleantext = _remove_stopwords(cleantext)
    bound = ''.join(cleantext)
    doc_out.append(bound)       # a list of sentences
print('----------------------------------------------------------------------')
print(doc_out)
print('----------------------------------------------------------------------')
print(news_split)
print('----------------------------------------------------------------------')
# print clean text
for line in doc_out:
    print(line)

# Read in BL lexicon
# Negative lexicon
ndct = ''
with open('bl_negative.csv', 'r', encoding='utf-8', errors='ignore') as infile:
    for line in infile:
        ndct = ndct + line

# create a list of negative words
ndct = ndct.split('\n')
# ndct = [entry for entry in ndct]
len(ndct)

# Positive lexicon
pdct = ''
with open('bl_positive.csv', 'r', encoding='utf-8', errors='ignore') as infile:
    for line in infile:
        pdct = pdct + line

pdct = pdct.split('\n')
# pdct = [entry for entry in pdct]
len(pdct)

# Count words being collected in the lexicon

def decompose_word(doc):
    txt = []
    for word in doc:
        txt.extend(word.split())
    return txt


# decompose a list of sentences into words by self-defined function
tokens = decompose_word(doc_out)
# decompose a list of sentences into words from NLTK module
tokens_nltk = nltk.word_tokenize(str(doc_out))


# generate wordcloud
comment_words = ' '
for token in tokens:
    comment_words = comment_words + token + ' '

print(comment_words)

wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                min_font_size = 10).generate(comment_words)

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig("wordcloud.png",format='png',dpi=200)
plt.show()


def wordcount(words, dct):
    counting = Counter(words)
    count = []
    for key, value in counting.items():
        if key in dct:
            count.append([key, value])
    return count

# Number of words in article
nwords = len(tokens)

nwc = wordcount(tokens, ndct)   # wordcount(text,lexicon)

pwc = wordcount(tokens, pdct)

# Total number of positive/negative words
ntot, ptot = 0, 0
for i in range(len(nwc)):
    ntot += nwc[i][1]

for i in range(len(pwc)):
    ptot += pwc[i][1]


# Print results
print('----------------------------------------------------------------------')
print('Positive words:')
for i in range(len(pwc)):
    print(str(pwc[i][0]) + ': ' + str(pwc[i][1]))
print('Total number of positive words: ' + str(ptot))
print('\n')
print('Percentage of positive words: ' + str(round(ptot / nwords, 4)) + '%')
print('----------------------------------------------------------------------')
print('Negative words:')
for i in range(len(nwc)):
    print(str(nwc[i][0]) + ': ' + str(nwc[i][1]))
print('Total number of negative words: ' + str(ntot))
print('\n')
print('Percentage of negative words: ' + str(round(ntot / nwords, 4)) + '%')
print('----------------------------------------------------------------------')