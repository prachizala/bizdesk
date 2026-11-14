# Security Audit: BizDesk
- **Owner Authentication**: JWT tokens with PBKDF2 HMAC-SHA256 password encryption.
- **SQL Injection Prevention**: Parameterized SQLAlchemy queries across all CRM endpoints.
- **Data Integrity**: Enforced database constraints preventing duplicate booking records.
