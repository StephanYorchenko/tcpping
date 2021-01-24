import socket
from struct import pack


class TCPFactory:
    @staticmethod
    def generate(k, host, number, port, seq, source):
        source_ip = k
        dest_ip = host

        ihl = 5
        version = 4
        tos = 0
        tot_len = 40
        id = number
        frag_off = 0
        ttl = 255
        protocol = socket.IPPROTO_TCP
        check = 10
        saddr = socket.inet_aton(source_ip)
        daddr = socket.inet_aton(dest_ip)

        ihl_version = (version << 4) + ihl

        ip_header = pack(
            "!BBHHHBBH4s4s",
            ihl_version,
            tos,
            tot_len,
            id,
            frag_off,
            ttl,
            protocol,
            check,
            saddr,
            daddr,
        )

        dest = port
        seq = seq
        ack_seq = seq + 1
        doff = 5
        fin = 0
        syn = 1
        rst = 0
        psh = 0
        ack = 0
        urg = 0
        window = 0
        check = 0
        urg_ptr = 0

        offset_res = (doff << 4) + 0
        tcp_flags = fin + (syn << 1) + (rst << 2)
        tcp_flags += (psh << 3) + (ack << 4) + (urg << 5)

        tcp_header = pack(
            "!HHLLBBHHH",
            source,
            dest,
            seq,
            ack_seq,
            offset_res,
            tcp_flags,
            window,
            check,
            urg_ptr,
        )

        source_address = socket.inet_aton(source_ip)
        dest_address = socket.inet_aton(dest_ip)
        placeholder = 0
        protocol = socket.IPPROTO_TCP
        tcp_length = len(tcp_header)

        psh = pack(
                "!4s4sBBH",
                source_address,
                dest_address,
                placeholder,
                protocol,
                tcp_length
        )
        psh = psh + tcp_header

        tcp_checksum = TCPFactory.checksum(psh)

        tcp_header = pack(
            "!HHLLBBHHH",
            source,
            dest,
            seq,
            ack_seq,
            offset_res,
            tcp_flags,
            window,
            tcp_checksum,
            urg_ptr,
        )

        packet = ip_header + tcp_header
        return packet

    @staticmethod
    def checksum(msg):
        s = 0
        msg = bytes(msg)
        for i in range(0, len(msg), 2):
            w = (msg[i] << 8) + (msg[i + 1])
            s = s + w
        s = (s >> 16) + (s & 0xFFFF)
        s = ~s & 0xFFFF
        return s
