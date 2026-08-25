from __future__ import annotations

from sqlalchemy import String, cast, or_
from sqlalchemy.orm import Session

from backend.models import ModuleModel, ModulePrerequisiteModel
from backend.schemas.module import ModuleFilterOptionsResponse, ModuleListResponse, ModuleSummary


def list_modules(
    db: Session,
    search: str | None = None,
    faculty: str | None = None,
    level: int | None = None,
    category: str | None = None,
    current_only: bool = False,
    limit: int = 30,
    offset: int = 0,
) -> ModuleListResponse:
    query = db.query(ModuleModel)

    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(or_(ModuleModel.code.ilike(search_pattern), ModuleModel.title.ilike(search_pattern)))

    if faculty:
        query = query.filter(ModuleModel.faculty == faculty)

    if level is not None:
        query = query.filter(ModuleModel.level == level)

    if category:
        query = query.filter(cast(ModuleModel.categories, String).ilike(f'%"{category.strip()}"%'))

    if current_only:
        query = query.filter(ModuleModel.is_current_semester.is_(True))

    total = query.count()
    modules = query.order_by(ModuleModel.code).offset(offset).limit(limit).all()
    module_codes = [module.code for module in modules]

    prerequisites_by_module = get_prerequisites_by_module(db, module_codes)
    unlocks_by_module = get_unlocks_by_module(db, module_codes)

    return ModuleListResponse(
        items=[
            build_module_summary(
                module=module,
                prerequisites=prerequisites_by_module.get(module.code, []),
                unlocks=unlocks_by_module.get(module.code, []),
            )
            for module in modules
        ],
        total=total,
        limit=limit,
        offset=offset,
    )


def get_module_by_code(db: Session, code: str) -> ModuleSummary | None:
    module = db.query(ModuleModel).filter(ModuleModel.code == code.upper()).first()

    if module is None:
        return None

    prerequisites = get_prerequisites_by_module(db, [module.code]).get(module.code, [])
    unlocks = get_unlocks_by_module(db, [module.code]).get(module.code, [])

    return build_module_summary(module=module, prerequisites=prerequisites, unlocks=unlocks)


def get_prerequisites_by_module(db: Session, module_codes: list[str]) -> dict[str, list[str]]:
    prerequisites_by_module = {module_code: [] for module_code in module_codes}

    if not module_codes:
        return prerequisites_by_module

    rows = (
        db.query(ModulePrerequisiteModel.module_code, ModulePrerequisiteModel.prerequisite_code)
        .filter(ModulePrerequisiteModel.module_code.in_(module_codes))
        .order_by(ModulePrerequisiteModel.module_code, ModulePrerequisiteModel.prerequisite_code)
        .all()
    )

    for module_code, prerequisite_code in rows:
        prerequisites_by_module[module_code].append(prerequisite_code)

    return prerequisites_by_module

def get_unlocks_by_module(db: Session, module_codes: list[str]) -> dict[str, list[str]]:
    unlocks_by_module = {module_code: [] for module_code in module_codes}

    if not module_codes:
        return unlocks_by_module

    rows = (
        db.query(ModulePrerequisiteModel.prerequisite_code, ModulePrerequisiteModel.module_code)
        .filter(ModulePrerequisiteModel.prerequisite_code.in_(module_codes))
        .order_by(ModulePrerequisiteModel.prerequisite_code, ModulePrerequisiteModel.module_code)
        .all()
    )

    for prerequisite_code, unlocked_module_code in rows:
        unlocks_by_module[prerequisite_code].append(unlocked_module_code)

    return unlocks_by_module

def build_module_summary(module: ModuleModel, prerequisites: list[str], unlocks: list[str]) -> ModuleSummary:
    return ModuleSummary(
        code=module.code,
        title=module.title,
        au=module.au,
        faculty=module.faculty,
        description=module.description,
        level=module.level,
        categories=module.categories or [],
        latest_year=module.latest_year,
        latest_semester=module.latest_semester,
        is_current_semester=module.is_current_semester,
        not_available_to_programme=module.not_available_to_programme,
        prerequisites=prerequisites,
        unlocks=unlocks,
        prerequisite_count=len(prerequisites),
        unlock_count=len(unlocks),
    )


def get_module_filter_options(db: Session) -> ModuleFilterOptionsResponse:
    faculties = [
        faculty
        for (faculty,) in db.query(ModuleModel.faculty)
        .filter(ModuleModel.faculty.isnot(None), ModuleModel.faculty != "")
        .distinct()
        .order_by(ModuleModel.faculty)
        .all()
    ]
    levels = [
        level
        for (level,) in db.query(ModuleModel.level)
        .filter(ModuleModel.level.isnot(None))
        .distinct()
        .order_by(ModuleModel.level)
        .all()
    ]
    categories = sorted(
        {
            category
            for (module_categories,) in db.query(ModuleModel.categories).all()
            for category in (module_categories or [])
            if category
        }
    )

    return ModuleFilterOptionsResponse(faculties=faculties, levels=levels, categories=categories)
