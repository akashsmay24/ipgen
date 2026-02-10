# Mass Recon IP Generator Tool

A Python 3 command-line utility for Kali Linux that generates a full list of IP addresses from given IP ranges.  
Supports both single range input and bulk file input, with export options in **TXT** or **JSON** format.  
Designed for **mass recon usage**: efficient, memory-safe, and capable of handling large IP ranges.

---

## ✨ Features
- Accepts **CIDR notation** (e.g., `192.168.1.0/24`)
- Accepts **IP start-end ranges** (e.g., `172.16.1.10-172.16.1.50`)
- Input via:
  - Single range (`-r`)
  - File containing multiple ranges (`-i`)
- Output formats:
  - **TXT** → one IP per line
  - **JSON** → `{"ips": ["ip1", "ip2", ...]}`
- Stream writing for **large ranges** (no memory overload)
- Verbose mode for progress logging
- Graceful handling of invalid ranges
- Optional flags:
  - `--unique` → deduplicate IPs
  - `--count` → show total number of generated IPs

---

## ⚙️ Installation
Clone the repository and make the script executable:

```bash
git clone https://github.com/yourusername/ip-generator-tool.git
cd ip-generator-tool
chmod +x ipgen.py
```

---

## 🚀 Usage

### Single Range Input
```bash
./ipgen.py -r 192.168.1.0/24 -o ips.txt --format txt
```

### File Input
```bash
./ipgen.py -i ranges.txt -o ips.json --format json
```

Example `ranges.txt`:
```
192.168.1.0/24
10.0.0.0/16
172.16.1.10-172.16.1.50
```

### Verbose Mode
```bash
./ipgen.py -r 10.0.0.0/8 -o big.txt --format txt -v
```

### Deduplicate & Count
```bash
./ipgen.py -i ranges.txt -o unique_ips.txt --format txt --unique --count
```

---

## 📌 CLI Options

| Flag        | Description                                    |
|-------------|------------------------------------------------|
| `-r`        | Single IP range (CIDR or start-end)            |
| `-i`        | Input file with multiple ranges                |
| `-o`        | Output filename                                |
| `--format`  | Output format: `txt` or `json`                 |
| `-v`        | Verbose mode (progress logging)                |
| `--unique`  | Deduplicate IPs                                |
| `--count`   | Show total number of generated IPs             |

---

## 🛡️ Error Handling
- Invalid ranges → skipped with warning
- Missing input file → clean error message
- Missing output format → help menu shown
- Malformed input → tool continues without crashing

---

## 📖 Example Outputs

### TXT
```
192.168.1.1
192.168.1.2
192.168.1.3
...
```

### JSON
```json
{
  "ips": [
    "192.168.1.1",
    "192.168.1.2",
    "192.168.1.3"
  ]
}
```

---

## 🧑‍💻 Development Notes
- Written in **Python 3**
- Uses only **standard libraries** (`argparse`, `ipaddress`, `json`, `os`, `sys`)
- Production-ready for **Kali Linux** environments
- Modular functions with clear comments
