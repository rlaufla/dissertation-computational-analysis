"""
Korean Text Morphological Analysis using KiwiPiePy
Description: Word frequency analysis for Korean literary texts and journalistic articles
"""

import os
import re
from kiwipiepy import Kiwi
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk import bigrams

# ===================== User Configuration =====================
input_path = r"C:\Users\Desktop\논문\Title.txt"  
output_dir = r"C:\Users\Desktop\논문"
# ==============================================================

# Load text
with open(input_path, 'r', encoding='utf-8') as f:
    raw_text = f.read()

# Clean text (keep only Korean characters and whitespace)
cleaned_text = re.sub(r"[^가-힣\s]", " ", raw_text)

# Initialize KIWI analyzer and add user-defined words
kiwi = Kiwi()
#example of tagging words
user_words = [
    ("무감동", 'NNG'), ("정조", 'NNG'), ("손님", 'NNG'), ("다방마담", 'NNG'),
    ("가정부인", 'NNG'), ("주체성", 'NNG'), ("문경", 'NNP'), ("혁주", 'NNP'),
    ("박첨지", 'NNP'), ("자연스러", 'VA'), ("금례", 'NNP'), ("치옥이", 'NNP'),
    ("튀기", 'NNG'), ("수선", 'NNP'), ("문혁", 'NNP'), ("미망인", 'NNG')
]
for word, tag in user_words:
    kiwi.add_user_word(word, tag=tag, score=0.0)

# Morphological analysis
results = kiwi.analyze(cleaned_text)

# Define target POS tags
주요품사 = ['NNG', 'VV', 'VA', 'MAG']  # Main POS: common noun, verb, adjective, general adverb
용언품사 = ['VV', 'VA']  # Verb POS: verb, adjective

# Extract morphemes (store as list for processing)
tokens_by_line = []
for result in results:
    tokens_by_line.append([(token, tag) for token, tag, _, _ in result[0]])

# ---------------------- 1. Word Frequency ----------------------
counter = Counter()
for token_line in tokens_by_line:
    for token, tag in token_line:
        if tag in 주요품사:
            counter.update([(token, tag)])

# Save: word_frequency.csv
freq_path = os.path.join(output_dir, "word_frequency.csv")
with open(freq_path, "w", encoding='utf-8-sig') as f:
    f.write("형태소,품사,빈도수\n")
    for (token, tag), count in counter.most_common(200):
        if tag in 용언품사:
            token += "다"  # Add ending for verbs/adjectives
        f.write(f"{token},{tag},{count}\n")

print(" 분석 및 저장 완료!")
print(f"- Word Frequency → {freq_path}")
