import json
from typing import Any


def _to_json_safe(obj: Any) -> Any:
    if hasattr(obj, "model_dump"):
        return obj.model_dump()

    if isinstance(obj, dict):
        return {key: _to_json_safe(value) for key, value in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [_to_json_safe(item) for item in obj]

    return obj


def print_agent_result_json(
    agent_result: Any,
    *,
    indent: int = 2,
    sort_keys: bool = False,
) -> None:
    json_safe = _to_json_safe(agent_result)

    print(
        json.dumps(
            json_safe,
            indent=indent,
            sort_keys=sort_keys,
            ensure_ascii=False,
        )
    )
