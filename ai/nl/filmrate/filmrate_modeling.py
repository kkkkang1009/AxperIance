import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from konlpy.tag import Komoran, Hannanum, Kkma, Okt
from tqdm import tqdm
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


data = pd.read_csv('/nl/filmrate/data/filmrate_data_ansi.csv', encoding='cp949')
text = data.iloc[:,[0,3,5]]
random.seed(1)

text['text'] = text['text'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
text['rate'] = text['rate'].replace('보고싶어요', np.nan, regex=True ) # 공백은 Null 값으로 변경
text['rate'] = text['rate'].replace('보는중', np.nan, regex=True ) # 공백은 Null 값으로 변경

text = text.dropna(how = 'any') # Null 값이 존재하는 행 제거

train_data = text[:2000]
test_data = text[2000:]

print("Train: {} | Val: {}".format(len(train_data), len(test_data)))

komoran = Komoran()
hannanum = Hannanum()
kkma = Kkma()
okt = Okt()
tokenizer = Tokenizer()

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

X_train = []
for sentence in tqdm(train_data['text']):
    tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
    stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
    X_train.append(stopwords_removed_sentence)

X_test = []
for sentence in tqdm(test_data['text']):
    tokenized_sentence = okt.morphs(sentence, stem=True) # 토큰화
    stopwords_removed_sentence = [word for word in tokenized_sentence if not word in stopwords] # 불용어 제거
    X_test.append(stopwords_removed_sentence)

tokenizer.fit_on_texts(X_train)

threshold = 3
total_cnt = len(tokenizer.word_index) # 단어의 수
rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

# 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # 단어의 등장 빈도수가 threshold보다 작으면
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value

print('단어 집합(vocabulary)의 크기 :',total_cnt)
print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)

vocab_size = total_cnt - rare_cnt + 1
print('단어 집합의 크기 :',vocab_size)

tokenizer = Tokenizer(vocab_size) # 빈도수 2 이하인 단어는 제거
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

y_train = np.array(pd.to_numeric(train_data['rate'])*2)
y_test = np.array(pd.to_numeric(test_data['rate'])*2)

y_train.astype(np.int);
y_test.astype(np.int);

y_train.shape

# print('리뷰의 최대 길이 :',max(len(l) for l in X_train))
# print('리뷰의 평균 길이 :',sum(map(len, X_train))/len(X_train))
# plt.hist([len(s) for s in X_train], bins=50)
# plt.xlabel('length of samples')
# plt.ylabel('number of samples')
# plt.show()

def below_threshold_len(max_len, nested_list):
    cnt = 0
    for s in nested_list:
        if(len(s) <= max_len):
            cnt = cnt + 1
    # print('전체 샘플 중 길이가 %s 이하인 샘플의 비율: %s'%(max_len, (cnt / len(nested_list))*100))

max_len = 100
below_threshold_len(max_len, X_train)

# 전체 데이터의 길이는 30으로 맞춘다.
X_train = pad_sequences(X_train, maxlen = max_len)
X_test = pad_sequences(X_test, maxlen = max_len)

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

print("X_val:", X_train.shape)  # X_val: (10000, 784)
print("Y_val:", y_train.shape)  # Y_val: (10000, 28, 28, 10)

y_train[1]

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
mc = ModelCheckpoint('best_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

model = Sequential()
model.add(Embedding(vocab_size, 100))
model.add(LSTM(128))
model.add(Dense(64, activation='softmax'))
model.add(Dense(11, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['acc'])
history = model.fit(X_train, y_train, epochs=100, callbacks=[es, mc], batch_size=64, validation_split=0.2)

def sentiment_predict(new_sentence):
    new_sentence = okt.morphs(new_sentence, stem=True) # 토큰화
    new_sentence = [word for word in new_sentence if not word in stopwords] # 불용어 제거
    encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
    pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
    score = model.predict(pad_new)# 예측

sentiment_predict('와 개쩐다 정말 세계관 최강자들의 영화다')
sentiment_predict('이 영화 핵노잼 ㅠㅠ')
sentiment_predict('감독 뭐하는 놈이냐?')