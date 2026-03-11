import sys

def ip_to_int(ip_str):
    """Convert IP address string to integer"""
    parts = ip_str.split('.')
    if len(parts) != 4:
        raise ValueError("Invalid IP format")
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])

def int_to_ip(ip_int):
    """Convert integer to IP address string"""
    return f"{(ip_int >> 24) & 255}.{(ip_int >> 16) & 255}.{(ip_int >> 8) & 255}.{ip_int & 255}"

def int_to_binary(ip_int):
    """Convert integer to 32-bit binary string"""
    return bin(ip_int)[2:].zfill(32)

def calculate_netmask(prefix):
    """Calculate subnet mask from prefix length"""
    if prefix < 0 or prefix > 32:
        raise ValueError("Prefix must be between 0 and 32")
    return (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF

def ip_calculator(cidr_notation):
    """Calculate IPv4 network information from CIDR notation"""
    
    if '/' not in cidr_notation:
        raise ValueError("Invalid CIDR format. Use IP/prefix (e.g., 192.168.1.0/24)")
    
    ip_part, prefix_str = cidr_notation.split('/')
    try:
        prefix = int(prefix_str)
    except ValueError:
        raise ValueError("Prefix must be a number")
    
    ip_int = ip_to_int(ip_part)
    
    netmask = calculate_netmask(prefix)
    
    network_int = ip_int & netmask
    
    broadcast_int = network_int | (~netmask & 0xFFFFFFFF)
    
    if prefix == 31:
        first_host_int = network_int
        last_host_int = broadcast_int
        num_hosts = 2
    elif prefix == 32:
        first_host_int = network_int
        last_host_int = network_int
        num_hosts = 1
    else:
        first_host_int = network_int + 1
        last_host_int = broadcast_int - 1
        num_hosts = (broadcast_int - network_int - 1)
    
    print(f"CIDR Notation: {cidr_notation}\n")
    
    print("Network Address:")
    print(f"  Binary:  {int_to_binary(network_int)}")
    print(f"  Decimal: {int_to_ip(network_int)}\n")
    
    print("Subnet Mask:")
    print(f"  Binary:  {int_to_binary(netmask)}")
    print(f"  Decimal: {int_to_ip(netmask)}\n")
    
    print(f"Number of Hosts: {num_hosts}\n")
    
    print("First Host IP:")
    print(f"  Binary:  {int_to_binary(first_host_int)}")
    print(f"  Decimal: {int_to_ip(first_host_int)}\n")
    
    print("Last Host IP:")
    print(f"  Binary:  {int_to_binary(last_host_int)}")
    print(f"  Decimal: {int_to_ip(last_host_int)}\n")
    
    print("Broadcast Address:")
    print(f"  Binary:  {int_to_binary(broadcast_int)}")
    print(f"  Decimal: {int_to_ip(broadcast_int)}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculatorip.py <IP/prefix>")
        print("Example: python calculatorip.py 192.168.1.0/24")
        sys.exit(1)
    
    try:
        ip_calculator(sys.argv[1])
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)