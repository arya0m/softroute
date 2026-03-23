from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from softroute.utils.ip_utils import parse_ip


@dataclass
class Packet:
    src_ip: str
    dest_ip: str
    payload: Optional[bytes] = None
    ttl: int = 64
    path: List[str] = field(default_factory=list)

    def validate(self) -> None:
        parse_ip(self.src_ip)
        parse_ip(self.dest_ip)
        if self.ttl <= 0:
            raise ValueError("TTL must be greater than 0")

    def decrement_ttl(self) -> None:
        self.ttl -= 1

    def is_expired(self) -> bool:
        return self.ttl <= 0
