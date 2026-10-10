# CIS Benchmark Methodology

## What are CIS Benchmarks?
The Center for Internet Security (CIS) Benchmarks are best practices for the secure configuration of a target system. 

## CIS for Container-Optimized OS
COS is highly restricted by design (immutable rootfs, locked down SSH, disabled unused services). Standard Linux CIS benchmarks do not always apply. We utilize a tailored subset of rules designed for read-only container operating systems.

## Categories Covered
- **Filesystem**: Verifying `/var` and `/home` mount options (nodev, nosuid).
- **Services**: Ensuring no extraneous services are enabled via systemd.
- **Network**: Checking iptables and sysctl IP forwarding settings.
- **Logging**: Auditing cloud-audit configuration and stackdriver integration.
- **SSH**: Verifying RootLogin disabled and strict cipher suites.
- **Auth**: Checking PAM configurations (where applicable).
- **Docker**: Verifying daemon.json configurations (user namespace remapping, default ulimits).
- **Kernel**: Reviewing specific sysctl harding flags (e.g., ASLR, dmesg restriction).

## Execution Methodology
1. Backend triggers Python scanner.
2. Scanner executes a series of read-only shell commands (`cat`, `sysctl`, `systemctl is-enabled`).
3. Output is parsed and compared against defined regex patterns or expected values.

## Scoring
- **Pass**: System meets the requirement.
- **Fail**: System does not meet the requirement.
- **Manual**: Requires human verification.

## Limitations
This is an academic tool. It does not replace professional auditing software. Always consult the official CIS documentation.
