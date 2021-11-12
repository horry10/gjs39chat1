# 2021 인공지능 학습용 데이터 활용 해커톤 경진대회

### 1. 프로젝트 주제

- 코로나 민원 처리 채팅 시스템

### 2. 프로젝트 개요
- 코로나 확진자가 날이 갈수록 점차 증가함에 따라 질병관리본부에 코로나 관련 민원이 폭주하고 있어 코로나 관련 상담을 받을 수 있는 대기 시간이 상당히 길다.  
따라서 고객들과의 상담 시간을 단축하여 대기 시간을 줄이고 정확한 정보를 빠르게 전달하기 위해 온라인 채팅 서비스를 구축하고자 한다.

### 3. 프로젝트 진행 과정
- [데이터](https://aihub.or.kr/aidata/30716) 다운로드 및 정제
- TransFormer 모델과 Kobert Tokenizer 를 활용하여 정제한 데이터 학습
- Telegram 채팅봇과 연동

### 4. 실행 방법
1. `chatbot` 폴더 다운로드
2. 아래 두 링크를 통해 TransFormer Model 가중치 파일을 다운로드 한 뒤 chatbot 폴더에 추가합니다
- [1](https://drive.google.com/file/d/142VbKzrEcCTrgnwNVk0SvPuGHG5tgscY/view?usp=sharing)

- [2](https://drive.google.com/file/d/1f-cnsS9frDE2OnC1jyXJJZJz8afMM7vn/view?usp=sharing)

3. `pip install -r requirements.txt` 필요한 라이브러리를 설치합니다 (tensorflow 반드시 2.7.0 또는 2.6.2 버전 사용)
4. `transformer_model.py` 파일을 실행시켜 잘 작동하는지 확인합니다.
5. `telegram_chatbot.py` 를 실행합니다.
    - `telegram_chatbot.py` 의 `token`, `id`  직접 발급받아 사용하여야 합니다.  아래 링크를 참조해주세요
    
    [`발급방법`](https://gabrielkim.tistory.com/entry/Telegram-Bot-Token-%EB%B0%8F-Chat-Id-%EC%96%BB%EA%B8%B0)  
      
      
### _참고자료_
- [TransFormer Model](https://wikidocs.net/89786)
- [Kobert Tokenizer](https://github.com/monologg/KoBERT-Transformers)

