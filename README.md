# VoteY FastAPI Service

간단 개요
- 목적: FastAPI가 다른 백엔드(Spring)와 서버-서버 통신을 안전하게 수행.
- 보안: X-API-Key + HMAC-SHA256 서명, 요청 추적(X-Request-ID), 재시도/백오프 내장.

빠른 실행
- .env 설정 후 서버 실행:
```powershell
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
- 헬스 체크:
```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/api/health"
```

환경 변수(.env)
- API_KEY: FastAPI가 수신 시 검증할 키.
- OUTBOUND_BASE_URL: FastAPI가 호출할 대상(Spring) 베이스 URL
- OUTBOUND_API_KEY: FastAPI가 대상 서버로 전송할 API Key.
- HMAC_SECRET: 양방향 HMAC 서명/검증용 시크릿(서버 간 공유).
- REQUEST_TIMEOUT: 아웃바운드 요청 타임아웃(초).

폴더 구조(요점)
- app/main.py: 앱 엔트리(lifespan에서 httpx 클라이언트 생성, CORS/미들웨어/라우터 등록).
- app/core/: 설정 로딩(pydantic-settings), 요청 컨텍스트.
- app/api/
  - dependencies.py: verify_api_key, verify_hmac.
  - routers/: 도메인 라우터
    - health.py: 헬스
    - issue_total.py: app/data/json의 issue 관련 파일
    - items.py: API Key 보호 예시
    - secure.py: API Key + HMAC 검증
    - remote.py: 서버→서버 프록시(OUTBOUND_BASE_URL로 호출)
- app/services/http_client.py: 공유 httpx 클라이언트, 자동 헤더(X-API-Key/HMAC/X-Request-ID), 재시도/백오프.
- app/middleware/request_id.py: X-Request-ID 주입/전파.
- app/schemas/: Pydantic 모델.
- app/utils/hmac_signer.py: HMAC 유틸.

엔드포인트 요약
- Inbound(FastAPI 수신)
  - GET /api/health: 무인증
  - POST /api/items/: X-API-Key
  - GET/POST /api/secure/echo: X-API-Key + HMAC(X-Timestamp, X-Signature)
- Outbound(FastAPI → Spring)
  - /api/remote/*: OUTBOUND_BASE_URL로 프록시 호출(상대 경로 사용: "health", "secure/echo" 등)
  - 헤더 자동 첨부: X-API-Key, X-Timestamp, X-Signature, X-Request-ID

빠른 테스트 예시
```powershell
# 프록시 경유(헤더 불필요)
Invoke-RestMethod -Method Get  -Uri "http://localhost:8000/api/remote/health"
```