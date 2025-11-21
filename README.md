# Computational Text Analysis for PhD Dissertation

Python scripts for computational analysis of Korean newspaper articles, including TF-IDF analysis, sentiment scoring, and statistical testing.

> **Note:** Initial code drafts were generated with ChatGPT (OpenAI, 2025) and subsequently reviewed, modified, and validated by the author.

---

## Repository Contents

This repository includes:
- **Morphological analysis** using KiwiPiePy tokeniser
- **TF-IDF analysis**: Temporal comparison across six historical periods (1970–2023)
- **Sentiment analysis**: Token-level scoring with custom Korean lexicon
- **Statistical tests**: Shapiro-Wilk, Levene's test, Mann-Whitney U
- **Visualisation**: Heatmaps, boxplots, Q-Q plots

---

## Project Structure
```
dissertation-computational-analysis/
├── data/
│   └── README.md                           # Data availability notice
├── dictionaries/
│   └── SentiWord_info.json                 # Modified Korean sentiment lexicon
├── scripts/
│   ├── TF-IDF.py                           # Period-based TF-IDF & z-score heatmap
│   ├── Term frequency.py                   # Term frequency analysis
│   └── sentiment_analysis_with_kiwi.py     # Token-level sentiment scoring
├── README.md
└── requirements.txt
```

---

## Key Methodologies

### 1. TF-IDF Temporal Analysis
- Extracts top-20 terms across entire corpus
- Calculates mean TF-IDF per period
- Z-score normalisation for comparison
- Generates heatmap visualisation

### 2. Sentiment Analysis
- Token-based (not word count) for accuracy
- Custom Korean sentiment dictionary (modified from KNU lexicon)
- Outputs: sentiment ratio, positive/negative counts, average sentiment score

### 3. Statistical Testing
- **Normality test**: Shapiro-Wilk
- **Variance homogeneity**: Levene's test
- **Group comparison**: Mann-Whitney U (used due to small sample size)

---

## Dependencies

**Python version:** 3.10.9

Install required packages:
```bash
pip install -r requirements.txt
```

**Key packages:**
- kiwipiepy==0.15.1 (Korean morphological analyser)
- scikit-learn>=1.3.0 (TF-IDF vectorisation)
- pandas>=2.0.0
- scipy>=1.11.0
- matplotlib>=3.7.0
- seaborn>=0.12.0

---

## Usage

### TF-IDF Temporal Analysis
```bash
python scripts/tfidf_temporal_analysis.py
```
**Outputs:**
- `period_top20_meanTFIDF.csv`
- `period_top20_mean_zscore.csv`
- `heatmap_mean_tfidf_zscore.png`

### Morphological Frequency Analysis
```bash
python scripts/morphological_frequency.py
```
**Outputs:**
- `word_frequency.csv`

### Sentiment Analysis
```bash
python scripts/sentiment_analysis_with_kiwi.py
```
**Outputs:**
- Excel file with columns: File | Type | Total Tokens | Sentiment Words | Avg Score | Positive Count | Negative Count | Sentiment Ratio (%)
- 'avg_sentiment_score_by_type.png'
  
### Statistical Analysis
```bash
python scripts/sentiment_statistical_analysis.py
```
**Outputs:**
- Statistical test results
- Boxplot and Q-Q plots
- Summary Excel file

**Note:** Korean font (Malgun Gothic for Windows) required for proper visualisation.

---

## Data & Acknowledgments

### Data Confidentiality
Raw newspaper articles are not included due to confidentiality requirements. Sample data structure is provided in `data/README.md`.

### Sentiment Dictionary
**Base lexicon:** KNU Korean Sentiment Lexicon (군산대학교 한국어 감성사전)
- Source: [KnuSentiLex GitHub](https://github.com/park1200656/KnuSentiLex)
- **Modifications by author:**
  - Domain-specific vocabulary added
  - Polarity scores adjusted for media context
  - Modified version: `dictionaries/SentiWord_info.json`

### AI Tool Usage
Initial Python scripts were drafted using ChatGPT (OpenAI, 2025) for:
- TF-IDF and z-score calculation logic
- Statistical test implementation
- Visualisation code

All generated code was thoroughly reviewed, modified, and validated by the author. The author takes full responsibility for the final codebase.

---

## Citation

If using this code, please cite:

> Kim, Youlim. (2025). *Computational Text Analysis for PhD Dissertation* [Computer software]. GitHub. https://github.com/rlaufla/dissertation-computational-analysis

**References:**

OpenAI. (2025). *ChatGPT* (GPT-4) [Large language model]. https://chat.openai.com/

---

## License

MIT License

---

## Contact

Youlim Kim  
Email: Youlim.Kim@ruhr-uni-bochum.de
