# InboundFlow 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Built with Pydantic](https://img.shields.io/badge/Data%20Validation-Pydantic-E91E63.svg)](https://docs.pydantic.dev/)

**InboundFlow** converts messy, raw incoming SMTP emails into structured, sanitized, and strictly typed JSON webhooks delivered instantly to your application backend. 

Stop wrestling with multipart raw mail formats, stripping out email signature clutter, or managing complex mail servers. Provision an email address via our API, point your users to it, and receive clean webhooks.

---

## ✨ Features

* **Instant SMTP Ingestion:** Blazing fast asynchronous processing built on top of FastAPI.
* **Smart Content Sanitization:** Automatically strips out email signature noise, tracking pixels, and messy raw HTML headers.
* **Strict Pydantic Validation:** Every webhook guarantees a clean schema including validated sender fields, subject lines, body text, and structured attachments.
* **Resilient Webhook Retries:** If your server goes down, our queue system retries deliveries with exponential backoff.
* **Attachment Offloading:** Large email attachments are automatically parsed and saved to secure cloud storage URLs.

---

## 🛠️ Tech Stack & Architecture

* **Framework:** FastAPI (Asynchronous ASGI processing)
* **Data Validation:** Pydantic v2
* **Database & Queue:** PostgreSQL & Alembic (state persistence), Redis (rate limiting & webhook queuing)

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and install dependencies using your preferred package manager:

```bash
git clone [https://github.com/yourusername/inboundflow.git](https://github.com/yourusername/inboundflow.git)
cd inboundflow

# Install using pip
pip install -r requirements.txt
