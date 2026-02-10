#!/usr/bin/env python3
"""
Mass Recon IP Generator Tool
Generates all IPs from CIDR or start-end ranges.
Supports single range input or bulk file input.
Outputs in TXT or JSON format.
"""

import argparse
import ipaddress
import os
import sys
import json

def parse_range(range_str):
    """
    Parse a range string which can be CIDR or start-end format.
    Returns a generator of IP addresses.
    """
    range_str = range_str.strip()
    if not range_str:
        return []
    try:
        if "-" in range_str:
            # Start-End format
            start_ip, end_ip = range_str.split("-")
            start_ip = ipaddress.IPv4Address(start_ip.strip())
            end_ip = ipaddress.IPv4Address(end_ip.strip())
            if int(end_ip) < int(start_ip):
                raise ValueError("End IP smaller than start IP")
            return (ipaddress.IPv4Address(ip) for ip in range(int(start_ip), int(end_ip) + 1))
        else:
            # CIDR format
            net = ipaddress.ip_network(range_str, strict=False)
            return net.hosts()
    except Exception as e:
        print(f"[!] Invalid range skipped: {range_str} ({e})", file=sys.stderr)
        return []


def read_ranges_from_file(filename):
    """
    Read ranges from a file, skipping comments and empty lines.
    """
    if not os.path.exists(filename):
        print(f"[!] File not found: {filename}", file=sys.stderr)
        sys.exit(1)
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                yield line


def generate_ips(ranges, verbose=False, unique=False):
    """
    Generator that yields IPs from ranges.
    Supports verbose logging and uniqueness.
    """
    seen = set() if unique else None
    for r in ranges:
        if verbose:
            print(f"[+] Expanding range: {r}")
        for ip in parse_range(r):
            if seen is not None:
                if ip in seen:
                    continue
                seen.add(ip)
            yield ip


def write_output(ips, output_file, fmt, verbose=False, count=False):
    """
    Write IPs to output file in chosen format.
    Stream writing to avoid memory issues.
    """
    total = 0
    if fmt == "txt":
        with open(output_file, "w") as f:
            for ip in ips:
                f.write(str(ip) + "\n")
                total += 1
                if verbose and total % 100000 == 0:
                    print(f"[+] Generated {total} IPs...")
    elif fmt == "json":
        with open(output_file, "w") as f:
            f.write('{"ips":[')
            first = True
            for ip in ips:
                if not first:
                    f.write(",")
                f.write(f"\"{ip}\"")
                first = False
                total += 1
                if verbose and total % 100000 == 0:
                    print(f"[+] Generated {total} IPs...")
            f.write("]}")
    else:
        print("[!] Unsupported format. Use txt or json.", file=sys.stderr)
        sys.exit(1)

    if count:
        print(f"[+] Total IPs generated: {total}")
    else:
        print(f"[+] Finished. Output written to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Mass Recon IP Generator Tool")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-r", "--range", help="Single IP range (CIDR or start-end)")
    group.add_argument("-i", "--input", help="File containing multiple ranges")
    parser.add_argument("-o", "--output", required=True, help="Output filename")
    parser.add_argument("--format", required=True, choices=["txt", "json"], help="Output format")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    parser.add_argument("--unique", action="store_true", help="Deduplicate IPs")
    parser.add_argument("--count", action="store_true", help="Show total count of IPs")

    args = parser.parse_args()

    # Collect ranges
    if args.range:
        ranges = [args.range]
    else:
        ranges = list(read_ranges_from_file(args.input))

    # Generate IPs
    ips = generate_ips(ranges, verbose=args.verbose, unique=args.unique)

    # Write output
    write_output(ips, args.output, args.format, verbose=args.verbose, count=args.count)


if __name__ == "__main__":
    main()
