This document defines the rules, constraints, and expectations for **OpenAI Codex agents** and human contributors working on this repository.
Agents must follow these instructions exactly unless explicitly overridden.

---
## 1. Authority and Precedence
1. Instructions in this file take precedence over:
   * Implicit conventions
   * Tool defaults
   * Agent assumptions
2. In case of conflict, the priority order is:
   1. `AGENTS.md`
   2. `README.md`
   3. Source code comments
   4. Tool or framework defaults

---
## 2. Working Agreements
### 2.1 Dependency Management
* **Do not add new production dependencies without explicit confirmation.**
* Prefer:
  * Python standard library
  * Existing dependencies already present in the project
* Development-only dependencies may be added only if:
  * They are strictly necessary
  * Their purpose is clearly documented

---
## 3. Development Environment (Mandatory)
### 3.1 Python Version
* Use **Python 3.14** exclusively.
* Do not introduce syntax or dependencies incompatible with Python 3.14.

### 3.2 Environment & Tooling
* Use **uv** for:
  * Dependency resolution
  * Virtual environment management
* The virtual environment **must** reside in .venv/
* Never commit files from the virtual environment.

### 3.3 Required Tooling
Agents must run and respect the results of:
* `ruff`
  * Linting
  * Formatting
* `mypy`
  * Static type checking

Code changes **must not** introduce:
* New lint violations
* New type errors

---
## 4. Code Standards (Strict)
### 4.1 Style and Quality

* Code **must** comply with **PEP 8**.
* Favor:
  * Readability
  * Explicit control flow
  * Clear naming
* Avoid:
  * Clever one-liners
  * Implicit behavior
  * Over-optimization

### 4.2 Typing
* Type annotations are required for:
  * Public functions
  * Module-level variables
* `Any` should be avoided unless explicitly justified.
* Prefer types from `collections.abc` module instead of deprecated ones from `typing`.

---
### 4.3 Comments (Non-Obvious Only)
* **Do not add comments that restate the code.**
* Comments must explain:
  * *Why* something is done
  * Non-obvious constraints or trade-offs
  * Security, performance, or correctness implications
* Comments must **not** describe:
  * What the code is already clearly doing
  * Self-explanatory control flow or variable usage

**Disallowed examples:**
```python
def build_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser for Prober."""
    ...

# Loop over items
for item in items:
    process(item)
```

**Allowed examples:**
```python
# ZAP returns false positives for this endpoint; filter is intentional
if alert.risk == "HIGH":
    findings.append(alert)
# Timeout is capped to avoid hanging on misconfigured hosts
request(timeout=5)
```

* Prefer expressive naming over explanatory comments.
* If a comment is required to explain *what* the code does, refactor the code instead.


---
### 4.4 Imports
- Place imports one per line.

    **Disallowed example:**
    ```python
    from collections.abc import Iterable, Mapping
    ```
    **Allowed example:**
    ```python
    from collections.abc import Iterable
    from collections.abc import Mapping
    ```

---
## 5. Security & Scope Rules
* Never expand scanning scope beyond defined in-scope assets.
* Assume all targets are:
  * Explicitly authorized
  * Derived from the bounty-targets-data repository
* Do not:
  * Hardcode domains
  * Introduce undocumented network behavior

---
## 6. Agent Behavior Constraints
Codex agents must:
* Make **minimal, focused changes**
* Avoid speculative refactors
* Preserve existing behavior unless instructed otherwise
* Ask for clarification when requirements are ambiguous

Codex agents must **not**:
* Add features not explicitly requested
* Modify unrelated files
* Introduce silent behavior changes

---
## 7. Documentation Requirements
* Update documentation when behavior or interfaces change.
* Keep documentation:
  * Accurate
  * Concise
  * Aligned with actual implementation

---
## 8. References
* `README.md` — project purpose, workflow, and CLI usage
* Source code — authoritative behavior definition
