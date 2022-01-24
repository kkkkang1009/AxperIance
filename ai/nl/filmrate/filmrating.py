from . import filmrate_crawling

from tensorflow.keras import backend
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from konlpy.tag import Komoran, Hannanum, Kkma, Okt
import h5py
import pickle


# make_filmrate_model : 크롤링 및 모델 생성을 수행한다.
def make_filmrate_model(url, keyword, user_id, user_pw):
    dataPath = filmrate_crawling.exportDataFromCrawling(url, keyword, user_id, user_pw)
    print(keyword + " csv : " + dataPath)
    if dataPath != "":
        return True
    else :
        return False


# 손실 함수
def loss_score(y_true, y_pred):
    loss = float(0)
    ln = len(y_true)
    for i in range(ln):
        loss_y = float(0)
        for j in range(10):
            loss_y = loss_y + (j+1)/10 * (y_pred[i][j] - y_true[i][j])
        loss = loss + backend.abs(loss_y)
    loss = loss/float(ln)
    return loss

# 손실 함수 (loss 벡터)
def loss_score_v(y_true, y_pred):
    loss = float(0)
    ln = len(y_true)
    for i in range(ln) :
        loss_y = float(0)
        for j in range(10) :
            loss_y = loss_y + (y_pred[i][j] - y_true[i][j])**2 # 벡터변환 거리 
        if loss_y != 0 :
            loss = loss + (loss_y)**0.5

    if loss != 0 :
        loss = loss/float(ln*10)
    return loss

# loss_score / RMSprop 모델 v01
def sentiment_predict_01(sentence):
    okt = Okt()
    # tokenizer load
    with open('nl/filmrate/tokenizer/filmrate_tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    # model load with custom loss
    model_file = h5py.File('nl/filmrate/model/filmrate_model_01.h5', 'r')
    # model = load_model(model_file, custom_objects={'loss': loss_score(y_true, y_pred)})
    model = load_model(model_file, compile=False)

    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    sentence = okt.morphs(sentence, stem=True)  # 토큰화
    sentence = [word for word in sentence if not word in stopwords]     # 불용어 제거
    encoded = tokenizer.texts_to_sequences([sentence])  # 정수 인코딩
    pad = pad_sequences(encoded, maxlen=100)      # 패딩

    score = 0
    for i in range(10):
      score += model.predict(pad)[0][i] * (i+1)    # 예측
    
    return round(score)/2.0

# loss_score_v / RMSprop 모델 v02
def sentiment_predict_02(sentence):
    okt = Okt()
    # tokenizer load
    with open('nl/filmrate/tokenizer/filmrate_tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    # model load with custom loss
    model_file = h5py.File('nl/filmrate/model/filmrate_model_02.h5', 'r')
    # model = load_model(model_file, custom_objects={'loss': loss_score(y_true, y_pred)})
    model = load_model(model_file, compile=False)

    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    sentence = okt.morphs(sentence, stem=True)  # 토큰화
    sentence = [word for word in sentence if not word in stopwords]     # 불용어 제거
    encoded = tokenizer.texts_to_sequences([sentence])  # 정수 인코딩
    pad = pad_sequences(encoded, maxlen=100)      # 패딩

    score1 = 0
    score2 = 0
    #print(model.predict(pad_new)[0])
    for i in range(10) :
      if score1 < model.predict(pad)[0][i] :
        score1 = model.predict(pad)[0][i]
        score2 = (i+1)/2 # 예측
    
    return score2

# loss_score_v / adam 모델 v03
def sentiment_predict_03(sentence):
    okt = Okt()
    # tokenizer load
    with open('nl/filmrate/tokenizer/filmrate_tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    # model load with custom loss
    model_file = h5py.File('nl/filmrate/model/filmrate_model_03.h5', 'r')
    # model = load_model(model_file, custom_objects={'loss': loss_score(y_true, y_pred)})
    model = load_model(model_file, compile=False)

    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    sentence = okt.morphs(sentence, stem=True)  # 토큰화
    sentence = [word for word in sentence if not word in stopwords]     # 불용어 제거
    encoded = tokenizer.texts_to_sequences([sentence])  # 정수 인코딩
    pad = pad_sequences(encoded, maxlen=100)      # 패딩

    score1 = 0
    score2 = 0
    #print(model.predict(pad_new)[0])
    for i in range(10) :
      if score1 < model.predict(pad)[0][i] :
        score1 = model.predict(pad)[0][i]
        score2 = (i+1)/2 # 예측
    
    return score2


# v04
def sentiment_predict_04(sentence):
    okt = Okt()
    # tokenizer load
    with open('nl/filmrate/tokenizer/filmrate_tokenizer_04.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    # model load with custom loss
    model_file = h5py.File('nl/filmrate/model/filmrate_model_04.h5', 'r')
    # model = load_model(model_file, custom_objects={'loss': loss_score(y_true, y_pred)})
    model = load_model(model_file, compile=False)

    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    sentence = okt.morphs(sentence, stem=True)  # 토큰화
    sentence = [word for word in sentence if not word in stopwords]     # 불용어 제거
    encoded = tokenizer.texts_to_sequences([sentence])  # 정수 인코딩
    pad = pad_sequences(encoded, maxlen=100)      # 패딩

    score1 = model.predict(pad)
    score2 = 0
    #print(model.predict(pad))

    return score.argmax()/2

# get_filmrate_prediction : 예상 평점을 return 한다.
# input : 리뷰 내용
# output : 예상 평점
def get_filmrate_prediction(modelId, content):
    if type(content) is not str:
        return 0.0
    
    if len(content) < 5:      # 최소 길이 제한
        return 0.0

    if modelId == 1:
        return sentiment_predict_01(content)
    elif modelId == 2:
        return sentiment_predict_02(content)
    elif modelId == 3:
        return sentiment_predict_03(content)
    elif modelId == 4:
        return sentiment_predict_04(content)
    
    return 0.0
