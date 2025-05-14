

# 🧳 AI-based Travel Information Recommendation System

When you enter a travel-related question,  
this smart travel assistant automatically classifies the query, retrieves relevant information,  
and provides a response with both text and images.  
It is powered by Google Gemini API, Pexels API, and Sentence Transformers.

---

## 🚀 Key Features

- ✅ **Automatic Question Classification**: Classifies into `contents`, `historical`, or `preparation` using Gemini API
- 🔍 **Document Retrieval**: Uses Sentence Transformers embedding + FAISS for similarity search
- 🧠 **Answer Generation**: Generates natural language responses based on retrieved documents using Gemini
- 🗂 **Structured Message per Category**:
  - `contents`: JSON output with Place, F&B, and Activity fields
  - `preparation`: JSON output with Clothes and ETC fields
  - `historical`: Timeline-based explanation + list of major historical events
- 🖼️ **Auto Image Linking**: Fetches relevant images for each item using Pexels API (handled in FastAPI)
- 💬 **Summary Generation**: Gemini generates a friendly 1-3 sentence summary (`summary`)
- 🔒 **Secure API Key Management**: Managed using `.env` file

---

## 📄 Output Format by Category

### 📍 `contents`
```json
{
  "Place": [{ "name": "...", "information": "..." }, ...],
  "F&B": [{ "name": "...", "information": "..." }, ...],
  "Activity": [{ "name": "...", "information": "..." }, ...]
}
```

### 📍 `preparation`
```json
{
  "Clothes": [
    {
      "name": "Light Outerwear",
      "information": "Perfect for spring and autumn trips with wide temperature ranges, it helps maintain body temperature during outdoor activities."
    },
    {
      "name": "Comfortable Sneakers",
      "information": "Reduces foot fatigue during long walks and supports safe travel."
    }
  ],
  "ETC": [
    {
      "name": "Portable Battery",
      "information": "Keeps your smartphone charged during long outings."
    },
    {
      "name": "Multi Adapter",
      "information": "A must-have for international travel to support various plug types."
    }
  ]
}

```

### 📍 `historical`
```json
{
  "Edo Period": {
    "Period Description": "During the Edo period, Osaka developed into Japan’s largest commercial center and was called the 'Kitchen of the Nation.'",
    "Major Events": [
      {
        "name": "Construction of Osaka Castle",
        "description": "Built by Toyotomi Hideyoshi, this iconic structure remains a key tourist attraction in Osaka."
      },
      {
        "name": "Commercial Boom",
        "description": "Osaka prospered as a rice distribution hub and became the economic center of Japan."
      }
    ]
  },
  "Meiji Period": {
    "Period Description": "After the Meiji Restoration, Osaka rapidly grew into an industrial and financial hub.",
    "Major Events": [
      {
        "name": "Modern Industrialization",
        "description": "Osaka transformed into a leading industrial city with factories and railroads."
      },
      {
        "name": "Urban Planning Introduction",
        "description": "With the implementation of modern urban infrastructure, Osaka became a central city of development."
      }
    ]
  }
}

```

## 📦 Technologies Used

| Area | Technology |
|------|------|
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2` |
| Conversational AI | Google `Gemini API` (generativeai) |
| Image Search | `Pexels API` |
| Vector Search | `FAISS` |
| Environment Variable Management | `python-dotenv` |
| Others | `requests`, `numpy`, `os` etc. |

---


## 🔑 Required API Keys

### 1. 🔮 Google Gemini API
- Generate your API key at: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) 
- Add it to your `.env` file as `GEMINI_API_KEY=your_api_key`

### 2. 📷 Pexels API
- Sign up and get your API key at: [https://www.pexels.com/api/](https://www.pexels.com/api/) 
- Add it to your `.env` file as `PEXELS_API_KEY=your_api_key`

---

## 🛠️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/YourUsername/YourRepositoryName.git
cd YourRepositoryName

# 2. Set up a virtual environment
python -m venv venv
venv\\Scripts\\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the FastAPI server
uvicorn api:app --reload
```


---

# 🧳 AI 기반 여행 정보 추천 시스템

여행 관련 질문을 입력하면,  
자동으로 질문을 분류하고 관련 정보를 찾아  
텍스트 답변과 이미지를 함께 제공해주는 스마트한 여행 도우미입니다.  
Google Gemini API와 Pexels API, Sentence Transformers 기반으로 작동합니다.

---

## 🚀 주요 기능

