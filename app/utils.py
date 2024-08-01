from typing import Any, Mapping


def serialize(obj: Any) -> Any:
    """Recursively serialize an object to a JSON-compatible format."""
    if isinstance(obj, Mapping):
        return {key: serialize(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [serialize(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        return serialize(obj.__dict__)
    else:
        return obj