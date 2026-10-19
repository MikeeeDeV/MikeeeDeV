# Security Policy

## Supported Versions

We actively support and maintain the latest release of the Profile Engine and VectorForge Shape Studio:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

---

## 🔒 Security Architecture & Guarantees

This repository is designed with **zero runtime trust** and **hermetic determinism**:

1. **Zero External Runtime Execution**:
   All SVG assets, status badges, and terminal cards are static vector documents pre-rendered and committed. They do not trigger client-side fetch requests, eval scripts, or dynamic cross-origin tracking.
2. **Safe XML Sanitization**:
   All text fields, commits, and labels are sanitized and escaped before injection into SVG documents to eliminate SVG-based XSS (Cross-Site Scripting) vectors.
3. **No Secret Leaks**:
   GitHub Actions workflows operate with least-privilege tokens. All personal tokens are scoped strictly to read operations where applicable.

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability or potential data leak in this repository, please do **NOT** open a public issue.

Instead, please report the vulnerability confidentially:

1. **Email**: Send details to [mohamed.ayman.developer@gmail.com](mailto:mohamed.ayman.developer@gmail.com).
2. **Include**:
   - A detailed description of the vulnerability.
   - Proof of Concept (PoC) or reproduction steps.
   - Potential impact.
3. **Response SLA**:
   - We will acknowledge receipt of your report within **24 hours**.
   - A triage update and proposed fix timeline will be provided within **72 hours**.
