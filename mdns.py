#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# An attempt to construct a raw -- and VERY specific -- mDNS query
# from scratch. The adventure begins at:
#
#    https://en.wikipedia.org/wiki/Multicast_DNS
# taken from
# https://serverfault.com/questions/949441/how-does-ping-determine-the-ip-address-of-an-mdns-service

import socket
import struct
import sys
import time

def main(host, domain):

    # if len(sys.argv) > 1:
        # host, domain = sys.argv[1].split(".")
    host, domain = host.encode(), domain.encode()
    hlen, dlen   = bytes([len(host)]), bytes([len(domain)])
    # else:
    #     print("Usage:\n\n    mdns.py FQDN\n")
    #     print("No FQDN supplied. Exiting...")
    #     sys.exit(1)

    # Construct the UDP packet to be multicast
    #
    PACKET  = b""
    PACKET += b"\x00\x00"              # Transaction ID
    PACKET += b"\x00\x00"              # Flags
    PACKET += b"\x00\x01"              # Number of questions
    PACKET += b"\x00\x00"              # Number of answers
    PACKET += b"\x00\x00"              # Number of authority  resource records
    PACKET += b"\x00\x00"              # Number of additional resource records
    PACKET += hlen                     # Prefixed host name string length
    PACKET += host                     # Host name
    PACKET += dlen                     # Prefixed domain name string length
    PACKET += domain                   # Domain name
    PACKET += b"\x00"                  # Terminator
    PACKET += b"\x00\x01"              # Type (A record, Host address)
    #PACKET += b"\x00\x1C"             # Type (AAAA record, IPv6 address)
    PACKET += b"\x00\x01"              # Class

    print(PACKET)

    multicast_group = ("224.0.0.251", 5353)

    # Create the datagram socket
    #
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    #
    sock.settimeout(0.2)

    # Set the time-to-live for messages to 1 so they do not
    # go past the local network segment.
    #
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        # Send data to the multicast group
    #   print('sending {!r}'.format(message))
        sent = sock.sendto(PACKET, multicast_group)

        # Look for responses from all recipients
        #
        while True:
            print('waiting to receive')
            try:
                data, server = sock.recvfrom(4096)
            except socket.timeout:
                print('timed out, no more responses')
                break
            else:
                print('received {!r} from {}'.format(
                    data, server))

    finally:
        print('closing socket')
        sock.close()


if __name__ == "__main__":
    main()
