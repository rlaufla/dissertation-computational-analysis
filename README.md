# dissertation-computational-analysis
Python script for computations analysis of Korean newspaper articles (Phd dissertation)


This repository contains all Python scripts and supporting files used in the sentiment analysis and lexical feature comparison of Korean media articles, including period-based TF-IDF and z-score heatmap visualization, as part of a PhD dissertation.

> **Note:** Initial code drafts were generated with ChatGPT (OpenAI 2025), then reviewed, modified, and validated manually by the author.

---

## AI Tool Usage Declaration

Initial Python scripts for the following tasks were drafted using ChatGPT (OpenAI 2025):
- Sentiment dictionary mapping and token-level analysis logic
- TF-IDF and z-score calculation across time periods
- Statistical test implementation (Shapiro-Wilk, Mann-Whitney U, Levene's Test)
- Data visualization code (boxplots, Q-Q plots, heatmaps)

**Important:** All generated code was:
- Thoroughly reviewed by the author for accuracy and appropriateness
- Modified to fit the specific research requirements
- Validated against expected outputs
- Tested with actual dissertation data

The author takes full responsibility for the final codebase and any errors therein.

## Acknowledgments


**Sentiment Dictionary:**
- **KNU Korean Sentiment Lexicon** (군산대학교 한국어 감성사전)
  - Source: [KnuSentiLex GitHub Repository](https://github.com/park1200656/KnuSentiLex)
  - The dictionary contains sentiment scores for Korean words and emoticons
  - Used for token-level sentiment analysis in this research
  - Some vocabulary and their scores added or edited by the author
     **Modifications by author:**
    - Additional domain-specific vocabulary added
    - Some polarity scores adjusted based on media context
    - Modified version used for token-level sentiment analysis in this research
  - Note: Modified lexicon is available in this repository as `dictionaries/SentiWord_Dict.txt`

    
## Project Structure
```
dissertation-sentiment-analysis/
├── data/
│   ├── 기사코딩20250603_감성분석포함.xlsx   # Raw input articles (Not publicly shared)
│   └── dummy_sample_data.xlsx              # Dummy version with same structure
├── dictionaries/
│   └── SentiWord_info.json                 # Custom Korean sentiment dictionary (JSON format)
├── scripts/
│   ├── sentiment_analysis_with_kiwi.py     # Token-level sentiment scoring
│   ├── media_type_classifier.py            # Maps Type 1+2 → Non-screen, Type 3 → Screen
│   ├── tfidf_zscore_by_period.py           # Mean TF-IDF and z-score heatmap analysis
│   ├── stats_tests_and_plots.py            # Mann–Whitney U, Shapiro–Wilk, boxplot, Q-Q
│   └── export_summary_excel.py             # Summary (file, type, token stats) to Excel
├── results/
│   ├── sentiment_summary_table.xlsx        # Final summary output
│   └── 시기별_top20_meanzscore.csv          # Mean z-score values for top 20 terms by period
├── README.md
└── requirements.txt
```

---

## Main Analyses Included

- **Sentiment Scoring** using a custom Korean lexicon and KIWI tokenizer
- **TF-IDF Analysis**: Mean TF-IDF and z-score normalization across periods
- **Token-based analysis** (not word count) for more accurate ratio calculations
- **Media Type Classification**: 
  - Type 1 + 2 → Non-screen media
  - Type 3 → Screen media
- **Statistical Tests**:
  - Shapiro–Wilk (normality)
  - Levene's Test (homogeneity of variance)
  - Mann–Whitney U Test (used due to small N)
- **Visualization**:
  - Boxplots
  - Q-Q plots
  - Heatmaps (mean TF-IDF z-scores)

---

## Output Variables (Exported to Excel)

| 파일 | 유형 | 전체토큰수 | 감성단어수 | 평균감정점수 | 긍정단어수 | 부정단어수 | 감성단어비율 (%) |
|------|------|------------|------------|---------------|-------------|-------------|-------------------|

---

##  Dependencies

**Python version:** 3.10.9 (Anaconda distribution)

Install with pip:
```bash
pip install -r requirements.txt
```

**Required packages**:
- pandas (>=2.0.0)
- kiwipiepy (==0.15.1)
- scipy (>=1.11.0)
- matplotlib (>=3.7.0)
- seaborn (>=0.12.0)
- openpyxl (>=3.1.0)
- scikit-learn (>=1.3.0)

## Usage

Run the complete analysis pipeline:
```bash
python scripts/full_sentiment_analysis.py
```

This will execute all three main analyses:
1. Sentiment word extraction and visualisation
2. Cliff's Delta effect size calculation
3. Statistical tests (normality, homogeneity, group comparison) and plots

All results will be saved to the `results/` directory.

## How to Cite

If using this code in your research, please cite as:

> Kim, Youlim. (2025). *Dissertation Sentiment & Lexical Analysis* [Computer software]. GitHub. https://github.com/rlaufla/dissertation-sentiment-analysis

Initial scripts were drafted using ChatGPT (OpenAI 2025) and later refined by the author.

**References:**

OpenAI. (2025). *ChatGPT* (GPT-4) [Large language model]. https://chat.openai.com/

---

## Data Confidentiality Note

Due to data confidentiality requirements, raw article texts are not included in this repository. A dummy file with matching structure is provided for demonstration purposes.

---

## License

MIT License - Feel free to use with proper attribution.

---

## 📧 Contact

For questions regarding this code or methodology, please contact: Youlim.Kim@ruhr-uni-bochum.de
