---
id: 1
title: Hackathon Todo App Constitution
stage: constitution
date: 2025-12-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: claude
command: /sp.constitution
labels: [constitution, governance, hackathon]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
tests:
 - none
---

## Prompt

```text
Hackathon Todo App Constitution
Core Principles
I. Spec-First

Every feature starts with a fully written spec before implementation.

Specs must be self-contained, clear, and human-readable.

All specs live under /specs folder, organized by type (features, API, database, UI).

No code is written without a corresponding spec.

II. Full-Stack Feature Implementation

Each feature is implemented across the entire stack: backend, frontend, database, and UI.

Frontend or backend alone is never implemented in isolation.

Implementation must follow the spec exactly.

III. Test-First / TDD (Non-Negotiable)

All endpoints and UI components must have tests before or during implementation.

Red-Green-Refactor cycle is mandatory:

Write failing test

Implement feature

Ensure test passes

Refactor if necessary

IV. JWT-Based Authentication & Security

All user-related API endpoints must enforce JWT token verification.

User isolation: each user only sees and modifies their own tasks.

Unauthorized requests must return 401 Unauthorized.

Shared secrets (BETTER_AUTH_SECRET) must be stored in environment variables.

V. Observability, Logging & Simplicity

All backend operations must log key actions and errors in a structured format.

Frontend and backend must be debuggable independently.

Start simple: no over-engineering; YAGNI principles apply.

VI. Monorepo & CLAUDE Context

Use a single monorepo for both frontend and backend.

CLAUDE.md files must guide Claude Code in conventions and stack patterns.

Root CLAUDE.md provides overview; subfolder CLAUDE.md files provide layer-specific guidance.

Additional Constraints

Technology Stack:

Frontend: Next.js 16+, TypeScript, Tailwind CSS

Backend: FastAPI, SQLModel, Neon Serverless PostgreSQL

Authentication: Better Auth with JWT

Performance Standards:

API responses under 300ms in dev environment

Minimal DB queries: use indexes for filtering

Security Requirements:

No sensitive data in logs

JWT tokens must have expiry (~7 days)

Database access restricted via credentials stored in environment variables

Development Workflow

Write/Update spec: /specs/features/<feature>.md

Generate plan: outline endpoints, models, frontend components

Break plan into atomic tasks

Implement via Claude Code (both frontend + backend)

Test each task fully (unit + integration + UI)

Update spec if feature changes

Repeat for next feature

Governance

This constitution supersedes any ad-hoc development practices.

All PRs and Claude Code implementations must comply with this constitution.

Complexity must be justified in the spec and CLAUDE.md.

Amendments require documentation, approval, and migration plan.

Use /CLAUDE.md and /specs/overview.md for runtime development guidance.

Version: 1.0 | Ratified: 2025-12-15 | Last Amended: 2025-12-15
```

## Response snapshot

Updated the project constitution by populating the template with the Hackathon Todo App Constitution details. The constitution now includes six core principles: Spec-First, Full-Stack Feature Implementation, Test-First/TDD, JWT-Based Authentication & Security, Observability & Simplicity, and Monorepo & CLAUDE Context.

I also updated the related templates to align with the new constitution:
1. Updated the plan template to include constitution checks
2. Updated the spec template to include constitution compliance section
3. Updated the tasks template to reflect full-stack and authentication requirements

The constitution file is now properly populated with the project's governance principles and requirements.

## Outcome

- ✅ Impact: Project constitution fully populated with Hackathon Todo App principles and related templates updated
- 🧪 Tests: No tests required for this governance update
- 📁 Files: Updated constitution.md and three template files to align with new principles
- 🔁 Next prompts: Ready to proceed with feature specification and implementation following the new constitution
- 🧠 Reflection: Constitution now provides clear governance framework for the hackathon project

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification following the new constitution