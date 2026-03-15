import html
from typing import Optional, Union

def sanitize_text(text: Optional[str]) -> Optional[str]:
    """
    Escapes HTML characters to prevent XSS.
    Converts <, >, &, ", and ' to HTML entities.
    """
    if text is None:
        return None
    return html.escape(text)

def sanitize_object(obj: Union[dict, list, str, None]) -> Union[dict, list, str, None]:
    """Recursively sanitizes values in a dictionary or list."""
    if isinstance(obj, str):
        return sanitize_text(obj)
    if isinstance(obj, dict):
        return {k: sanitize_object(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_object(item) for item in obj]
    return obj
