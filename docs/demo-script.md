# Demo Script (10 minutes)

## 0:00 – 1:00 | Introduction
- Title slide with project name and team.
- State problem: knowledge-grounded chatbot for CI&T Flow documentation.

## 1:00 – 3:00 | Architecture Overview
- Display high-level diagram from `architecture.md`.
- Highlight three tiers: React UI, FastAPI API, Redis-backed worker.
- Emphasise RAG pipeline and separation of concerns.

## 3:00 – 5:00 | Frontend Walkthrough
- Share Vercel-deployed UI.
- Show nickname gate; explain simplified authentication.
- Type question, highlight optimistic UI update and loading indicators.

## 5:00 – 7:00 | Backend & Worker Deep Dive
- Switch to Render dashboard.
- Show Docker Compose file and environment variables.
- Tail logs to demonstrate worker picking up Flow tasks.
- Briefly mention testing strategy (Pytest, Vitest, Playwright) and CI pipeline.

## 7:00 – 8:30 | Document Upload & RAG Enhancement
- Upload a PDF via UI.
- Re-run the same question and show improved answer citing uploaded document.
- Tie back to embedding store and ingestion service.

## 8:30 – 9:30 | Operations & Deployment
- Reference `operations-runbook.md` and `deployment-guide.md`.
- Highlight monitoring, alerting, and credential rotation plan.

## 9:30 – 10:00 | Q&A Prompt
- Recap key wins: worker isolation, robust testing, complete documentation.
- Invite questions and future improvements (streaming responses, multilingual support).
