# 교육 AI 챗봇 구축 시행착오 노트

> AI Hub 데이터 기반 RAG 챗봇 (LangChain + ChromaDB + Streamlit) 구축 과정에서 마주치는 문제와 해결법 정리

---

## 목차

1. [환경 세팅](#1-환경-세팅)
2. [AI Hub 데이터 다운로드 및 전처리](#2-ai-hub-데이터-다운로드-및-전처리)
3. [임베딩 모델 및 벡터 DB](#3-임베딩-모델-및-벡터-db)
4. [RAG 파이프라인](#4-rag-파이프라인)
5. [Streamlit UI](#5-streamlit-ui)
6. [공유 및 배포](#6-공유-및-배포)
7. [자주 쓰는 명령어 모음](#7-자주-쓰는-명령어-모음)

---

## 1. 환경 세팅

### 패키지 버전 충돌

**증상:** `pip install` 후 `ImportError` 또는 `AttributeError` 발생

**원인:** LangChain은 버전 간 API 변경이 잦아 최신 버전과 호환 안 되는 경우 많음

**해결:**
```bash
# 검증된 버전 고정 설치
pip install -r requirements.txt
```

```
# requirements.txt (검증된 버전)
langchain==0.2.16
langchain-community==0.2.16
langchain-openai==0.1.23
chromadb==0.5.5
sentence-transformers==3.0.1
streamlit==1.38.0
openai==1.45.0
python-dotenv==1.0.1
```

---

### `langchain_community` 모듈 못 찾는 오류

**증상:**
```
ModuleNotFoundError: No module named 'langchain_community'
```

**해결:**
```bash
pip install langchain-community
```

> `langchain`과 `langchain-community`는 별도 패키지. 둘 다 설치 필요.

---

### Windows에서 가상환경 활성화 오류

**증상:**
```
'source'은(는) 내부 또는 외부 명령이 아닙니다
```

**해결:**
```bash
# Windows (PowerShell / CMD)
chatbot_env\Scripts\activate

# Mac / Linux
source chatbot_env/bin/activate
```

---

### `.env` 파일 API 키 인식 안 됨

**증상:** `openai.AuthenticationError` 또는 `API key not found`

**체크리스트:**
- `.env` 파일이 `app.py`와 같은 폴더에 있는지 확인
- `load_dotenv()`를 코드 최상단에서 호출했는지 확인
- `.env` 파일 내용 형식 확인 (등호 앞뒤 공백 없어야 함)

```
# 올바른 형식
OPENAI_API_KEY=sk-xxxxxxxxxxxx

# 잘못된 형식 (공백 있으면 안 됨)
OPENAI_API_KEY = sk-xxxxxxxxxxxx
```

---

## 2. AI Hub 데이터 다운로드 및 전처리

### 데이터 신청 후 승인 지연

- 승인까지 보통 **1~3 영업일** 소요
- 기관 소속 없어도 개인 신청 가능
- 승인 메일 오면 마이페이지 → 데이터 신청 현황에서 다운로드

---

### JSON 키 이름이 다른 경우

**증상:** 전처리 후 청크가 전부 빈 문자열로 나옴

**원인:** 데이터셋마다 JSON 키 이름이 다름

**해결:** 데이터 받으면 먼저 구조 확인

```python
import json

with open("./dataset/train/train_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 첫 번째 항목 키 확인
print(data[0].keys())
print(data[0])
```

출력 예시에 따라 `preprocess.py`의 키 이름 수정:
```python
# 예: 키가 "ques", "ans"인 경우
question = item.get("ques", "")
answer = item.get("ans", "")
```

---

### JSON이 리스트가 아닌 딕셔너리인 경우

**증상:** `TypeError: argument of type 'dict' is not iterable`

**원인:** 일부 AI Hub 데이터셋은 최상위가 딕셔너리

```python
# 최상위 구조 먼저 확인
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(type(data))  # dict인지 list인지 확인
if isinstance(data, dict):
    print(data.keys())  # 어떤 키 아래에 실제 데이터가 있는지 확인
```

```python
# 딕셔너리인 경우 접근 예시
data = data["data"]  # 또는 data["utterances"] 등 실제 키로 변경
```

---

### 한글 인코딩 오류

**증상:** `UnicodeDecodeError: 'cp949' codec can't decode`

**해결:**
```python
# encoding="utf-8" 명시 필수
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 그래도 안 되면
with open(file_path, "r", encoding="utf-8-sig") as f:  # BOM 있는 경우
    data = json.load(f)
```

---

## 3. 임베딩 모델 및 벡터 DB

### 임베딩 모델 최초 다운로드 시간이 오래 걸림

- `jhgan/ko-sroberta-multitask` 모델 크기: 약 **400MB**
- 최초 1회만 다운로드, 이후 캐시에서 로드
- 캐시 위치: `~/.cache/huggingface/hub/`

---

### ChromaDB 저장 오류 (sqlite 버전 문제)

**증상:**
```
RuntimeError: Your system has an unsupported version of sqlite3.
```

**해결:**
```bash
pip install pysqlite3-binary

# 코드 최상단에 추가 (build_vectordb.py, rag_pipeline.py)
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
```

---

### 벡터 DB 재구축 없이 데이터 추가하는 법

```python
# 기존 DB에 새 데이터 추가 (처음부터 재구축 안 해도 됨)
existing_db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
existing_db.add_documents(new_split_chunks)
print("추가 완료")
```

---

### 검색 결과 품질이 낮을 때

**원인:** `k` 값(검색 문서 수) 또는 청크 크기 조정 필요

```python
# 검색 문서 수 조정 (기본 3 → 5로 늘리기)
retriever = vectordb.as_retriever(
    search_type="mmr",           # similarity 대신 mmr 사용 (다양성 확보)
    search_kwargs={"k": 5, "fetch_k": 10}
)
```

```python
# 청크 크기 조정 (교육 Q&A는 500~800이 적당)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,    # 너무 작으면 문맥 손실, 너무 크면 관련없는 내용 포함
    chunk_overlap=100  # overlap을 늘리면 문맥 연결성 향상
)
```

---

## 4. RAG 파이프라인

### `ConversationBufferMemory` deprecation 경고

**증상:**
```
LangChainDeprecationWarning: Please see the migration guide...
```

**해결 (LangChain 최신 버전):**
```python
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# 또는 경고 무시하고 기존 방식 유지 (기능은 동작함)
import warnings
warnings.filterwarnings("ignore")
```

---

### 답변이 "모르겠습니다"만 반복될 때

**원인:** 벡터 DB에 관련 데이터가 없거나 검색 결과가 너무 부정확함

**디버깅 방법:**
```python
# 검색 결과 직접 확인
docs = retriever.get_relevant_documents("광합성이란?")
for doc in docs:
    print(doc.page_content)
    print("---")
```

**해결:**
- 프롬프트에서 "모른다고 말하라" 조건 완화
- 데이터 전처리 품질 개선 (청크 구조 확인)
- 임베딩 모델을 더 강력한 것으로 교체

---

### OpenAI API 비용 절감 팁

```python
# gpt-4o-mini 사용 (gpt-4o 대비 약 10분의 1 비용)
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3)

# 무료 대안: Ollama + 로컬 모델
# ollama pull mistral
from langchain_community.llms import Ollama
llm = Ollama(model="mistral")
```

---

## 5. Streamlit UI

### 챗봇 실행 시 매번 모델 재로드 문제

**증상:** 질문할 때마다 임베딩 모델을 다시 불러와 느림

**원인:** `@st.cache_resource` 누락

**해결:**
```python
@st.cache_resource  # 이 데코레이터 필수
def load_chain():
    return create_rag_chain()

chain = load_chain()
```

---

### 대화 기록이 새로고침 시 사라지는 문제

**원인:** Streamlit은 매 인터랙션마다 스크립트를 재실행함

**해결 (이미 적용됨):**
```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```

> `st.session_state`를 사용하면 새로고침 없이 대화 유지 가능. 브라우저 새로고침 시에는 초기화됨.

---

### 포트 충돌 오류

**증상:**
```
OSError: [Errno 98] Address already in use
```

**해결:**
```bash
# 다른 포트로 실행
streamlit run app.py --server.port 8502
```

---

## 6. 공유 및 배포

### GitHub 업로드 시 주의사항

`.gitignore` 필수 항목:
```
.env                # API 키 절대 공개 금지
dataset/            # AI Hub 데이터 (라이선스 문제)
chroma_db/          # 용량 큼 (수백 MB 가능)
__pycache__/
*.pyc
chatbot_env/
```

---

### 공유받은 사람이 실행하는 방법

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. .env 파일 생성 후 본인 API 키 입력
echo "OPENAI_API_KEY=sk-..." > .env

# 3. 벡터 DB 구축 (chroma_db/ 폴더가 없는 경우)
python build_vectordb.py

# 4. 실행
streamlit run app.py
```

> `chroma_db/` 폴더를 같이 전달하면 3번 단계 생략 가능.

---

### Streamlit Cloud 무료 배포

1. GitHub에 코드 push (`.env`, `dataset/`, `chroma_db/` 제외)
2. [share.streamlit.io](https://share.streamlit.io) 접속 → GitHub 연동
3. **Secrets 설정** (`.env` 대신 사용):
   - Settings → Secrets → 아래 내용 입력
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
4. `chroma_db/`는 배포 시 매번 재구축되므로, 소규모 데이터에만 적합

---

## 7. 자주 쓰는 명령어 모음

```bash
# 가상환경 생성 및 활성화
python -m venv chatbot_env
chatbot_env\Scripts\activate        # Windows
source chatbot_env/bin/activate     # Mac/Linux

# 패키지 설치
pip install -r requirements.txt

# 벡터 DB 구축 (최초 1회 또는 데이터 변경 시)
python build_vectordb.py

# 챗봇 실행
streamlit run app.py

# 다른 포트로 실행
streamlit run app.py --server.port 8502

# 설치된 패키지 목록 저장
pip freeze > requirements.txt

# ChromaDB 초기화 (처음부터 다시 구축할 때)
rm -rf chroma_db/   # Mac/Linux
rmdir /s chroma_db  # Windows
```

---

## 참고 링크

- [AI Hub](https://aihub.or.kr) — 데이터셋 신청
- [LangChain 공식 문서](https://python.langchain.com/docs/)
- [ChromaDB 공식 문서](https://docs.trychroma.com/)
- [HuggingFace ko-sroberta](https://huggingface.co/jhgan/ko-sroberta-multitask) — 한국어 임베딩 모델
- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [OpenAI API 키 발급](https://platform.openai.com/api-keys)

---

*마지막 업데이트: 2024년 — 교육 AI 챗봇 구축 프로젝트*
