"""
Sentiment Analysis for Dissertation Research
Korean Media Articles: Screen Media vs Non-Screen Media
"""

import os
import json
import pandas as pd
from kiwipiepy import Kiwi
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from itertools import product
import scipy.stats as stats
from scipy.stats import mannwhitneyu, shapiro, levene, ttest_ind
from IPython.display import display

# ===================== Configuration =====================
# Set Korean font for matplotlib
matplotlib.rc('font', family='Malgun Gothic')  # For Windows
# matplotlib.rc('font', family='AppleGothic')  # Uncomment for macOS
matplotlib.rcParams['axes.unicode_minus'] = False

# Directory structure
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# File paths
SENTI_DICT_PATH = os.path.join(DATA_DIR, "SentiWord_info.json")
EXCEL_DATA_PATH = os.path.join(DATA_DIR, "article_coding_data.xlsx")

# Input text files configuration
INPUT_FILES = [
    ("screen_media_articles.txt", "screen_media"),
    ("non_screen_media_articles.txt", "non_screenmedia"),
]

# Type mapping for visualization
TYPE_MAPPING = {
    "screen_media": "articles on screen media",
    "non_screenmedia": "straight articles",
}

# =====================================================


def load_sentiment_dictionary(filepath):
    """Load sentiment dictionary from JSON file."""
    with open(filepath, encoding='utf-8-sig') as f:
        senti_dict = json.load(f)
    return {item['word']: int(item['polarity']) for item in senti_dict}


def extract_sentiment_words(text, kiwi, senti_lookup):
    """Extract sentiment words from text using Kiwi tokenizer."""
    tokens = kiwi.tokenize(text)
    sentiment_words = []
    
    for token in tokens:
        word = token.form
        tag = token.tag
        
        # Add '다' to verbs and adjectives
        if tag.startswith("VV") or tag.startswith("VA"):
            word += "다"
        
        if word in senti_lookup:
            sentiment_words.append({
                "단어": word,
                "극성": senti_lookup[word]
            })
    
    return sentiment_words


def analyze_text_files(input_files, data_dir, senti_lookup, kiwi):
    """Analyze sentiment in text files."""
    records = []
    
    for filename, label in input_files:
        filepath = os.path.join(data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: File not found - {filepath}")
            continue
            
        with open(filepath, encoding='utf-8') as f:
            text = f.read()
        
        sentiment_words = extract_sentiment_words(text, kiwi, senti_lookup)
        
        for item in sentiment_words:
            records.append({
                "파일": filename,
                "유형": label,
                "단어": item["단어"],
                "극성": item["극성"]
            })
    
    return pd.DataFrame(records)


def visualize_average_sentiment(df, type_mapping, output_dir):
    """Create bar plot of average sentiment scores by type."""
    df["type"] = df["유형"].map(type_mapping)
    avg_df = df.groupby("type")["극성"].mean().reset_index()
    
    plt.figure(figsize=(8, 5))
    sns.barplot(data=avg_df, x="type", y="극성", palette="Set2", width=0.5)
    plt.axhline(0, color='gray', linestyle='--')
    plt.title("Average Sentiment Score by Type")
    plt.ylabel("Average Sentiment Score")
    plt.xlabel("Type")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "avg_sentiment_score_by_type.png"), dpi=300)
    plt.show()


def cliffs_delta(lst1, lst2):
    """Calculate Cliff's delta effect size."""
    n1, n2 = len(lst1), len(lst2)
    gt = sum(1 for x, y in product(lst1, lst2) if x > y)
    lt = sum(1 for x, y in product(lst1, lst2) if x < y)
    delta = (gt - lt) / (n1 * n2)
    return delta


def interpret_cliffs_delta(delta):
    """Interpret Cliff's delta effect size."""
    abs_d = abs(delta)
    if abs_d < 0.147:
        return "negligible"
    elif abs_d < 0.33:
        return "small"
    elif abs_d < 0.474:
        return "medium"
    else:
        return "large"


def calculate_effect_size(df):
    """Calculate and interpret Cliff's delta."""
    # Type: 1 or 2 = non-screen, 3 = screen
    group1 = df[df["Type"].isin([1, 2])]["평균감성점수"].dropna().tolist()
    group2 = df[df["Type"] == 3]["평균감성점수"].dropna().tolist()
    
    delta = cliffs_delta(group2, group1)
    effect = interpret_cliffs_delta(delta)
    
    print(f"\nCliff's delta: {delta:.4f}")
    print(f"Effect size: {effect}")
    
    return delta, effect


def classify_media_type(type_value):
    """Classify media type based on Type column."""
    if type_value in [1, 2]:
        return 'non screen media'
    elif type_value == 3:
        return 'screen media'
    else:
        return 'unknown'


