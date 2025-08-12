# Kiwoom REST API Design Rules

This document outlines the expected structure and handling of responses from the Kiwoom REST API within the `python-kiwoom` project.

## 1. API Response Structure

Kiwoom REST API responses generally follow this pattern:

*   **HTTP Status Code:** Indicates the overall success or failure of the HTTP request (e.g., 200 OK, 400 Bad Request).
*   **Response Headers:**
    *   `cont-yn`: Continuous query flag ('Y' for continuation, 'N' for no more data).
    *   `next-key`: Key for the next continuous query.
    *   `api-id`: The TR name (e.g., 'ka10001').
*   **Response Body (JSON):**
    *   Contains `return_code` (0 for success, non-zero for failure) and `return_msg`.
    *   If `return_code` is 0 (success), the actual data payload (e.g., stock information, access token details) is directly present as top-level fields within the JSON body, alongside `return_code` and `return_msg`. It is NOT nested under a separate `data` key.

**Example Successful Response Body (Authentication):**
```json
{
    "expires_dt": "20251107083713",
    "token_type": "bearer",
    "token": "YOUR_ACCESS_TOKEN",
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

**Example Successful Response Body (Stock Info - ka10001):**
```json
{
    "stk_cd": "005930",
    "stk_nm": "삼성전자",
    "mrkt_type": "KOSPI",
    "prpr": "71100",
    // ... other stock info fields
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다"
}
```

## 2. Response Parsing Guidelines

*   **Direct Body Parsing:** When parsing the JSON response body for successful API calls (`return_code: 0`), the Pydantic models for the data (e.g., `AccessToken`, `StockInfo`) should directly map to the top-level fields of the JSON body. There is no need for a generic `APIResponse` wrapper with a `data` field for the actual payload.
*   **Error Handling:** Check `return_code` in the JSON body for API-specific errors. If `return_code` is not 0, raise a `KiwoomAPIError` using `return_msg`.
*   **Header Extraction:** Extract `cont-yn` and `next-key` from the response headers for pagination/continuous query logic where applicable.
