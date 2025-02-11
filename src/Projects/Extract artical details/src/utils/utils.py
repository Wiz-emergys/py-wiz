from bs4.element import Tag

def safe_get(element: Tag, selector: str, attribute: str = "text") -> str:
    
    """
    Safely extract a value from an HTML element.

    Parameters:
        element (bs4.element.Tag): The element to extract from.
        selector (str): The CSS selector to use to extract the element.
        attribute (str): The attribute to extract from the element. Defaults to "text".

    Returns:
        str: The extracted value, or empty string if the element or attribute is not found.
    """
    result = element.select_one(selector)
    if result:
        if attribute == "text":
            return result.get_text(strip=True)
        return result.get(attribute, "")
    return ""