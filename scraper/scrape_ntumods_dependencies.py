from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup


DEFAULT_INPUT = Path("data/modules.json")
DEFAULT_OUTPUT = Path("data/ntumods_enriched_modules.json")
NTUMODS_MODULE_URL = "https://ntumods.com/mods/{code}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich module data with NTUMods dependency graph data.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Path to modules.json.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Path to save enriched module JSON.")
    parser.add_argument("--limit", type=int, help="Optional number of modules to scrape for testing.")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests in seconds.")
    args = parser.parse_args()

    modules = load_modules(args.input)
    selected_modules = modules[: args.limit] if args.limit is not None else modules
    enriched_modules = enrich_modules(selected_modules, delay=args.delay)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps({"modules": enriched_modules}, indent=2), encoding="utf-8")
    print(f"Saved {len(enriched_modules)} enriched modules to {args.output}")


def load_modules(input_path: Path) -> list[dict[str, Any]]:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    return data["modules"]


def enrich_modules(modules: list[dict[str, Any]], delay: float) -> list[dict[str, Any]]:
    enriched_modules = []

    for index, module in enumerate(modules, start=1):
        code = module["code"]
        print(f"[{index}/{len(modules)}] Scraping {code}...")

        dependency_data = scrape_dependency_data(code)
        enriched_module = module.copy()
        enriched_module["requires"] = dependency_data["requires"]
        enriched_module["required_by"] = dependency_data["required_by"]

        if dependency_data["error"]:
            enriched_module["dependency_scrape_error"] = dependency_data["error"]

        enriched_modules.append(enriched_module)
        time.sleep(delay)

    return enriched_modules


def scrape_dependency_data(code: str) -> dict[str, Any]:
    url = NTUMODS_MODULE_URL.format(code=code)

    try:
        response = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
    except requests.RequestException as error:
        return empty_dependency_data(error=str(error))

    soup = BeautifulSoup(response.text, "html.parser")
    props = find_dependency_props(soup)

    if props is None:
        return empty_dependency_data(error=f"No dependency props found. HTTP status: {response.status_code}")

    node = props.get("node", {})

    return {
        "requires": node.get("requires", []),
        "required_by": node.get("requiredBy", []),
        "error": None,
    }


def find_dependency_props(soup: BeautifulSoup) -> dict[str, Any] | None:
    for island in soup.find_all("astro-island"):
        props_text = island.get("props")

        if not props_text or '"requires"' not in props_text:
            continue

        try:
            return decode_astro_props(json.loads(props_text))
        except json.JSONDecodeError:
            continue

    return None


def decode_astro_props(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: decode_astro_props(item) for key, item in value.items()}

    if isinstance(value, list) and len(value) == 2 and isinstance(value[0], int):
        marker, nested_value = value

        if marker == 0:
            return decode_astro_props(nested_value)

        if marker == 1 and isinstance(nested_value, list):
            return [decode_astro_props(item) for item in nested_value]

    if isinstance(value, list):
        return [decode_astro_props(item) for item in value]

    return value


def empty_dependency_data(error: str) -> dict[str, Any]:
    return {
        "requires": [],
        "required_by": [],
        "error": error,
    }


if __name__ == "__main__":
    main()
