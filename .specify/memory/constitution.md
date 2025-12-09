<!--
SYNC IMPACT REPORT
Version change: N/A (initial version) → 1.0.0
Added sections: Core Principles (6 principles), Technical Architecture Requirements, Development Standards & Quality Metrics, Governance
Removed sections: None (this is the initial constitution)
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ Constitution Check section should reference new principles
  - .specify/templates/spec-template.md: ⚠ pending (may need updates to align functional requirements with new principles)
  - .specify/templates/tasks-template.md: ⚠ pending (may need updates for test coverage requirements)
  - .specify/templates/commands/*.md: ✅ No changes needed as no command templates exist
  - README.md: ⚠ pending (if exists, should reference new constitution principles)
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Learning Platform Constitution

## Core Principles

### Spec-First, AI-Augmented
No code or content without validated specifications

### Pedagogy-Driven
Content structure must optimize learning outcomes

### Production-Ready
Hackathon speed cannot compromise system stability

### Open by Design
Architecture must support community contributions

### Type Safety & Validation
All Python code requires type hints, all functions require Google-style docstrings, and mypy compliance is mandatory

### Test Coverage Requirement
Backend code must maintain ≥85% test coverage using pytest

## Technical Architecture Requirements

Stack Requirements:
- Frontend: Docusaurus 3.x (React 18+, TypeScript 5+)
- Backend: FastAPI (Python 3.12+)
- Package Manager: uv (strictly enforced)
- Database: Neon PostgreSQL (operational), Qdrant (vector)
- Authentication: Better-Auth
- Orchestration: Claude Code CLI + Spec-Kit Plus

Infrastructure Rules:
- All Python dependencies pinned via uv.lock
- Environment variables managed through .env.production only
- Vector embeddings: all-MiniLM-L6-v2 (default), configurable
- API versioning: /v1/* prefix mandatory

## Development Standards & Quality Metrics

Python Code Standards:
- Type hints required for all functions
- Google-style docstrings required for all functions
- mypy compliance mandatory
- pytest with 90%+ coverage required
- src/ layout with clear separation

Quality Metrics (Minimum Viable):
- Backend test coverage: ≥85%
- Page load time: <3 seconds
- RAG response accuracy: >90% on test queries
- Translation quality: >70% human evaluator score
- Mobile responsiveness: 100% chapters

Database Schemas:
- User profiles with learning style, language preference, proficiency level, and personalized pathways
- Learning analytics tracking sessions, chapter completion, time spent, and assessment scores

## Governance

Workflow Rules:
- Atomic Tasks: All work decomposed to <2 hour units
- Validation Gates: Code must pass unit tests + integration tests, content requires curriculum alignment check + peer review
- Commit Standards: Conventional commits (feat:, fix:, docs:, content:), no direct pushes to main - PRs only
- Checkpoints: Every 4 hours - demonstrable progress required

Decision Authority:
- Technical Decisions: Lead Architect (specified in ADRs)
- Content Decisions: Curriculum Committee (3 members minimum)
- Merge Authority: Two approved reviews required

Change Management:
- Constitution amendments: Unanimous team vote required
- Syllabus changes: Curriculum Committee + one industry expert
- Breaking API changes: 48-hour deprecation notice

Risk Mitigation:
- Vector DB failure: SQLite fallback with TF-IDF
- Auth service outage: Read-only mode with cached content
- Translation API limits: Queue system with exponential backoff

**Version**: 1.0.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09