def perform_statistical_tests(df, output_dir):
    """Perform comprehensive statistical analysis."""
    # Classify media types
    df['media_type'] = df['Type'].apply(classify_media_type)
    df = df[df['media_type'] != 'unknown']
    
    # Extract groups
    non_screen = df[df['media_type'] == 'non screen media']['평균감성점수'].dropna()
    screen = df[df['media_type'] == 'screen media']['평균감성점수'].dropna()
    
    print(f"\n샘플 수 - non screen: {len(non_screen)}, screen: {len(screen)}")
    
    # Normality tests
    stat_ns, p_ns = shapiro(non_screen)
    stat_s, p_s = shapiro(screen)
    print("\n[정규성 검정 - Shapiro-Wilk]")
    print(f"  non screen media: p = {p_ns:.4f}")
    print(f"  screen media    : p = {p_s:.4f}")
    
    # Homogeneity of variance test
    stat_lev, p_lev = levene(non_screen, screen)
    print("\n[등분산성 검정 - Levene]")
    print(f"  p = {p_lev:.4f}")
    
    # Choose appropriate statistical test
    print("\n[통계적 비교]")
    if len(screen) < 10 or len(non_screen) < 10:
        stat, p = mannwhitneyu(non_screen, screen, alternative='two-sided')
        test_used = "Mann-Whitney U test (small sample)"
    elif p_ns > 0.05 and p_s > 0.05:
        if p_lev > 0.05:
            stat, p = ttest_ind(non_screen, screen, equal_var=True)
            test_used = "Student's t-test"
        else:
            stat, p = ttest_ind(non_screen, screen, equal_var=False)
            test_used = "Welch's t-test"
    else:
        stat, p = mannwhitneyu(non_screen, screen, alternative='two-sided')
        test_used = "Mann-Whitney U test (non-normal)"
    
    print(f"  → {test_used}")
    print(f"  통계량 = {stat:.4f}, p-value = {p:.4f}")
    
    # Summary statistics
    summary_table = df.groupby('media_type')['평균감성점수'].agg(
        N='count', Mean='mean', Median='median', SD='std', Min='min', Max='max'
    ).reset_index().round(4)
    
    display(summary_table)
    summary_table.to_excel(
        os.path.join(output_dir, "sentiment_summary_by_type.xlsx"), 
        index=False
    )
    
    # Visualizations
    create_visualizations(df, non_screen, screen, output_dir)
    
    return summary_table


def create_visualizations(df, non_screen, screen, output_dir):
    """Create boxplot and Q-Q plots."""
    # Boxplot
    plt.figure(figsize=(6, 4))
    sns.boxplot(data=df, x='media_type', y='평균감성점수')
    plt.title("Boxplot: 평균 감성점수 by Media Type")
    plt.xlabel("Media Type")
    plt.ylabel("평균 감성점수")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "boxplot_sentiment.png"), dpi=300)
    plt.show()
    
    # Q-Q Plot (non-screen)
    plt.figure(figsize=(6, 4))
    stats.probplot(non_screen, dist="norm", plot=plt)
    plt.title("Q-Q Plot: Non Screen Media")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "qqplot_non_screen.png"), dpi=300)
    plt.show()
    
    # Q-Q Plot (screen)
    plt.figure(figsize=(6, 4))
    stats.probplot(screen, dist="norm", plot=plt)
    plt.title("Q-Q Plot: Screen Media")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "qqplot_screen.png"), dpi=300)
    plt.show()


def main():
    """Main execution function."""
    print("=" * 60)
    print("Sentiment Analysis for Dissertation Research")
    print("=" * 60)
    
    # Load sentiment dictionary
    print("\n[1] Loading sentiment dictionary...")
    senti_lookup = load_sentiment_dictionary(SENTI_DICT_PATH)
    print(f"    Loaded {len(senti_lookup)} sentiment words")
    
    # Initialise Kiwi tokeniser
    print("\n[2] Initializing Kiwi tokenizer...")
    kiwi = Kiwi()
    
    # Analyse text files
    print("\n[3] Analyzing text files...")
    sent_df = analyze_text_files(INPUT_FILES, DATA_DIR, senti_lookup, kiwi)
    
    if not sent_df.empty:
        sent_df.to_csv(
            os.path.join(OUTPUT_DIR, "감성단어_기록.csv"), 
            index=False, 
            encoding='utf-8-sig'
        )
        print(f"    Extracted {len(sent_df)} sentiment words")
        
        # Visualise average sentiment
        print("\n[4] Creating sentiment visualizations...")
        visualize_average_sentiment(sent_df, TYPE_MAPPING, OUTPUT_DIR)
    
    # Load Excel data for statistical analysis
    print("\n[5] Loading Excel data for statistical analysis...")
    if os.path.exists(EXCEL_DATA_PATH):
        df_excel = pd.read_excel(EXCEL_DATA_PATH)
        
        # Calculate effect size
        print("\n[6] Calculating effect size...")
        calculate_effect_size(df_excel)
        
        # Perform statistical tests
        print("\n[7] Performing statistical tests...")
        perform_statistical_tests(df_excel, OUTPUT_DIR)
        
        print("\n Analysis complete! Results saved to:", OUTPUT_DIR)
    else:
        print(f"\n  Warning: Excel file not found at {EXCEL_DATA_PATH}")
        print("    Skipping statistical analysis.")


if __name__ == "__main__":
    main()
```
