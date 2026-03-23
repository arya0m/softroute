from __future__ import annotations

from dataclasses import dataclass

from softroute.utils.ip_utils import parse_network


@dataclass(frozen=True)
class Route:
    network: str
    next_hop: str | None
    interface: str | None = None
    metric: int = 1

    def __post_init__(self) -> None:
        parse_network(self.network)
        if self.metric < 0:
            raise ValueError("metric must be >= 0")

    @property
    def prefix_length(self) -> int:
        return parse_network(self.network).prefixlen
