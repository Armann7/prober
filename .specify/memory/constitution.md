<!-- Sync Impact Report
Version change: unversioned template -> 1.0.0
Modified principles:
- Template principle 1 placeholder -> I. Code Quality and Maintainability
- Template principle 2 placeholder -> II. Testing Standards
- Template principle 3 placeholder -> III. User Experience Consistency (CLI)
- Template principle 4 placeholder -> IV. Performance Requirements
Removed sections:
- Template principle 5 placeholder
Added sections:
- Security & Scope Requirements
- Development Workflow & Quality Gates
Templates requiring updates:
- UPDATED .specify/templates/plan-template.md
- UPDATED .specify/templates/spec-template.md
- UPDATED .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# Prober Constitution

## Core Principles

### I. Code Quality and Maintainability
- Code MUST be PEP 8 compliant and pass ruff formatting/linting.
- Functions, methods and module-level variables MUST have type annotations; avoid Any and
  use collections.abc types where applicable.
- Imports MUST be one per line; prefer explicit control flow and clear naming over
  clever one-liners.
- Production dependencies MUST NOT be added without explicit confirmation; prefer the
  Python standard library and existing project dependencies.

Rationale: Security tooling demands auditability; these rules reduce review risk.

### II. Testing Standards
- New or changed behavior MUST include tests that cover the behavior.
- Bug fixes MUST include regression tests that fail before the fix.
- Tests MUST be deterministic and avoid network access unless explicitly required for
  integration coverage.
- Test runs MUST pass alongside ruff and mypy in the same change set.

Rationale: Reliable tests protect against regressions in automated scanning workflows.

### III. User Experience Consistency (CLI)
- CLI flags, argument naming, and output formats MUST remain consistent with existing
  conventions; breaking UX changes require explicit approval and documentation updates.
- Results MUST be written to stdout and errors to stderr; exit codes MUST be meaningful
  and documented when introduced.
- User-facing messages MUST be actionable and stable enough for automation.

Rationale: Consistent CLI behavior enables reliable scripting and operator trust.

### IV. Performance Requirements
- Performance targets MUST be defined in the plan/spec for any change that affects
  scanning, parsing, or report analysis.
- Changes MUST NOT introduce regressions beyond defined targets or prior baselines
  without explicit approval and documented rationale.
- Resource usage MUST be bounded with timeouts or limits to prevent runaway scans.

Rationale: Performance budgets keep large-scale scanning practical and predictable.

## Security & Scope Requirements

- Scanning scope MUST remain limited to in_scope assets from the
  bounty-targets-data repository; never expand scope beyond authorized assets.
- Domains and targets MUST be derived from scope data; do not hardcode domains.
- Any new network behavior MUST be documented in specifications and reviewed; OWASP
  ZAP remains the default scanning engine unless explicitly approved.

## Development Workflow & Quality Gates

- Use Python 3.14 and manage environments with uv; the virtual environment MUST reside
  in `.venv/` and MUST NOT be committed.
- ruff (linting/formatting), mypy bandit (security) MUST be run; changes MUST not introduce new
  violations or type errors. Don't use line comments to disable a check without approve.
- Documentation MUST be updated when behavior or interfaces change.
- Changes MUST be minimal and focused; avoid speculative refactors or unrelated edits.
- Reviews MUST include a Constitution Check for code quality, testing, UX consistency,
  performance targets, and scope compliance.

## Governance

- This constitution supersedes other practices; conflicts are resolved in favor of this
  document.
- Amendments require updating this file, the Sync Impact Report, and any dependent
  templates or docs affected by the change.
- Versioning follows semantic versioning: MAJOR for breaking governance changes or
  principle removals, MINOR for new principles or materially expanded guidance, PATCH
  for clarifications and non-semantic edits.
- Compliance reviews MUST verify ruff/mypy/bandit status, required tests, UX consistency,
  performance targets, scope restrictions, and dependency policy.
- Use `README.md` and `AGENTS.md` as runtime guidance; keep them aligned with this
  constitution.

**Version**: 1.0.0 | **Ratified**: 2026-01-11 | **Last Amended**: 2026-01-11
