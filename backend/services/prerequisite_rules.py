from typing import Optional

# Each outer tuple is an OR alternative; every member of an inner tuple is required (AND).
# This is a reviewed course-prerequisite policy, not a parser for merged catalog text.
# Offering, standing, co-requisites and registration permissions remain separate constraints.
PrerequisiteGroups = tuple[tuple[str, ...], ...]

# Local NTU MPE list: data/Transcript and Curriculum Guide/MPE 2025.pdf,
# pages 1-2, marked "As of 14/7/2026", AY2025 and later cohorts.
# The request has no authenticated cohort metadata; this current listing is the bounded
# elective policy. Do not claim it proves historical or future cohort registration eligibility.
REVIEWED_MPE_PREREQUISITES: dict[str, PrerequisiteGroups] = {
    "SC3000": (("SC1007", "SC2000"), ("SC1007", "MH2500")),
    "SC3010": (("SC2005",),),
    "SC3020": (("SC2207",),),
    "SC3021": (("SC1003",),),
    "SC3030": (("SC2008",),),
    "SC3040": (("SC2006",),),
    "SC3050": (("SC1006",),),
    "SC3270": (("SC2001",), ("SC2301",), ("MH1403", "MH1812")),
    "SC3271": (("SC2203", "MH1812"), ("SC2203", "SC1124"), ("SC1124", "MH4302"), ("MH1812", "MH4302")),
    "SC4000": (("SC1004", "SC1007", "SC2000"), ("SC1007", "MH2500")),
    "SC4001": (("SC1004", "SC1007"), ("MH2802", "SC1007")),
    "SC4002": (("SC2001",), ("MH1403",)),
    "SC4003": (("SC1007", "SC2000"), ("SC1007", "MH2500")),
    "SC4010": (("SC2000",), ("MH2500",)),
    "SC4011": (("SC2006",),),
    "SC4012": (("SC2002", "SC2005"),),
    "SC4013": (("SC2005", "SC2008"),),
    "SC4014": (("SC1006", "SC2005"),),
    "SC4015": (("SC1006",),),
    "SC4017": (("SC2000", "SC2001"),),
    "SC4020": (("SC2001",), ("MH1403",)),
    "SC4021": (("SC2001",), ("MH1403",)),
    "SC4022": (("SC2001",), ("MH1403",)),
    "SC4023": (("SC2207",),),
    "SC4024": (("SC1003", "MH2500"), ("SC1003", "SC2000")),
    "SC4025": (("SC2006",),),
    "SC4030": (("SC2008",),),
    "SC4031": (("SC2008",),),
    "SC4040": (("SC2001",),),
    "SC4050": (("SC2001",),),
    "SC4051": (("SC2005", "SC2008"),),
    "SC4052": (("SC1004",), ("MH2802",)),
    "SC4053": (("SC1007", "SC2001"),),
    "SC4054": (("SC1007", "SC2000"),),
    "SC4055": (("SC1003", "SC1004", "SC2000"), ("SC1003", "SC2000", "MH2802"), ("SC1003", "SC1004", "MH2500")),
    "SC4062": (("SC4001", "SC4002"),),
    "SC4063": (("SC2005", "SC2008"),),
    "SC4064": (("SC2001", "SC2005"),),
    "SC4172": (("SC2107",),),
    "SC4242": (("SC2001", "SC2006"),),
}

# CSC 2324 Curriculum Guide.pdf p1 and CSC 2627 Curriculum Guide.pdf p1 agree
# on SC2001, SC2005, SC2008 and the Nil rows below. SC2002's OR rule comes only
# from the older guide; SC2003 is distinct and must not be inferred equivalent.
REVIEWED_CORE_PREREQUISITES: dict[str, PrerequisiteGroups] = {
    "SC2001": (("SC1007", "MH1812"),),
    "SC2002": (("SC1003",), ("SC1007",)),
    "SC2005": (("SC1006", "SC1007"),),
    "SC2008": (("SC2000", "SC1004"),),
    "SC1005": ((),),
    "MH1812": ((),),
}

# Previously reviewed old/new code pairs: titles and mutual-exclusion source support
# these pairs. No other title-based substitution is allowed, including SC1004/MH2802.
PREREQUISITE_EQUIVALENTS = {
    "CZ2007": "SC2207",
    "SC2207": "CZ2007",
    "CZ2101": "SC2001",
    "SC2001": "CZ2101",
}

# MPE 2025.pdf p2 explicitly says "TBC (Pending Approval)". A stored singleton
# cannot resolve that pending source requirement, so this candidate stays excluded.
UNRESOLVED_PREREQUISITE_COURSES = {"SC3103"}

def get_reviewed_prerequisite_groups(course_code: str) -> Optional[PrerequisiteGroups]:
    code = course_code.upper()
    return REVIEWED_MPE_PREREQUISITES.get(code, REVIEWED_CORE_PREREQUISITES.get(code))

# Unreviewed multiple codes are ambiguous unions. An explicitly loaded empty graph
# only establishes that no direct course prerequisite was stored, not academic eligibility.
def get_prerequisite_groups(
    course_code: str,
    graph_prerequisites: Optional[list[str]],
) -> Optional[PrerequisiteGroups]:
    if course_code.upper() in UNRESOLVED_PREREQUISITE_COURSES:
        return None

    reviewed = get_reviewed_prerequisite_groups(course_code)
    if reviewed is not None:
        return reviewed
    if graph_prerequisites is None:
        return None

    codes = tuple(sorted({code.upper() for code in graph_prerequisites}))
    if len(codes) > 1:
        return None

    return (codes,)
