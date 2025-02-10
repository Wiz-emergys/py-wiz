from bs4.element import Tag

def safe_get(element: Tag, selector: str, attribute: str = "text") -> str:
    """Safely extract values from HTML elements"""
    result = element.select_one(selector)
    if result:
        if attribute == "text":
            return result.get_text(strip=True)
        return result.get(attribute, "")
    return ""