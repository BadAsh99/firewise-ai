import xmltodict

def extract_summary(xml_bytes):
    """
    Extract the <config> section from the PAN-OS XML config.

    Args:
        xml_bytes (bytes): Raw bytes from uploaded XML file.

    Returns:
        dict: Parsed config dictionary, or error message.
    """
    try:
        parsed = xmltodict.parse(xml_bytes)
        return parsed.get("config", {})
    except Exception as e:
        return {"error": str(e)}