- ✅ **질문 자동 분류**: Gemini API로 `contents`, `historical`, `preparation` 중 하나로 정확히 분류
- 🔍 **문서 검색**: Sentence Transformers 임베딩 + FAISS로 유사 문서 검색
- 🧠 **답변 생성**: 문서 기반으로 Gemini가 문맥에 맞는 자연어 답변 생성
- 🗂 **카테고리별 message 구조화**
  - `contents`: Place, F&B, Activity 항목별 JSON
  - `preparation`: Clothes, ETC 항목별 JSON
  - `historical`: 시대별 설명 + 주요 사건 리스트
- 🖼️ **이미지 자동 연동**: Pexels API로 각 항목별 imageurl 자동 삽입 (FastAPI에서 처리)
- 💬 **요약 제공**: Gemini가 친근한 1~3문장 요약을 생성 (`summary`)
- 🔒 **API 키 보안**: `.env`를 통한 키 관리

---

## 📄 카테고리별 출력 형식

### 📍 `contents`
```json
{
  "Place": [{ "name": "...", "information": "..." }, ...],
  "F&B": [{ "name": "...", "information": "..." }, ...],
  "Activity": [{ "name": "...", "information": "..." }, ...]
}
```

### 📍 `preparation`
```json
{
  "Clothes": [
    {
      "name": "얇은 겉옷",
      "information": "일교차가 큰 봄·가을 여행에 적합하며, 야외 활동 시 체온 유지를 도와줍니다."
    },
    {
      "name": "편안한 운동화",
      "information": "도보 이동이 많은 여행 중 발 피로를 줄이고 안전한 활동을 도와줍니다."
    }
  ],
  "ETC": [
    {
      "name": "보조 배터리",
      "information": "장시간 외출 시 스마트폰을 지속적으로 사용할 수 있도록 도와줍니다."
    },
    {
      "name": "멀티 어댑터",
      "information": "해외 여행 시 다양한 전원 콘센트 형태에 대응할 수 있는 필수 준비물입니다."
    }
  ]
}
```

### 📍 `historical`
```json
{
  "에도 시대": {
    "시대 설명": "에도 시대 동안 오사카는 일본 최대의 상업 중심지로 성장하였고 '천하의 부엌'이라 불렸습니다.",
    "주요 사건": [
      {
        "이름": "오사카 성 건설",
        "설명": "도요토미 히데요시에 의해 건설된 오사카 성은 상징적 건축물로, 현재도 오사카 관광의 핵심입니다."
      },
      {
        "이름": "상업 붐",
        "설명": "에도 시대에 오사카는 쌀 유통의 중심지로 번성하며 전국 경제의 중심이 되었습니다."
      }
    ]
  },
  "메이지 시대": {
    "시대 설명": "메이지 유신 이후 오사카는 산업과 금융의 중심지로 급속히 발전했습니다.",
    "주요 사건": [
      {
        "이름": "근대 산업 도시화",
        "설명": "오사카는 공장과 철도가 집중되며 일본 근대 산업을 이끄는 도시로 변모했습니다."
      },
      {
        "이름": "도시 계획 도입",
        "설명": "근대적 도시 구조가 정비되며 오사카는 인프라 중심지로 탈바꿈했습니다."
      }
    ]
  }
}

```


## 📦 사용 기술

| 영역 | 기술 |
|------|------|
| 임베딩 모델 | `sentence-transformers/all-MiniLM-L6-v2` |
| 대화형 AI | Google `Gemini API` (generativeai) |
| 이미지 검색 | `Pexels API` |
| 벡터 검색 | `FAISS` |
| 환경 변수 로딩 | `python-dotenv` |
| 기타 | `requests`, `numpy`, `os` 등 |

---


## 🔑 필요한 API 키

### 1. 🔮 Google Gemini API
- [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) 에서 API 키 생성
- 생성 후 `.env` 파일에 `GEMINI_API_KEY=`에 붙여넣기

### 2. 📷 Pexels API
- [https://www.pexels.com/api/](https://www.pexels.com/api/) 에서 회원가입 후 API 키 발급
- `.env` 파일에 `PEXELS_API_KEY=`에 붙여넣기

---

## 🛠️ 설치 방법

```bash
# 1. 저장소 클론
git clone https://github.com/YourUsername/YourRepositoryName.git
cd YourRepositoryName

# 2. 가상환경 설정
python -m venv venv
venv\Scripts\activate        # Windows

# 3. 패키지 설치
pip install -r requirements.txt

# 4. FastAPI 서버 실행
uvicorn api:app --reload
