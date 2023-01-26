
# Service Design Document

![core service](https://img.shields.io/badge/svc-core-red)

AWS service provides API endpoints for interacting with AWS hardware.

---
## 🏜 **Background**

This service replaces the existing aws-quantum plugin for the new 2022 platform upgrade.

---
## ⭐ **User Stories**

As a sdk dev I would like to use the new service as a complete replacement for the older service.

---

## 🤝Requirements

### Constraints
- Use FastAPI
- Use service-lib

### Criteria
- The service should handle billing transactions
- Handle job creation
  - Precheck (billing etc)
  - Submit job to amazon
  - Create entry in platform
  - Make billing entry (use the billing module from braket to calculate cost -- vs current solution)
  - Return job id (or strangeworks response object -- tbd)
- Update job life cycle
  - Implement required cron endpoints (justin will write something)
  - investigate socket or hooks for job completion / status update from amazon
- Generate new resouces -- implement resource activation
  - Does this apply for all services?
  - In this case we have a managed account?
- Should implement all existing endpoints. Refer to existing code in `app/jobs.py` and `app/backends.py` etc

---

## ✏️**Design**


---

## 🌎**Release Plan**

Will be released as part of the updated product. Tested in staging.

---

## 🔒 Security Considerations

TBD

---

## ❓**Questions**

How do we verify the platform is making call? (keys)

---

## 📎Related Assets

https://github.com/strangeworks/service-lib
