from softroute.core.packet import Packet
from softroute.core.topology import Topology
from softroute.engine.simulator import SimulationEngine


def build_topology() -> Topology:
    payload = {
        'routers': [
            {
                'id': 'R1',
                'interfaces': [
                    {'name': 'lan1', 'ip_address': '192.168.1.1', 'network': '192.168.1.0/24'},
                    {'name': 'r1-r2', 'ip_address': '10.0.12.1', 'network': '10.0.12.0/30'},
                ],
                'routes': [
                    {'network': '10.0.2.0/24', 'next_hop': '10.0.12.2', 'interface': 'r1-r2'},
                ],
            },
            {
                'id': 'R2',
                'interfaces': [
                    {'name': 'r2-r1', 'ip_address': '10.0.12.2', 'network': '10.0.12.0/30'},
                    {'name': 'lan2', 'ip_address': '10.0.2.1', 'network': '10.0.2.0/24'},
                ],
                'routes': [],
            },
        ],
        'links': [
            {'router_a': 'R1', 'iface_a': 'r1-r2', 'router_b': 'R2', 'iface_b': 'r2-r1'},
        ],
    }
    return Topology.from_dict(payload)


def test_packet_delivery_across_multiple_routers() -> None:
    topology = build_topology()
    engine = SimulationEngine(topology)
    packet = Packet(src_ip='192.168.1.10', dest_ip='10.0.2.25')
    result = engine.simulate(packet)
    assert result.status == 'DELIVERED'
    assert result.path == ['R1', 'R2']


def test_no_route_detected() -> None:
    topology = build_topology()
    engine = SimulationEngine(topology)
    packet = Packet(src_ip='192.168.1.10', dest_ip='172.16.1.9')
    result = engine.simulate(packet)
    assert result.status == 'NO_ROUTE'


def test_routing_loop_detected() -> None:
    payload = {
        'routers': [
            {
                'id': 'R1',
                'interfaces': [
                    {'name': 'lan1', 'ip_address': '192.168.1.1', 'network': '192.168.1.0/24'},
                    {'name': 'r1-r2', 'ip_address': '10.0.12.1', 'network': '10.0.12.0/30'},
                ],
                'routes': [
                    {'network': '172.16.0.0/16', 'next_hop': '10.0.12.2', 'interface': 'r1-r2'},
                ],
            },
            {
                'id': 'R2',
                'interfaces': [
                    {'name': 'r2-r1', 'ip_address': '10.0.12.2', 'network': '10.0.12.0/30'},
                ],
                'routes': [
                    {'network': '172.16.0.0/16', 'next_hop': '10.0.12.1', 'interface': 'r2-r1'},
                ],
            },
        ],
        'links': [
            {'router_a': 'R1', 'iface_a': 'r1-r2', 'router_b': 'R2', 'iface_b': 'r2-r1'},
        ],
    }
    topology = Topology.from_dict(payload)
    engine = SimulationEngine(topology)
    packet = Packet(src_ip='192.168.1.10', dest_ip='172.16.2.9', ttl=8)
    result = engine.simulate(packet)
    assert result.status == 'ROUTING_LOOP'
