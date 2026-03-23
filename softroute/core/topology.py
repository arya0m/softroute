from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from softroute.core.interface import Interface
from softroute.core.router import Router
from softroute.utils.ip_utils import parse_ip


@dataclass
class Link:
    router_a: str
    iface_a: str
    router_b: str
    iface_b: str


@dataclass
class Topology:
    routers: Dict[str, Router] = field(default_factory=dict)
    links: List[Link] = field(default_factory=list)

    def add_router(self, router: Router) -> None:
        self.routers[router.router_id] = router

    def get_router(self, router_id: str) -> Router:
        return self.routers[router_id]

    def connect(self, router_a: str, iface_a: str, router_b: str, iface_b: str) -> None:
        if router_a not in self.routers or router_b not in self.routers:
            raise ValueError("Both routers must exist before connecting")
        self.links.append(Link(router_a=router_a, iface_a=iface_a, router_b=router_b, iface_b=iface_b))

    def resolve_next_router(self, current_router_id: str, next_hop: str) -> Optional[Router]:
        parse_ip(next_hop)
        for link in self.links:
            if link.router_a == current_router_id:
                neighbor = self.routers[link.router_b]
                iface = neighbor.interfaces[link.iface_b]
                if iface.ip_address == next_hop:
                    return neighbor
            elif link.router_b == current_router_id:
                neighbor = self.routers[link.router_a]
                iface = neighbor.interfaces[link.iface_a]
                if iface.ip_address == next_hop:
                    return neighbor
        return None

    def find_ingress_router(self, src_ip: str) -> Optional[Router]:
        for router in self.routers.values():
            if router.has_direct_delivery(src_ip):
                return router
        return None

    @classmethod
    def from_dict(cls, payload: dict) -> 'Topology':
        topology = cls()
        for router_data in payload.get('routers', []):
            router = Router(router_id=router_data['id'])
            for iface_data in router_data.get('interfaces', []):
                router.add_interface(
                    Interface(
                        name=iface_data['name'],
                        ip_address=iface_data['ip_address'],
                        network=iface_data['network'],
                    )
                )
            for route_data in router_data.get('routes', []):
                router.add_route(
                    network=route_data['network'],
                    next_hop=route_data.get('next_hop'),
                    interface=route_data.get('interface'),
                    metric=route_data.get('metric', 1),
                )
            topology.add_router(router)

        for link_data in payload.get('links', []):
            topology.connect(
                router_a=link_data['router_a'],
                iface_a=link_data['iface_a'],
                router_b=link_data['router_b'],
                iface_b=link_data['iface_b'],
            )
        return topology
