import xml.dom.minidom
import csv
import io

def format_config_for_display(filename: str, content_bytes: bytes) -> str:
    """
    Parses and formats file content for clean display in the UI.
    This is for human readability, not for AI analysis.
    """
    try:
        if filename.endswith(".xml"):
            dom = xml.dom.minidom.parseString(content_bytes)
            return dom.toprettyxml()
        
        elif filename.endswith(".csv"):
            decoded = content_bytes.decode("utf-8")
            # For display, just return the decoded content as-is
            return decoded
        
        else:
            return "[Error] Unsupported file format"
            
    except Exception as e:
        return f"[Parse Error] {str(e)}"
