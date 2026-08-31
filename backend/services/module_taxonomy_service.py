from __future__ import annotations

import re
from dataclasses import dataclass

@dataclass(frozen=True)
class TaxonomyRule:
    tag: str
    keywords: tuple[str, ...]

TAXONOMY_RULES = (
    TaxonomyRule(
        tag="software-engineering",
        keywords=(
            "software",
            "object oriented",
            "programming",
            "development",
            "design pattern",
            "testing",
            "requirements",
        ),
    ),
    TaxonomyRule(
        tag="web-development",
        keywords=("web", "internet", "frontend", "backend", "full stack", "mobile application"),
    ),
    TaxonomyRule(
        tag="data",
        keywords=("data", "database", "analytics", "visualisation", "visualization", "mining"),
    ),
    TaxonomyRule(
        tag="ai-ml",
        keywords=("artificial intelligence", "machine learning", "neural", "deep learning", "ai"),
    ),
    TaxonomyRule(
        tag="systems",
        keywords=("system", "operating", "distributed", "cloud", "parallel", "network"),
    ),
    TaxonomyRule(
        tag="security",
        keywords=("security", "cryptography", "privacy", "forensics", "malware"),
    ),
    TaxonomyRule(
        tag="hardware",
        keywords=("hardware", "circuit", "microprocessor", "embedded", "computer organisation"),
    ),
    TaxonomyRule(
        tag="business",
        keywords=("business", "entrepreneur", "management", "innovation", "marketing", "finance"),
    ),
    TaxonomyRule(
        tag="math",
        keywords=("mathematics", "statistics", "probability", "linear algebra", "calculus"),
    ),
    TaxonomyRule(
        tag="communication",
        keywords=("communication", "writing", "presentation", "language", "professional"),
    ),
)

def build_curated_taxonomy_tags(code: str, title: str, description: str | None) -> list[str]:
    searchable_text = normalize_taxonomy_text(f"{code} {title} {description or ''}")

    return [
        rule.tag
        for rule in TAXONOMY_RULES
        if any(keyword in searchable_text for keyword in rule.keywords)
    ]

def merge_module_categories(existing_categories: list[str], taxonomy_tags: list[str]) -> list[str]:
    merged_categories: list[str] = []
    seen_categories: set[str] = set()

    for category in [*existing_categories, *taxonomy_tags]:
        normalized_category = category.strip()

        if not normalized_category or normalized_category.lower() in seen_categories:
            continue

        merged_categories.append(normalized_category)
        seen_categories.add(normalized_category.lower())

    return merged_categories

def normalize_taxonomy_text(text: str) -> str:
    normalized_text = text.lower().replace("&", " and ")
    normalized_text = re.sub(r"[^a-z0-9]+", " ", normalized_text)

    return " ".join(normalized_text.split())
