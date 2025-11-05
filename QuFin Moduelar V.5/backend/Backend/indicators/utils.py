from typing import Union


def convert_to_float(value: Union[str, int, bool]) -> Union[float, None]:
    try:
        return float(value)
    except Exception:
        return None
