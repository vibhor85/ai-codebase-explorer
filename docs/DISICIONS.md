# Architecture Decision Log

---

## Decision Template

Date

Decision

Status

Context

Options Considered

Decision

Reasoning

Trade-offs

Future Impact

---

## Example

Date

2026-07-31

Decision

Use Tree-sitter for parsing

Status

Accepted

Context

Need accurate parsing across multiple languages.

Options

- Regex
- Babel
- Tree-sitter

Decision

Use Tree-sitter.

Reasoning

Language agnostic

Fast

Supports incremental parsing

Trade-offs

Learning curve

Future Impact

Easy support for multiple languages.