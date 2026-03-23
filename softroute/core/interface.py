from __future__ import annotations

from dataclasses import dataclass

from softroute.utils.ip_utils import parse_ip, parse_network


@dataclass(frozen=True)
class Interface:
    name: str
    ip_address: str
    network: str

    def __post_init__(self) -> None:
        parse_ip(self.ip_address)
        parse_network(self.network)

    def is_in_subnet(self, ip: str) -> bool:
        return parse_ip(ip) in parse_network(self.network)
