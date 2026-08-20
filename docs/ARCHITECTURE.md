# Architecture & System Design Specification

## Overview

**ResearchCore AI** is an enterprise-grade autonomous multi-agent deep research intelligence engine. It deconstructs complex technical, economic, and scientific inquiries into structured hypotheses, conducts parallel multi-vector retrieval across academic and open web repositories, extracts verified facts and quantitative metrics, authors comprehensive whitepapers, and executes peer-review QA audits with automatic revision loops.

```
                                 ┌────────────────────────┐
                                 │   User Research Query  │
                                 └───────────┬────────────┘
                                             │
                                             ▼
                             ┌───────────────────────────────┐
                             │  1. Lead Research Director    │
                             │  - Hypothesis Deconstruction  │
                             │  - Target Dimension Mapping   │
                             └───────────────┬───────────────┘
                                             │
                                             ▼
                             ┌───────────────────────────────┐
                             │  2. Search Query Planner      │
                             │  - Multi-Vector Query Gen     │
                             │  - Academic / Market / Tech   │
                             └───────────────┬───────────────┘
                                             │
                                             ▼
                             ┌───────────────────────────────┐
                             │  3. Academic & Web Retriever  │
                             │  - DuckDuckGo / arXiv / Wiki  │
                             │  - Async HTML Markdown Scraper│
                             └───────┬───────────────┬───────┘
                                     │               │
                     ┌───────────────┘               └───────────────┐
                     ▼                                               ▼
     ┌───────────────────────────────┐               ┌───────────────────────────────┐
     │  4. Fact & Credibility Auditor│               │ 5. Quantitative Data Analyst  │
     │  - Cross-Source Verification  │               │ - Metric & CAGR Extraction    │
     │  - Hallucination Flagging     │               │ - Benchmark Trade-off Matrices│
     └───────────────┬───────────────┘               └───────────────┬───────────────┘
                     │                                               │
                     └───────────────┐               ┌───────────────┘
                                     ▼               ▼
                             ┌───────────────────────────────┐
                             │ 6. Research Synthesis Author  │
                             │ - Executive Whitepaper Draft  │
                             │ - IEEE Numbered Citations     │
                             └───────────────┬───────────────┘
                                             │
                                             ▼
                             ┌───────────────────────────────┐
                             │  7. Peer Reviewer & QA Auditor│
                             │  - 5-Dimension Rubric Scoring │
                             └───────┬───────────────┬───────┘
                                     │               │
            Score < 85 (Needs Revision)              │ Score >= 85 (Approved)
            ┌────────────────────────┘               │
            ▼                                        ▼
    [ Targeted Revision Loop ]            ┌───────────────────────────────────┐
    (Back to Director Agent)              │ Multi-Format Intelligence Package │
                                          │ - Markdown Whitepaper (.md)       │
                                          │ - Interactive HTML Report (.html) │
                                          │ - JSON Knowledge Graph (.json)    │
                                          └───────────────────────────────────┘
```

---

## The 7 Specialist Agent Roles

| Agent | Class | Core Responsibility |
| :--- | :--- | :--- |
| **1. Director** | `DirectorAgent` | Formulates 3 hypotheses, maps 5 investigation dimensions, supervises loops. |
| **2. Query Planner** | `QueryPlannerAgent` | Expands research directives into technical, academic, market, and risk queries. |
| **3. Retriever** | `RetrieverAgent` | Concurrently queries search backends and asynchronously scrapes full-text articles. |
| **4. Fact Checker** | `FactCheckerAgent` | Cross-references empirical evidence, calculates confidence scores (0-100), detects hallucinations. |
| **5. Data Analyst** | `DataAnalystAgent` | Extracts numerical benchmarks, percentages, CAGR, latency figures, and structures comparison matrices. |
| **6. Report Writer** | `ReportWriterAgent` | Synthesizes verified findings into an authoritative executive whitepaper with IEEE citations. |
| **7. Peer Reviewer** | `PeerReviewerAgent` | Audits the report against 5 dimensions (Depth, Accuracy, Flow, Citations, Objectivity). Approves or triggers feedback revisions. |

---

## State Machine & Telemetry

The execution state is managed via `ResearchState` (`Pydantic v2`):
- **Immutability & Safety**: Private subscriber callbacks stream every reasoning step via WebSockets and Streamlit UI in real-time.
- **Cost & Token Telemetry**: Integrated `CostTracker` tracks prompt tokens, completion tokens, latency (ms), and exact USD cost per model.
- **Resilient Fallback Engine**: If no API keys are provided or network errors occur, the system automatically falls back to deterministic, high-signal heuristic engines for 100% test reliability.
