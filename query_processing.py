import re
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N

def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

# print(correction('speling'))

import requests
from bs4 import BeautifulSoup

link = "http://csivit.com/"

html = requests.get(link).text

"""If you do not want to use requests then you can use the following code below
   with urllib (the snippet above). It should not cause any issue."""
soup = BeautifulSoup(html, "html.parser")

bag_of_words = []

bag_of_words.append(soup.find('p').getText())
bag_of_words.append(soup.find('span').getText())
bag_of_words.append(soup.find('div').getText())
new_bag = []
for i in bag_of_words:
    x = re.sub('\\n',' ',i )
    x = re.sub('\\r',' ',x )
    x = re.sub( '\.','',x )
    x = re.sub( '\,','',x )
    new_bag.append( re.sub('\t','',x ).split(' ') )

final_bag = []
for i in new_bag:
    if( len(i) ):
        for z in i:
            if(len(z)):
                print(z)
                final_bag.append(z)

for i in final_bag:
    i = i.lower()
    if( correction(i) != i ):
        print(i + " corrected to : ", correction(i))