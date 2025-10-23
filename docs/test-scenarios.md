# Test Scenarios

## Backend

| Scenario | Steps | Expected Result | Type |
| --- | --- | --- | --- |
| Health endpoint | Call `GET /api/health/ping` | Response `200` with `{ "status": "ok" }` | Smoke |
| Document ingestion (empty) | POST `/api/documents/ingest` with empty directory | Response `202` with empty list or zero chunks | Unit |
| Document upload (PDF) | Upload sample PDF | Response `201`, chunks indexed > 0 | Integration |
| Chat completion | POST `/api/chat/completions` with stubbed Flow response | Response `200`, contains `response` text | Unit |
| Worker task | Enqueue `process_chat` with prompt | Result contains context array | Integration |

## Frontend

| Scenario | Steps | Expected Result | Type |
| --- | --- | --- | --- |
| Nickname gate | Enter nickname | Chat UI unlocked; nickname persisted in local storage | Unit |
| Message submission | Type message and press send | Message appears in chat; API called | Component |
| Assistant response render | Mock API returning context | Assistant bubble shows response and cited documents | Component |
| Document upload flow | Select PDF via UI | Progress indicator shown; success toast on completion | Integration |
| Error handling | API returns 500 | User sees non-blocking error banner | Component |

## End-to-End (Playwright)

1. Launch frontend against local Docker environment.
2. Fill nickname, send message, wait for mocked backend response.
3. Upload document and confirm toast.
4. Assert chat history contains both user and assistant messages.

## Performance

- Load test using k6: 25 virtual users, ramp-up 2 minutes, sustained 5 minutes, to validate P95 < 3 seconds when Flow API is mocked.

## Regression

- Run `pytest` + `npm run test` + `npx playwright test` on every pull request via GitHub Actions.
