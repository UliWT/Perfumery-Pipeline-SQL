# Skill Registry - Perfumeria

## User Skills (auto-detected)

| Name | Trigger | Location |
|------|---------|----------|
| branch-pr | Creating a pull request, opening a PR, or preparing changes for review. | ~/.gemini/skills/branch-pr/SKILL.md |
| issue-creation | Creating a GitHub issue, reporting a bug, or requesting a feature. | ~/.gemini/skills/issue-creation/SKILL.md |
| judgment-day | When user says "judgment day", "review adversarial", "dual review", "doble review", "juzgar", "que lo juzguen". | ~/.gemini/skills/judgment-day/SKILL.md |
| go-testing | Go tests, Bubbletea TUI testing | ~/.gemini/skills/go-testing/SKILL.md |

## Compact Rules (auto-resolved)

### Python (Data Engineering)
- Use `pandas` for data manipulation.
- Use `deltalake` for Delta Lake operations.
- Use `sqlalchemy` for PostgreSQL connections.
- Follow PEP 8 standards.
- Layers:
  - Bronze: Parquet/Delta with raw data.
  - Silver: Cleaned data, typed columns, no duplicates.
  - Gold: Business aggregates, joins, ready for consumption.

### Testing
- No test runner detected. TDD is currently disabled.
- Goal: Implement `pytest` eventually.

### Documentation
- Use DBeaver to verify tables in PostgreSQL.
- Keep the pipeline idempotent.
