from softroute.core.routing_table import RoutingTable


def test_longest_prefix_match_prefers_more_specific_route() -> None:
    table = RoutingTable()
    table.add_route('10.0.0.0/8', '10.0.12.2', 'wan', 5)
    table.add_route('10.1.0.0/16', '10.0.12.3', 'wan', 1)
    match = table.find_best_match('10.1.2.3')
    assert match is not None
    assert match.network == '10.1.0.0/16'


def test_default_route_matches_anything_when_no_specific_route_exists() -> None:
    table = RoutingTable()
    table.add_route('0.0.0.0/0', '1.1.1.1', 'wan')
    match = table.find_best_match('203.0.113.15')
    assert match is not None
    assert match.network == '0.0.0.0/0'
