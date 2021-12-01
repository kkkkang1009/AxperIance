## make_filmrate_model : 크롤링 및 모델 생성을 수행한다.
def make_filmrate_model(url, user_id, user_pw) :
    return False

## get_filmrate_prediction : 예상 평점을 return 한다.
## input : 리뷰 내용
## output : 예상 평점
def get_filmrate_prediction(content) :
    if type(content) is not str :
        return 0.0
    
    if len(content) < 10 :      # 최소 길이 제한
        return 0.0
        
    # CODE HERE
    prediction_rate = 5.0
    
    return prediction_rate
