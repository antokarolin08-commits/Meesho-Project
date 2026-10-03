def alias_for(reseller_id: str) -> str:
    """
    Transforms raw reseller ID into a privacy-safe alias.
    Example: RS019 -> ALIAS-19, RS006 -> ALIAS-06
    """
    if not reseller_id.startswith("RS"):
        return reseller_id
    num_part = reseller_id[2:]  # strips 'RS'
    # Retain standard two-digit alias format or strip leading single zero if needed:
    # Acceptance specifies: RS019 -> ALIAS-19, RS006 -> ALIAS-06
    return f"ALIAS-{int(num_part):02d}"


def assert_no_raw_names_leak(text: str, reseller_names: list[str]) -> bool:
    """
    Returns False if any raw reseller_name string appears verbatim in text.
    Returns True only if the text is completely clean of raw reseller identities.
    """
    for name in reseller_names:
        if name and name in text:
            return False
    return True