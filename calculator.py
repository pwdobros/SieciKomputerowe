import sys

def ip_to_int(ip_str):
    parts = ip_str.split('.')
    if len(parts) != 4:
        raise ValueError("Invalid IP format")
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])