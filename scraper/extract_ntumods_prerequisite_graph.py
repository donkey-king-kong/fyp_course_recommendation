from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

from scrape_ntumods_dependencies import decode_astro_props

DEFAULT_INPUT = Path("data/prerequisite_graph.html")
DEFAULT_OUTPUT = Path("data/ntu_prerequisite_unlock_graph.json")

def main() -> None:
    parser = argparse.ArgumentParser(description="Extract the full NTUMods prerequisite graph from saved HTML.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Path to the saved NTUMods HTML file.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Path to save the prerequisite graph JSON.")
    args = parser.parse_args()

    prerequisite_graph = extract_prerequisite_graph(args.input)
    write_json(args.output, prerequisite_graph)
    print(f"Saved {len(prerequisite_graph)} prerequisite graph modules to {args.output}")

def extract_prerequisite_graph(input_path: Path) -> dict[str, dict[str, list[str]]]:
    raw_html = input_path.read_text(encoding="utf-8")

    if not raw_html.strip():
        raise ValueError(f"{input_path} is empty. Save the full NTUMods page source HTML before running this script.")

    source_html = normalize_saved_html(raw_html)
    graph = find_graph_props(source_html)

    if graph is None:
        raise ValueError(f"No NTUMods prerequisite graph found in {input_path}.")

    return clean_prerequisite_graph(graph)

def normalize_saved_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")
    source_lines = soup.select("td.line-content")

    if not source_lines:
        return raw_html

    return "".join(line.get_text() for line in source_lines)

def find_graph_props(source_html: str) -> dict[str, Any] | None:
    for island_tag in re.findall(r"<astro-island\b[^>]*>", source_html, flags=re.DOTALL):
        props_text = extract_attribute(island_tag, "props")
        opts_text = extract_attribute(island_tag, "opts") or ""

        if not props_text:
            continue

        if "ModsPrerequisiteGraph" not in opts_text and '"graph"' not in props_text:
            continue

        props = decode_astro_props(json.loads(props_text))
        graph = props.get("graph")

        if isinstance(graph, dict):
            return graph

    return None

def extract_attribute(tag: str, name: str) -> str | None:
    match = re.search(rf'{name}="(.*?)"', tag, flags=re.DOTALL)
    if match is None:
        return None

    return html.unescape(match.group(1)).replace("\n", " ").replace("\r", " ").replace("\t", " ")

def clean_prerequisite_graph(raw_graph: dict[str, Any]) -> dict[str, dict[str, list[str]]]:
    prerequisite_graph = {}

    for course_code, course_data in raw_graph.items():
        if not isinstance(course_data, dict):
            continue

        prerequisite_graph[course_code] = {
            "prerequisites": course_data.get("requires", []),
            "unlocks": course_data.get("requiredBy", []),
        }

    return dict(sorted(prerequisite_graph.items()))

def write_json(output_path: Path, data: dict[str, dict[str, list[str]]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
