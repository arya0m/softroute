from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from softroute.core.route import Route
from softroute.utils.ip_utils import parse_ip, parse_network


@dataclass
class RoutingTable:
    routes: List[Route] = field(default_factory=list)

    def add_route(self, network: str, next_hop: str | None, interface: str | None = None, metric: int = 1) -> Route:
        route = Route(network=network, next_hop=next_hop, interface=interface, metric=metric)
        self.routes.append(route)
        return route

    def remove_route(self, network: str, next_hop: str | None = None) -> int:
        before = len(self.routes)
        self.routes = [
            route for route in self.routes
            if not (route.network == network and (next_hop is None or route.next_hop == next_hop))
        ]
        return before - len(self.routes)

    def find_best_match(self, ip: str) -> Optional[Route]:
        target = parse_ip(ip)
        matches = [route for route in self.routes if target in parse_network(route.network)]
        if not matches:
            return None
        matches.sort(key=lambda route: (-route.prefix_length, route.metric, route.network))
        return matches[0]

    def __len__(self) -> int:
        return len(self.routes)
