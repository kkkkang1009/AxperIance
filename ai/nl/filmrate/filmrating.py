from . import filmrate_crawling

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Komoran, Hannanum, Kkma, Okt
import h5py

import numpy as np


## make_filmrate_model : 크롤링 및 모델 생성을 수행한다.
def make_filmrate_model(url, keyword, user_id, user_pw) :
    dataPath = filmrate_crawling.exportDataFromCrawling(url, keyword, user_id, user_pw)
    
    print(keyword + " csv : " + dataPath)
    
    if dataPath != "" :
        return True
    else :
        return False

def sentiment_predict(new_sentence):
    okt = Okt()
    tokenizer = Tokenizer()

    model_file = h5py.File('nl/filmrate/filmrate.h5', 'r')
    new_model = load_model(model_file)

    stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = 100) # 패딩
    score = new_model.predict(pad_new)# 예측
    
    return score.argmax()/2


## get_filmrate_prediction : 예상 평점을 return 한다.
## input : 리뷰 내용
## output : 예상 평점
def get_filmrate_prediction(content) :
    if type(content) is not str :
        return 0.0
    
    if len(content) < 10 :      # 최소 길이 제한
        return 0.0       
    # CODE HERE

    prediction_rate = sentiment_predict(content)
    
    return prediction_rate
