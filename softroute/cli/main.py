from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from softroute.core.packet import Packet
from softroute.core.topology import Topology
from softroute.engine.simulator import SimulationEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='SoftRoute routing simulation CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    simulate = subparsers.add_parser('simulate', help='Run a packet simulation')
    simulate.add_argument('--topology', required=True, help='Path to topology JSON file')
    simulate.add_argument('--src', required=True, help='Source IP address')
    simulate.add_argument('--dest', required=True, help='Destination IP address')
    simulate.add_argument('--ttl', type=int, default=64, help='Packet TTL')
    simulate.add_argument('--start-router', default=None, help='Optional starting router ID')
    simulate.add_argument('--json', action='store_true', help='Output JSON result')
    return parser


def cmd_simulate(args: argparse.Namespace) -> int:
    topology_data = json.loads(Path(args.topology).read_text(encoding='utf-8'))
    topology = Topology.from_dict(topology_data)
    engine = SimulationEngine(topology)
    packet = Packet(src_ip=args.src, dest_ip=args.dest, ttl=args.ttl)
    result = engine.simulate(packet, start_router_id=args.start_router)

    if args.json:
        print(json.dumps({
            'status': result.status,
            'message': result.message,
            'path': result.path,
            'ttl_remaining': result.ttl_remaining,
            'logs': result.logs,
        }, indent=2))
    else:
        print(result.status)
        print(f'Message: {result.message}')
        print(f"Path: {' -> '.join(result.path) if result.path else '(none)'}")
        print(f'TTL remaining: {result.ttl_remaining}')
    return 0 if result.status == 'DELIVERED' else 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == 'simulate':
        return cmd_simulate(args)
    parser.error('Unknown command')
    return 2


if __name__ == '__main__':
    sys.exit(main())
