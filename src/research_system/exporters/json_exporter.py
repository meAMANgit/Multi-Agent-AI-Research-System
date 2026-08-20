"""Knowledge Graph and structured JSON exporter."""

import json
import os
from src.research_system.models.schemas import ResearchResponse


class JSONExporter:
    """Exports structured research knowledge graph and full telemetry payload to JSON."""

    @classmethod
    def export_to_dict(cls, response: ResearchResponse) -> dict:
        """Construct structured graph representation with entities, facts, and sources."""
        # Convert response to dictionary
        base_dict = response.model_dump(mode="json")
        
        # Build Knowledge Graph Nodes and Links
        nodes = [
            {"id": "root_topic", "label": response.topic, "type": "topic", "group": 1}
        ]
        links = []

        # Add target dimensions as nodes
        if response.plan:
            for idx, dim in enumerate(response.plan.target_dimensions):
                dim_id = f"dim_{idx}"
                nodes.append({"id": dim_id, "label": dim, "type": "dimension", "group": 2})
                links.append({"source": "root_topic", "target": dim_id, "relation": "investigates"})

        # Add verified facts as nodes
        for idx, fact in enumerate(response.verified_facts):
            fact_id = f"fact_{idx}"
            nodes.append({
                "id": fact_id,
                "label": fact.statement[:60] + "...",
                "full_text": fact.statement,
                "type": "fact",
                "category": fact.category,
                "confidence": fact.confidence_score,
                "group": 3
            })
            links.append({"source": "root_topic", "target": fact_id, "relation": "supported_by"})

        # Add sources as nodes
        for idx, src in enumerate(response.sources[:8]):
            src_id = f"src_{idx}"
            nodes.append({
                "id": src_id,
                "label": src.title[:45] + "...",
                "url": src.url,
                "type": "source",
                "authority": src.domain_authority,
                "group": 4
            })
            links.append({"source": "root_topic", "target": src_id, "relation": "cites"})

        base_dict["knowledge_graph"] = {
            "nodes": nodes,
            "links": links,
        }

        return base_dict

    @classmethod
    def export_to_string(cls, response: ResearchResponse, indent: int = 2) -> str:
        """Serialize knowledge graph to formatted JSON string."""
        return json.dumps(cls.export_to_dict(response), indent=indent)

    @classmethod
    def export_to_file(cls, response: ResearchResponse, output_path: str) -> str:
        """Write JSON knowledge graph to disk."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cls.export_to_string(response))
        return output_path
