"""
TF-IDF Analysis for Dissertation
Description: Temporal TF-IDF analysis of Korean news articles using KiwiPiePy morphological analyser
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from kiwipiepy import Kiwi

# ========== Configuration ==========
BASE_DIR = "./data"  
INPUT_FILE = "article_data.xlsx"  
SHEET_NAME = "text1"  

file_path = os.path.join(BASE_DIR, INPUT_FILE)
OUTPUT_DIR = "./output"  # Output directory for results

# Analysis parameters
EXCLUDE_WORDS = {"미혼모", "하다"}  # Words to exclude from analysis
TOP_N = 20  # Number of top words to analyse

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========== Data Loading ==========
print("Loading data...")
df = pd.read_excel(file_path, sheet_name=SHEET_NAME)

# ========== Period Classification ==========
def get_period(year):
    """Classify year into historical periods"""
    if 1970 <= year <= 1979: return "1. 1970–1979"
    elif 1980 <= year <= 1987: return "2. 1980–1987"
    elif 1988 <= year <= 1995: return "3. 1988–1995"
    elif 1996 <= year <= 2007: return "4. 1996–2007"
    elif 2008 <= year <= 2014: return "5. 2008–2014"
    elif 2015 <= year <= 2023: return "6. 2015–2023"
    else: return "Unknown"

df["Period"] = df["Year"].apply(get_period)

# ========== Morphological Analysis ==========
print("Initializing morphological analyzer...")
kiwi = Kiwi()

def tokenize_text(text):
    """
    Tokenise Korean text using KiwiPiePy
    Extracts nouns (NNG) and verbs (VV), converting verbs to dictionary form
    """
    tokens = kiwi.tokenize(text)
    return [
        (token.form + "다" if token.tag.startswith("VV") else token.form)
        for token in tokens
        if token.tag.startswith(("NNG", "VV")) and
           ((token.form + "다") if token.tag.startswith("VV") else token.form) not in EXCLUDE_WORDS
    ]

# ========== Period-wise Document Tokenisation ==========
print("Tokenizing documents by period...")
period_docs = defaultdict(list)
for _, row in df.iterrows():
    period = row["Period"]
    tokens = tokenize_text(str(row["Content"]))  # Change "Content" to your column name
    period_docs[period].append(" ".join(tokens))

# ========== Total TF-IDF Calculation → Extract Top N Words ==========
print(f"Calculating TF-IDF and extracting top {TOP_N} words...")
all_docs = []
for docs in period_docs.values():
    all_docs.extend(docs)

vectorizer = TfidfVectorizer()
X_all = vectorizer.fit_transform(all_docs)
df_all = pd.DataFrame(X_all.toarray(), columns=vectorizer.get_feature_names_out())
top_words = df_all.sum().sort_values(ascending=False).head(TOP_N).index.tolist()

print(f"Top {TOP_N} words identified: {top_words}")

# ========== Analysis 1: Sum TF-IDF by Period ==========
print("\n=== Analysis 1: Sum TF-IDF ===")
period_sum = {}
for period, docs in period_docs.items():
    X = vectorizer.transform(docs)
    df_tfidf = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    
    # Fill missing words with 0
    for word in top_words:
        if word not in df_tfidf.columns:
            df_tfidf[word] = 0.0
    
    # Calculate sum TF-IDF
    sum_tfidf = df_tfidf[top_words].sum(axis=0)
    period_sum[period] = sum_tfidf

sum_tfidf_df = pd.DataFrame(period_sum).T[top_words]

# Z-score normalisation for sum TF-IDF
mean_val = sum_tfidf_df.values.mean()
std_val = sum_tfidf_df.values.std()
z_score_sum_df = (sum_tfidf_df - mean_val) / std_val

# Save sum TF-IDF results
sum_out = os.path.join(OUTPUT_DIR, "period_top20_sumTFIDF.csv")
z_sum_out = os.path.join(OUTPUT_DIR, "period_top20_sum_zscore.csv")

sum_tfidf_df.to_csv(sum_out, encoding="utf-8-sig")
z_score_sum_df.to_csv(z_sum_out, encoding="utf-8-sig")
print(f" Sum TF-IDF saved: {sum_out}")
print(f" Sum Z-score saved: {z_sum_out}")

# ========== Analysis 2: Mean TF-IDF by Period ==========
print("\n=== Analysis 2: Mean TF-IDF ===")
period_mean = {}
for period, docs in period_docs.items():
    X = vectorizer.transform(docs)
    df_tfidf = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
    
    # Fill missing words with 0
    for word in top_words:
        if word not in df_tfidf.columns:
            df_tfidf[word] = 0.0
    
    # Calculate mean TF-IDF
    mean_tfidf = df_tfidf[top_words].mean(axis=0)
    period_mean[period] = mean_tfidf

mean_tfidf_df = pd.DataFrame(period_mean).T[top_words]

# Z-score normalisation for mean TF-IDF
mean_val_mean = mean_tfidf_df.values.mean()
std_val_mean = mean_tfidf_df.values.std()
z_score_mean_df = (mean_tfidf_df - mean_val_mean) / std_val_mean

# Save mean TF-IDF results
mean_out = os.path.join(OUTPUT_DIR, "period_top20_meanTFIDF.csv")
z_mean_out = os.path.join(OUTPUT_DIR, "period_top20_mean_zscore.csv")

mean_tfidf_df.to_csv(mean_out, encoding="utf-8-sig")
z_score_mean_df.to_csv(z_mean_out, encoding="utf-8-sig")
print(f" Mean TF-IDF saved: {mean_out}")
print(f" Mean Z-score saved: {z_mean_out}")

# ========== Visualisation: Heatmap ==========
print("\nGenerating heatmap...")

# Font settings for Korean text (adjust based on your OS)
plt.rcParams["font.family"] = "Malgun Gothic"  # Windows: Malgun Gothic, MacOS: AppleGothic
plt.rcParams["axes.unicode_minus"] = False

# Heatmap for mean TF-IDF z-scores
plt.figure(figsize=(14, 8))
sns.heatmap(z_score_mean_df, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Z-score'})
plt.title("Temporal Analysis: Top 20 Words Mean TF-IDF Z-scores", fontsize=16, pad=20)
plt.xlabel("Words", fontsize=12)
plt.ylabel("Period", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save heatmap
heatmap_path = os.path.join(OUTPUT_DIR, "heatmap_mean_tfidf_zscore.png")
plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
print(f" Heatmap saved: {heatmap_path}")
plt.show()

print("\n=== Analysis Complete ===")
