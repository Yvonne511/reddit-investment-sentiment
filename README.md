# reddit-investment-sentiment

## Team Members:

[Yvonne Wu](https://github.com/Yvonne511): yw4142@nyu.edu 

[Huixuan Wang](https://github.com/hxwang-463): hw2544@nyu.edu

Chidire Prasanna: pkc4609@nyu.edu

## Project Objectives:

Inspired by GameStop Short Squeeze, our team wants to analyze the ability to use Reddit to predict stock prices. 

**Several questions we might be looking into:**

1. can Reddit predict stock price of all <span style="color:red">industries</span>

    A: We did not have enough time to process enough companies to generate an answer

2. which <span style="color:red">fluctuations</span> on Reddit indicate a change

    A: Based on our results, 2 days of data is enough to predict the general trend of the following market trend given no significant event happening afterward

3. is there a <span style="color:red">time lapse</span> between Reddit sentiment change and the actual stock price change

    A: not much based on the causality result from different lag value

## Data Collection:

**There are several metrics we considered for data collection:**

1. which <span style="color:red">subreddit</span> to look into (or the whole platform)
2. how to <span style="color:red">filter</span> relevant comments

There are a few files that we use to collect data:
1. data-mining-submission.py: it gets all the reddit posts with keywords or from which subreddit
2. get_comments.py: it gets all the sub comments from each reddit posts using PRAW

## Sentiment Analysis:

check file: sentiment_analysis.py

## Causality Analysis

It uses files from data/final/..

1. Correlation Analysis:
https://www.kaggle.com/code/yvonnewu511/lstm-reddit
This is from Kaggle notebook. The colab notebook is also downloaded called correlation analysis. The dataframe gme can be changed to other companies's.

2. Causality Analysis:
check file: granger_causality.py
It can be used to process other companies' granger causality by changing the line:

`file_path = os.path.join(cwd, 'data', 'final', 'gme_wsb.csv')`

## Modeling:


