# Kiwoom API 예시

이 문서는 `python-kiwoom` 프로젝트에서 키움증권 REST API를 사용하는 추가 예시를 제공합니다.

## 1. 주식기본정보요청 (fn_ka10001)

주식의 기본 정보를 요청하는 예시입니다.

### 인증 모듈 예시

```python
import requests
import json

# 주식기본정보요청
def fn_ka10001(token, data, cont_yn='N', next_key=''):
	# 1. 요청할 API URL
	#host = 'https://mockapi.kiwoom.com' # 모의투자
	host = 'https://api.kiwoom.com' # 실전투자
	endpoint = '/api/dostk/stkinfo'
	url =  host + endpoint

	# 2. header 데이터
	headers = {
		'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
		'authorization': f'Bearer {token}', # 접근토큰
		'cont-yn': cont_yn, # 연속조회여부
		'next-key': next_key, # 연속조회키
		'api-id': 'ka10001', # TR명
	}

	# 3. http POST 요청
	response = requests.post(url, headers=headers, json=data)

	# 4. 응답 상태 코드와 데이터 출력
	print('Code:', response.status_code)
	print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
	print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
	# 1. 토큰 설정
	MY_ACCESS_TOKEN = '사용자 AccessToken' # 접근토큰

	# 2. 요청 데이터
	params = {
		'stk_cd': '005930', # 종목코드 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
	}

	# 3. API 실행
	fn_ka10001(token=MY_ACCESS_TOKEN, data=params)

	# next-key, cont-yn 값이 있을 경우
	# fn_ka10001(token=MY_ACCESS_TOKEN, data=params, cont_yn='Y', next_key='nextkey..')
```

### Request/Response 예시

**Request**
```json
{
	"stk_cd" : "005930"
}
```

**Response**
```json
{
	"stk_cd":"005930",
	"stk_nm":"삼성전자",
	"setl_mm":"12",
	"fav":"5000",
	"cap":"1311",
	"flo_stk":"25527",
	"crd_rt":"+0.08",
	"oyr_hgst":"+181400",
	"oyr_lwst":"-91200",
	"mac":"24352",
	"mac_wght":"",
	"for_exh_rt":"0.00",
	"repl_pric":"66780",
	"per":"",
	"eps":"",
	"roe":"",
	"pbr":"",
	"ev":"",
	"bps":"-75300",
	"sale_amt":"0",
	"bus_pro":"0",
	"cup_nga":"0",
	"250hgst":"+124000",
	"250lwst":"-66800",
	"high_pric":"95400",
	"open_pric":"-0",
	"low_pric":"0",
	"upl_pric":"20241016",
	"lst_pric":"-47.41",
	"base_pric":"20231024",
	"exp_cntr_pric":"+26.69",
	"exp_cntr_qty":"95400",
	"250hgst_pric_dt":"3",
	"250hgst_pric_pre_rt":"0",
	"250lwst_pric_dt":"0.00",
	"250lwst_pric_pre_rt":"0",
	"cur_prc":"0.00",
	"pre_sig":"",
	"pred_pre":"",
	"flu_rt":"0",
	"trde_qty":"0",
	"trde_pre":"0",
	"fav_unit":"0",
	"dstr_stk":"0",
	"dstr_rt":"0",
	"return_code":0,
	"return_msg":"정상적으로 처리되었습니다"
}
