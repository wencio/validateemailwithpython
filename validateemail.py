import re
from typing import Dict

def validate_name(name: str, min_length: int, max_length: int) -> None:
    """
    Validates a name according to specified rules and raises ValueError on validation failure.
    """
    name = name.strip()  # Remove leading and trailing spaces
    
    if len(name) < min_length:
        raise ValueError(f"{name} is too short. Minimum length is {min_length} characters")
    
    if len(name) > max_length:
        raise ValueError(f"{name} is too long. Maximum length is {max_length} characters")

def validate_email_addr(email_addr: str) -> bool:
    """
    Returns True if the email_addr is valid per specification. Otherwise, raises ValueError.
    """
    # Remove leading and trailing spaces
    email_addr = email_addr.strip()

    # Total length of email too long.
    if len(email_addr) > 254:
        raise ValueError("Email address is too long")

    # Split email address into local part and domain
    local_part, domain = email_addr.split('@', 1)

    # Check the length of local part and domain
    if len(local_part) > 64:
        raise ValueError("Local part of email address is too long")
    
    if len(domain) > 251:
        raise ValueError("Domain part of email address is too long")

    # Validate characters in local part and domain
    if not re.match(r'^[a-zA-Z0-9@_]+$', local_part):
        raise ValueError("Invalid characters in local part of email address")

    if not re.match(r'^[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*$', domain):
        raise ValueError("Invalid characters or structure in domain part of email address")

    # Hyphens and dots cannot occur as the first or last characters in the local part
    if local_part.startswith('-') or local_part.endswith('-'):
        raise ValueError("Hyphens cannot be the first or last characters in the local part of email address")

    # Periods (.) can only occur in the TLD part of the domain
    if '.' in domain[:-1]:
        raise ValueError("Periods are not allowed aside from the TLD part of the domain")

    # Email address must end in ".com", ".net", or ".org"
    if not domain.endswith((".com", ".net", ".org")):
        raise ValueError("Email address must end in '.com', '.net', or '.org'")

    return True

def validate_html(html: str) -> None:
    """
    Validates the HTML according to specified rules and raises ValueError on validation failure.
    """
    if not html:
        raise ValueError("HTML content is empty")

def validate_replacements(html: str, replacements: Dict) -> None:
    """
    Validates replacements according to specified rules and raises ValueError on validation failure.
    """
    # Extract tags in the HTML content
    html_tags = re.findall(r'\{([^}]+)\}', html)

    # Check if replacements are non-empty and match the tags in the HTML
    for tag in html_tags:
        if tag not in replacements:
            raise ValueError(f"Replacement key '{tag}' not found in replacements")
        if not replacements[tag]:
            raise ValueError(f"Replacement value for key '{tag}' is empty")

    # Check for surplus replacement keys not used in HTML
    surplus_keys = set(replacements.keys()) - set(html_tags)
    if surplus_keys:
        raise ValueError(f"Surplus replacement keys: {', '.join(surplus_keys)}")

def validate_email_payload(sender_name: str, sender_addr: str, receiver_name: str, receiver_addr: str, html: str,
                           replacements: Dict) -> bool:
    """
    Returns True if the payload is validated and is safe to send out. Otherwise, raises ValueError.
    """
    validate_name(sender_name, min_length=5, max_length=30)
    validate_name(receiver_name, min_length=5, max_length=60)

    if not validate_email_addr(sender_addr):
        raise ValueError("Invalid sender email address")

    if not validate_email_addr(receiver_addr):
        raise ValueError("Invalid receiver email address")

    # Validate HTML and replacements
    validate_html(html)
    validate_replacements(html, replacements)

    return True
