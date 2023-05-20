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
1. `data-mining-submission.py`: it gets all the reddit posts with keywords or from which subreddit. Change parameters in line 39, 40, 41.
2. `get_comments.py`: it gets all the sub comments from each reddit posts using PRAW. Change parameters in line 98. For PRAW, you have to apply for token on reddit website, and add `client_id, client_secret, and user_agent` in `config.toml`.

## Sentiment Analysis:

run ```data_cleaning.py``` followed by the company folder name, like ```data_cleaning.py netflix```. This will get data from ```./data/netflix/```, do sentiment analysis, and generate results in ```./data/cleaned_data/netflix/```. We run this step in Greene with GPU.  
We also use ```data_visual.py``` to combine stock price and sentiment score together, in ```data/final/```.

## Causality Analysis

It uses files from `data/final/.`.

1. Correlation Analysis:
https://www.kaggle.com/code/yvonnewu511/lstm-reddit
This is from Kaggle notebook. The colab notebook is also downloaded called correlation analysis. The dataframe gme can be changed to other companies's.

2. Causality Analysis:
check file: granger_causality.py
It can be used to process other companies' granger causality by changing the line:`file_path = os.path.join(cwd, 'data', 'final', 'gme_wsb.csv')`

## Modeling:
all data in folder ```./data_sentiment_score```
1. pre processing  
We will do some data prepare for LSTM in folder ```./data_sentiment_score```. There is a folder for each company as the company's name. I will use Netflix as example. ```./netflix/netflix``` contain all the sentiment score from Netflix, ```./netflix/NFLX.csv``` contain all stock price from Netflix. Then we used ```./preprocessing_sentiment.py``` and ```./preprocessing_stock.py``` to pre-process the data, and generated ```./netflix/netflix.csv``` and ```./netflix/price.csv```. These two file will be sent to our LSTM model. The other 3 companies is generated as the same.  
2. model trining
We used a Jupyter Notebook to train our model, named ```./lstm.ipynb```. ```x1,y1``` corrisponding to data of Gamestop; ```x2,y2``` is Netflix; ```x3,y3``` is Nvidia, ```x4,y4``` is Tesla. Then we combine different set of companies as training set using ```np.concatenate()```. 
3. evaluation
In ```./lstm.ipynb```, we use ```calculate_mape()``` to calculate the MAPE; we used ```predict_period()``` to predict the movement of the stock price. For example, if we train the data using ```x1/2/3 and y1/2/3```, we can run ```predict_period(x4[-200:], y4[-200:])``` to predict the last 200 time period of Tesla's stock price.


