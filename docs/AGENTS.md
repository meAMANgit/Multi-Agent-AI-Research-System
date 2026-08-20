# Specialist Agent Directory & Evaluation Rubrics

ResearchCore AI utilizes a hierarchical, collaborative collective of 7 specialized AI agents.

---

## Agent Specifications

### 1. Lead Research Director (`DirectorAgent`)
- **System Prompt Focus**: Strategy formulation, hypothesis generation, and iteration management.
- **Inputs**: User inquiry, research depth, feedback from previous review iterations.
- **Outputs**: `ResearchPlan` (topic, hypotheses, dimensions, planned search queries, subtasks).

### 2. Search Query Planner (`QueryPlannerAgent`)
- **System Prompt Focus**: Vector deconstruction and query expansion across academic, market, technical, and counter-perspectives.
- **Inputs**: ResearchPlan.
- **Outputs**: Prioritized `SearchQueryItem` list.

### 3. Academic & Web Retriever (`RetrieverAgent`)
- **System Prompt Focus**: Multi-source querying (DuckDuckGo, Wikipedia, arXiv, Tavily) and async article parsing.
- **Outputs**: Filtered `SearchResult` list with raw content and domain authority scores.

### 4. Fact & Credibility Auditor (`FactCheckerAgent`)
- **System Prompt Focus**: Empirical validation, cross-citation consistency, and hallucination elimination.
- **Outputs**: `ExtractedFact` list with confidence scores (0-100%).

### 5. Quantitative Data Analyst (`DataAnalystAgent`)
- **System Prompt Focus**: Numerical benchmarks, CAGR rates, latency metrics, energy consumption, and trade-off matrices.
- **Outputs**: `QuantitativeDataPoint` list.

### 6. Research Synthesis Author (`ReportWriterAgent`)
- **System Prompt Focus**: Executive-grade whitepaper synthesis with IEEE-style citations, architecture diagrams, and SWOT analysis.
- **Outputs**: Markdown Whitepaper.

### 7. Peer Reviewer & QA Auditor (`PeerReviewerAgent`)
- **System Prompt Focus**: 5-dimension rubric scoring and feedback generation.
- **Rubric (Max 20 Points Each / 100 Total)**:
  1. **Technical Depth & Rigor** (0-20)
  2. **Factual Accuracy & Evidence Backing** (0-20)
  3. **Structural Flow & Readability** (0-20)
  4. **Citation Validity & Source Quality** (0-20)
  5. **Objectivity & Balanced Counter-Perspectives** (0-20)
- **Decision Rule**: Total Score >= 85 -> `APPROVED`. Total Score < 85 -> `REVISION_NEEDED`.
