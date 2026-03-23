from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from softroute.core.packet import Packet
from softroute.core.topology import Topology
from softroute.utils.logger import TraceLogger


@dataclass
class SimulationResult:
    status: str
    message: str
    path: List[str]
    ttl_remaining: int
    logs: list


class SimulationEngine:
    def __init__(self, topology: Topology) -> None:
        self.topology = topology
        self.logger = TraceLogger()

    def simulate(self, packet: Packet, start_router_id: str | None = None) -> SimulationResult:
        packet.validate()
        current = self.topology.get_router(start_router_id) if start_router_id else self.topology.find_ingress_router(packet.src_ip)
        if current is None:
            return SimulationResult(
                status='ERROR',
                message='Could not determine ingress router for source IP',
                path=packet.path,
                ttl_remaining=packet.ttl,
                logs=self.logger.to_dict(),
            )

        visited = set()
        while True:
            if packet.is_expired():
                self.logger.log(current.router_id, 'TTL_EXPIRED', ttl=packet.ttl)
                return SimulationResult(
                    status='TTL_EXPIRED',
                    message='Packet TTL expired before delivery',
                    path=packet.path,
                    ttl_remaining=packet.ttl,
                    logs=self.logger.to_dict(),
                )

            if current.router_id in visited:
                self.logger.log(current.router_id, 'ROUTING_LOOP', path=list(packet.path))
                return SimulationResult(
                    status='ROUTING_LOOP',
                    message='Routing loop detected',
                    path=packet.path,
                    ttl_remaining=packet.ttl,
                    logs=self.logger.to_dict(),
                )
            visited.add(current.router_id)
            packet.path.append(current.router_id)

            if current.has_direct_delivery(packet.dest_ip):
                self.logger.log(current.router_id, 'DELIVERED', dest_ip=packet.dest_ip)
                return SimulationResult(
                    status='DELIVERED',
                    message=f'Packet delivered by router {current.router_id}',
                    path=packet.path,
                    ttl_remaining=packet.ttl,
                    logs=self.logger.to_dict(),
                )

            route = current.forward_decision(packet)
            if route is None:
                self.logger.log(current.router_id, 'NO_ROUTE', dest_ip=packet.dest_ip)
                return SimulationResult(
                    status='NO_ROUTE',
                    message=f'No route to destination {packet.dest_ip} from {current.router_id}',
                    path=packet.path,
                    ttl_remaining=packet.ttl,
                    logs=self.logger.to_dict(),
                )

            if route.next_hop is None:
                self.logger.log(current.router_id, 'NEXT_HOP_MISSING', route=route.network)
                return SimulationResult(
                    status='NO_ROUTE',
                    message=f'Route {route.network} has no next hop and destination is not directly connected',
                    path=packet.path,
                    ttl_remaining=packet.ttl,
                    logs=self.logger.to_dict(),
                )

            next_router = self.topology.resolve_next_router(current.router_id, route.next_hop)
            self.logger.log(
                current.router_id,
                'FORWARD',
                dest_ip=packet.dest_ip,
                matched_network=route.network,
                next_hop=route.next_hop,
                interface=route.interface,
            )
            if next_router is None:
                self.logger.log(current.router_id, 'UNREACHABLE_NEXT_HOP', next_hop=route.next_hop)
                return SimulationResult(
                    status='NO_ROUTE',
                    message=f'Next hop {route.next_hop} is unreachable from {current.router_id}',
                    path=packet.path,
                    ttl_remaining=packet.ttl,
                    logs=self.logger.to_dict(),
                )

            packet.decrement_ttl()
            current = next_router
