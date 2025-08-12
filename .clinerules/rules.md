# python-kiwoom 프로젝트를 위한 Cline 규칙

이 문서는 `python-kiwoom` 프로젝트의 개발 가이드라인과 규칙을 정의합니다.

## 1. 프로젝트 개요

본 프로젝트는 키움증권 REST API를 쉽게 사용할 수 있도록 돕는 Python 래퍼(Wrapper) 라이브러리입니다.

## 2. 언어 및 코드 스타일

-   **언어:** Python 3.9 이상
-   **가상환경:** `uv`를 사용하여 가상 환경을 구성하고 의존성을 관리합니다.
-   **코드 포맷팅:** `black`을 사용하여 코드 스타일을 통일합니다.
-   **린팅:** `flake8`을 사용하여 코드 스타일 및 잠재적 오류를 검사합니다.
-   **임포트 정렬:** `isort`를 사용하여 import 구문을 정렬합니다.
-   **타입 힌팅:** `mypy`를 사용하여 정적 타입 검사를 수행합니다. 모든 새로운 코드에는 타입 힌트를 작성해야 합니다.

## 3. 프로젝트 구조

표준 Python 라이브러리 구조를 따릅니다.

```
python-kiwoom/
├── kiwoom/
│   ├── __init__.py
│   ├── client.py       # API 클라이언트
│   ├── models.py       # API 응답/요청 모델 (Pydantic)
│   ├── tr.py           # TR 코드 관련 처리
│   └── ...
├── tests/
│   ├── __init__.py
│   ├── test_client.py
│   └── ...
├── .gitignore
├── pyproject.toml
├── README.md
└── ...
```

## 4. 의존성 관리

-   `pyproject.toml` 파일을 사용하여 프로젝트 의존성과 메타데이터를 관리합니다.
-   `uv`를 사용하여 `pyproject.toml`에 정의된 의존성을 설치합니다. (`uv pip install -e .`)
-   주요 의존성:
    -   `httpx`: 비동기 지원이 가능한 HTTP 클라이언트
    -   `pydantic`: 데이터 유효성 검사 및 모델링

## 5. API 클라이언트 설계

-   메인 클라이언트는 클래스(`KiwoomClient`)로 구현합니다.
-   클라이언트의 메서드는 키움 API의 각 엔드포인트에 대응되도록 작성합니다.
-   인증, 헤더, 기본 URL 등은 클라이언트 내부에서 처리합니다.
-   API 에러 발생 시, 사용자 정의 예외(`KiwoomAPIError`)를 발생시킵니다.

### 인증 모듈 예시

```python
import requests
import json

# 접근토큰 발급
def fn_au10001(data):
	# 1. 요청할 API URL
	#host = 'https://mockapi.kiwoom.com' # 모의투자
	host = 'https://api.kiwoom.com' # 실전투자
	endpoint = '/oauth2/token'
	url =  host + endpoint

	# 2. header 데이터
	headers = {
		'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
	}

	# 3. http POST 요청
	response = requests.post(url, headers=headers, json=data)

	# 4. 응답 상태 코드와 데이터 출력
	print('Code:', response.status_code)
	print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
	print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
	# 1. 요청 데이터
	params = {
		'grant_type': 'client_credentials',  # grant_type
		'appkey': 'AxserEsdcredca.....',  # 앱키
		'secretkey': 'SEefdcwcforehDre2fdvc....',  # 시크릿키
	}

	# 2. API 실행
	fn_au10001(data=params)
```

### Request/Response 예시

**Request**
```json
{
	"grant_type": "client_credentials",
	"appkey": "AxserEsdcredca.....",
	"secretkey": "SEefdcwcforehDre2fdvc...."
}
```

**Response**
```json
{
	"expires_dt":"20241107083713",
	"token_type":"bearer",
	"token":"WQJCwyqInphKnR3bSRtB9NE1lv...",
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
```

## 6. 문서화

-   **Docstrings:** 모든 모듈, 클래스, 함수에 대해 Google 스타일 Docstring을 작성합니다.
-   **README.md:** 설치 방법, 기본 사용법 예제, 전체 문서 링크를 포함해야 합니다.

## 7. 테스트

-   `pytest`를 사용하여 테스트 코드를 작성하고 실행합니다.
-   API 응답을 모의(Mocking)하기 위해 `pytest-mock`을 사용합니다. 실제 API를 호출하지 않도록 합니다.
-   테스트 코드는 `tests/` 디렉토리에 위치합니다.

## 8. 커밋 메시지

[Conventional Commits](https://www.conventionalcommits.org/) 명세를 따릅니다. 이는 변경 이력을 쉽게 파악하고, 변경 로그(Changelog)를 자동 생성하는 데 도움이 됩니다.

예시: `feat: 실시간 시세 조회 기능 추가`

## 9. 개발 워크플로우

1.  `uv venv` 명령어로 가상 환경을 생성하고 활성화합니다.
2.  `uv pip install -e .` 명령어로 개발 의존성을 설치합니다.
3.  기능 개발 또는 버그 수정을 위해 새 브랜치를 생성합니다.
4.  위 가이드라인에 따라 코드를 작성합니다.
5.  **애플리케이션 실행:** `uv run python -m kiwoom.client` (또는 메인 실행 파일 경로) 명령어로 애플리케이션을 실행합니다.
6.  **테스트 실행:** `uv run pytest` 명령어로 테스트를 실행합니다.
7.  모든 테스트와 린터 검사를 통과하는지 확인합니다.
8.  코드 리뷰를 위해 Pull Request를 생성합니다.
