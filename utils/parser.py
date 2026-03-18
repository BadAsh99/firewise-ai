import xmltodict
import json
import re

# --- Sanitization Helpers ---

def _scrub_text(text):
    """
    Uses regular expressions to find and replace sensitive PII in a block of text.
    """
    # Scrub emails
    text = re.sub(r'[\w\.\-]+@[\w\.\-]+', '[EMAIL_REMOVED]', text)
    # Scrub phone numbers (basic formats)
    text = re.sub(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', '[PHONE_REMOVED]', text)
    # Scrub password hashes (common PAN-OS format)
    text = re.sub(r'\$1\$.{28}', '[HASH_REMOVED]', text)
    return text

def _anonymize_ips(text):
    """
    Finds all IPv4 addresses and replaces them with numbered, generic placeholders.
    """
    ip_map = {}
    
    def replace(match):
        ip = match.group(0)
        # Check if it's a private IP
        is_private = ip.startswith(('10.', '172.', '192.168.'))
        prefix = 'PRIVATE_IP_' if is_private else 'PUBLIC_IP_'
        
        # If we haven't seen this IP before, add it to our map
        if ip not in ip_map:
            ip_map[ip] = f'[{prefix}{len(ip_map) + 1}]'
        
        return ip_map[ip]

    # Regex to find all IPv4 addresses
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    return re.sub(ip_pattern, replace, text)


# --- Main Parser Function ---

def extract_config_summary(xml_content):
    """
    Extracts, sanitizes, and summarizes the PAN-OS XML configuration.
    """
    try:
        parsed_dict = xmltodict.parse(xml_content)
        
        # Isolate the main config section
        if "response" in parsed_dict and "result" in parsed_dict["response"]:
            config_section = parsed_dict["response"]["result"].get("config")
        else:
            config_section = parsed_dict.get("config")

        if not config_section:
            return json.dumps({"error": "No <config> section found in the XML file."})

        # 1. Convert the relevant dictionary section to a JSON string
        json_string = json.dumps(config_section, indent=2)

        # 2. Sanitize the entire string
        sanitized_string = _scrub_text(json_string)
        sanitized_string = _anonymize_ips(sanitized_string)

        # 3. Return the sanitized string for AI analysis
        return sanitized_string
        
    except Exception as e:
        return json.dumps({"error": f"Failed to parse XML: {str(e)}"})