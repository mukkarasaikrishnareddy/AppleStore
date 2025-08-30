def require_fields(data: dict, fields: list[str]):
    missing = [f for f in fields if f not in data or data[f] in (None, "")]
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}")
