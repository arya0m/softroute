from softroute.core.packet import Packet


def test_packet_validation_and_ttl() -> None:
    packet = Packet(src_ip='192.168.1.10', dest_ip='10.0.2.55', ttl=4)
    packet.validate()
    assert not packet.is_expired()
    packet.decrement_ttl()
    assert packet.ttl == 3
