from __future__ import annotations

from collections import defaultdict

import httpx

from app.config import CATEGORY_CODES, settings

CANDIDATE_LABELS = {
    "office": "office work and documents",
    "study": "study and online learning",
    "programming": "programming and software development",
    "gaming": "computer gaming",
    "video_editing": "video editing and motion graphics",
    "design_3d": "3d design and modeling",
}

KEYWORDS = {
    "office": [
        "word",
        "excel",
        "browser",
        "office",
        "docs",
        "document",
        "ворд",
        "офис",
        "браузер",
        "документ",
        "таблица",
    ],
    "study": [
        "study",
        "university",
        "college",
        "school",
        "lessons",
        "learning",
        "учеб",
        "университет",
        "школ",
        "заняти",
        "обуч",
    ],
    "programming": [
        "code",
        "coding",
        "programming",
        "developer",
        "backend",
        "docker",
        "python",
        "java",
        "программ",
        "разработ",
        "докер",
        "код",
    ],
    "gaming": [
        "game",
        "gaming",
        "cs2",
        "dota",
        "fps",
        "steam",
        "кс",
        "дота",
        "игр",
        "гейм",
    ],
    "video_editing": [
        "premiere",
        "davinci",
        "video",
        "editing",
        "after effects",
        "монтаж",
        "видео",
        "эдит",
        "рилс",
    ],
    "design_3d": [
        "blender",
        "3d",
        "maya",
        "cad",
        "render",
        "modeling",
        "дизайн",
        "3д",
        "блендер",
        "рендер",
    ],
}


async def classify_query(query: str) -> dict:
    query = (query or "").strip()
    if not query:
        return _format_result("office", {code: 0.0 for code in CATEGORY_CODES})

    if settings.huggingface_api_key:
        result = await _classify_with_hf(query)
        if result:
            return result

    return _classify_with_keywords(query)


async def _classify_with_hf(query: str) -> dict | None:
    url = f"https://api-inference.huggingface.co/models/{settings.hf_model}"
    headers = {"Authorization": f"Bearer {settings.huggingface_api_key}"}
    payload = {
        "inputs": query,
        "parameters": {
            "candidate_labels": list(CANDIDATE_LABELS.values()),
            "multi_label": False,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                return None
            data = response.json()
    except Exception:
        return None

    labels = data.get("labels", [])
    scores = data.get("scores", [])
    if not labels or not scores:
        return None

    mapped_scores: dict[str, float] = {code: 0.0 for code in CATEGORY_CODES}
    reverse = {v: k for k, v in CANDIDATE_LABELS.items()}

    for label, score in zip(labels, scores):
        code = reverse.get(label)
        if code:
            mapped_scores[code] = round(float(score), 4)

    predicted = max(mapped_scores, key=mapped_scores.get)
    return _format_result(predicted, mapped_scores)


def _classify_with_keywords(query: str) -> dict:
    q = query.lower()
    score_map = defaultdict(float)

    for category, keywords in KEYWORDS.items():
        for kw in keywords:
            if kw in q:
                score_map[category] += 1.0

    if not score_map:
        score_map["office"] = 1.0

    total = sum(score_map.values()) or 1.0
    normalized = {code: round(score_map.get(code, 0.0) / total, 4) for code in CATEGORY_CODES}
    predicted = max(normalized, key=normalized.get)
    return _format_result(predicted, normalized)


def _format_result(category: str, scores: dict[str, float]) -> dict:
    return {"category": category, "scores": {code: float(scores.get(code, 0.0)) for code in CATEGORY_CODES}}
