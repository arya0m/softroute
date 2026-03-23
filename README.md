# SoftRoute

SoftRoute is a software-defined router simulation engine that models IP packet forwarding, routing table lookups, longest prefix match, next-hop resolution, TTL-based loop protection, and multi-router topologies.

## Features
- IPv4 packet simulation with source, destination, payload, and TTL
- Router engine with forwarding decisions and connected-network delivery
- Routing tables with static routes and default routes
- Longest Prefix Match (LPM) using prefix-aware route selection
- Multi-router topology simulation with named point-to-point links
- Step-by-step trace logs for each forwarding decision
- Loop and unreachable-destination detection
- CLI for simulating packet delivery from JSON topologies
- Unit and integration tests

## Project structure
```text
softroute/
├── softroute/
│   ├── core/
│   │   ├── packet.py
│   │   ├── interface.py
│   │   ├── route.py
│   │   ├── routing_table.py
│   │   ├── router.py
│   │   └── topology.py
│   ├── engine/
│   │   └── simulator.py
│   ├── utils/
│   │   ├── ip_utils.py
│   │   └── logger.py
│   └── cli/
│       └── main.py
├── examples/
│   └── sample_topology.json
├── tests/
├── requirements.txt
└── README.md
```

## Installation
```bash
cd softroute
python -m venv .venv
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
pip install -r requirements.txt
```

## Run tests
```bash
pytest -q
```

## Run the CLI
```bash
python -m softroute.cli.main simulate \
  --topology examples/sample_topology.json \
  --src 192.168.1.10 \
  --dest 10.0.2.55
```

## Example output
```text
DELIVERED
Path: R1 -> R2 -> R3
TTL remaining: 61
```

## Topology JSON format
```json
{
  "routers": [
    {
      "id": "R1",
      "interfaces": [
        {"name": "lan1", "ip_address": "192.168.1.1", "network": "192.168.1.0/24"},
        {"name": "r1-r2", "ip_address": "10.0.12.1", "network": "10.0.12.0/30"}
      ],
      "routes": [
        {"network": "10.0.2.0/24", "next_hop": "10.0.12.2", "interface": "r1-r2"},
        {"network": "0.0.0.0/0", "next_hop": "10.0.12.2", "interface": "r1-r2"}
      ]
    }
  ]
}
```

## Engineering notes
- Route lookup uses longest-prefix ordering, implemented with deterministic selection by prefix length and metric.
- Delivery succeeds when a packet reaches a router with a directly connected network matching the destination.
- TTL is decremented per forwarded hop.
- Loop detection is based on repeat visits to the same router for the same packet.

## Future extensions
- Trie-based route storage
- OSPF/RIP simulation
- Latency and packet-loss modeling
- Web UI / topology visualization
