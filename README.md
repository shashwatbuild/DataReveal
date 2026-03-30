# 💻 DataReveal AI — Enterprise RAG + SQL Intelligence System

> **"Reveal insights from any data — structured or unstructured — instantly."**

<p align="center">

<img src="https://img.shields.io/badge/Python-3.12+-blue?logo=python"/>
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi"/>
<img src="https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit"/>
<img src="https://img.shields.io/badge/LangChain-AI%20Framework-black"/>
<img src="https://img.shields.io/badge/RAG-Enabled-purple"/>
<img src="https://img.shields.io/badge/SQL-Agent-blue"/>
<img src="https://img.shields.io/badge/FAISS-VectorDB-orange"/>
<img src="https://img.shields.io/badge/Ollama-LLM-orange"/>
<img src="https://img.shields.io/badge/OpenAI-LLM-412991?logo=openai"/>
<img src="https://img.shields.io/badge/License-MIT-green"/>

</p>

---

## 🧠 Overview

**DataReveal AI** is a production-grade AI-powered data platform that allows users to interact with their data using natural language.

It intelligently processes both:

* 📊 **Structured Data (CSV / Excel)** → via SQL Agent
* 📄 **Unstructured Data (PDF / Text)** → via RAG (Retrieval-Augmented Generation)

This system acts like:

> **"ChatGPT for your enterprise data."**

<img width="1465" height="815" alt="Screenshot 2026-03-26 at 3 06 44 PM" src="https://github.com/user-attachments/assets/290e181e-b6c7-4f78-9dfa-a92135f8a45f" />
<img width="1470" height="836" alt="Screenshot 2026-03-26 at 3 07 10 PM" src="https://github.com/user-attachments/assets/2782b782-3203-441c-bdc0-025da88665e9" />
<img width="1467" height="806" alt="Screenshot 2026-03-26 at 3 09 25 PM" src="https://github.com/user-attachments/assets/985b42dc-c96a-4d9e-81ec-32a35a0fedc4" />
<img width="1464" height="829" alt="Screenshot 2026-03-26 at 3 11 13 PM" src="https://github.com/user-attachments/assets/67c44f51-f12e-4201-9f39-0954c8cd387d" />

---

## ⚡ Core Capabilities

* 📂 Upload any data (CSV, Excel, PDF, Text)
* 💬 Ask questions in natural language
* 🤖 Intelligent routing:

  * SQL Agent → for tabular insights
  * RAG Pipeline → for document understanding
* 📊 Generate accurate, data-backed insights
* 🧠 AI explanations for query results
* 🔍 Context-aware responses using embeddings

---

## 🏗️ System Architecture

```
Frontend (Streamlit Chat UI)
        ↓
FastAPI Backend
        ↓
🧭 Router Agent (RAG vs SQL Decision)
        ↓
┌──────────────┬───────────────┬──────────────┐
│ RAG Pipeline │ SQL Engine    │ File Manager │
└──────────────┴───────────────┴──────────────┘
        ↓               ↓
   Vector DB        Pandas/DB
        ↓               ↓
        └──────→ LLM (Ollama/OpenAI) ←──────┘
                        ↓
                Final AI Response
```

---

## 🤖 Intelligent Agent System

This platform is powered by modular AI agents:

### 📁 Data Upload Agent

Handles file ingestion and validation

### 🧹 Preprocessing Agent

Cleans and standardizes raw data

### ✂️ Chunking Agent (RAG)

Splits text into meaningful chunks

### 🔗 Embedding Agent

Converts data into vector embeddings

### 🗄️ Vector Store Agent

Stores embeddings using FAISS

### 🔍 Retrieval Agent

Fetches relevant context

### 🧠 SQL Generation Agent

Converts natural language → SQL

### ⚙️ Query Execution Agent

Executes safe SQL queries

### 🧠 Response Agent

Generates human-like answers

### 🧭 Router Agent (Core Brain)

Decides between SQL vs RAG flow

---

## 🔁 Workflow

### 📥 Data Ingestion

* Upload file
* Clean & preprocess
* Store:

  * Text → Vector DB
  * CSV → Query-ready

---

### 💬 Query Processing

1. User asks a question
2. Router decides:

   * SQL → Generate & execute query
   * RAG → Retrieve relevant context
3. LLM generates final answer

---

## 🛠️ Tech Stack

* **Language:** Python
* **LLM:** OpenAI / Ollama
* **Framework:** LangChain
* **Backend:** FastAPI
* **Frontend:** Streamlit
* **Vector DB:** FAISS
* **Data Processing:** Pandas
* **Optional:** SQLite / Snowflake

---

## 📁 Project Structure

```
rag-enterprise/
│
├── frontend/
├── backend/
├── agents/
├── rag/
├── data/
├── utils/
├── requirements.txt
└── README.md
```

---

## 🔐 Key Design Principles

* ❌ No hallucination — answers must use data
* 🔍 Context-first responses
* 🔒 Safe SQL execution (read-only)
* 🧩 Modular agent-based architecture
* ⚡ Scalable & production-ready

---

## 🚀 Deployment Strategy

* 🖥️ Local: Ollama
* 🐳 Dockerized services
* ☁️ Azure App Service (Backend)
* 🌐 Streamlit Cloud (Frontend)

---

## 🧪 Testing

* Upload datasets
* Test:

  * RAG queries
  * SQL queries
* Validate accuracy & performance

---

## 🌟 Why This Project is Unique

* Combines **RAG + SQL + AI Agents** in one system
* Works on **any data format**
* Mimics real-world enterprise AI platforms
* Demonstrates **Data Engineering + AI + Backend + System Design**

---

## 🎯 Final Vision

> **"A unified AI system that replaces dashboards, BI tools, and manual analysis."**

---

## 👨‍💻 Author

**Shashwat Saxena**
Azure Data Engineer | AI Systems Builder

---

## 🔥 Taglines

* **"From raw data to real intelligence."**
* **"Ask your data. Get real answers."**
* **"One system. Any data. Infinite insights."**

---

⭐ Star this repo if you believe in AI-powered data systems!
