from __future__ import annotations

from ipaddress import IPv4Address, IPv4Network, ip_address, ip_network


def parse_ip(value: str) -> IPv4Address:
    try:
        parsed = ip_address(value)
    except ValueError as exc:
        raise ValueError(f"Invalid IP address: {value}") from exc
    if parsed.version != 4:
        raise ValueError(f"Only IPv4 is supported: {value}")
    return parsed


def parse_network(value: str) -> IPv4Network:
    try:
        parsed = ip_network(value, strict=False)
    except ValueError as exc:
        raise ValueError(f"Invalid network: {value}") from exc
    if parsed.version != 4:
        raise ValueError(f"Only IPv4 networks are supported: {value}")
    return parsed
