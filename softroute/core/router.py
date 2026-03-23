from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from softroute.core.interface import Interface
from softroute.core.packet import Packet
from softroute.core.route import Route
from softroute.core.routing_table import RoutingTable
from softroute.utils.ip_utils import parse_ip


@dataclass
class Router:
    router_id: str
    interfaces: Dict[str, Interface] = field(default_factory=dict)
    routing_table: RoutingTable = field(default_factory=RoutingTable)

    def add_interface(self, interface: Interface) -> None:
        self.interfaces[interface.name] = interface

    def add_route(self, network: str, next_hop: str | None, interface: str | None = None, metric: int = 1) -> Route:
        return self.routing_table.add_route(network=network, next_hop=next_hop, interface=interface, metric=metric)

    def lookup_route(self, dest_ip: str) -> Optional[Route]:
        parse_ip(dest_ip)
        return self.routing_table.find_best_match(dest_ip)

    def has_direct_delivery(self, dest_ip: str) -> bool:
        return any(interface.is_in_subnet(dest_ip) for interface in self.interfaces.values())

    def directly_connected_networks(self) -> List[str]:
        return [interface.network for interface in self.interfaces.values()]

    def forward_decision(self, packet: Packet) -> Optional[Route]:
        return self.lookup_route(packet.dest_ip)
