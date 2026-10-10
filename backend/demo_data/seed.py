import json
import os
from datetime import datetime

def seed_demo_data(db):
    base_dir = os.path.dirname(__file__)
    cursor = db.cursor()

    # Seed Hardening Actions
    actions = [
        ("h_ssh_01", "SSH", "Disable Root Login", "Ensure root login is disabled over SSH.", "sed -i 's/^PermitRootLogin.*/PermitRootLogin no/g' /etc/ssh/sshd_config && systemctl restart sshd", "high", "High", "pending"),
        ("h_ssh_02", "SSH", "Disable Password Authentication", "Enforce key-based authentication only.", "sed -i 's/^PasswordAuthentication.*/PasswordAuthentication no/g' /etc/ssh/sshd_config && systemctl restart sshd", "high", "High", "pending"),
        ("h_fs_01", "Filesystem", "Set /tmp to noexec", "Prevent execution of binaries from /tmp.", "mount -o remount,noexec /tmp", "medium", "Medium", "pending"),
        ("h_net_01", "Network", "Disable IPv6", "Disable IPv6 if not required.", "sysctl -w net.ipv6.conf.all.disable_ipv6=1", "low", "Low", "pending"),
        ("h_net_02", "Network", "Enable TCP SYN Cookies", "Protect against SYN flood attacks.", "sysctl -w net.ipv4.tcp_syncookies=1", "medium", "Medium", "pending"),
        ("h_doc_01", "Docker", "Enable Docker Content Trust", "Enforce signature verification for images.", "export DOCKER_CONTENT_TRUST=1", "high", "High", "pending"),
        ("h_ker_01", "Kernel", "Restrict dmesg access", "Prevent unprivileged users from reading kernel logs.", "sysctl -w kernel.dmesg_restrict=1", "medium", "Low", "pending")
    ]
    for act in actions:
        cursor.execute("INSERT OR IGNORE INTO hardening_actions (action_id, category, title, description, command, risk_level, impact, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", act)

    # Seed CVEs
    try:
        with open(os.path.join(base_dir, 'sample_cves.json'), 'r') as f:
            cves = json.load(f)
            for c in cves:
                cursor.execute(
                    "INSERT OR IGNORE INTO cve_entries (cve_id, severity, cvss_score, description, affected_versions, fixed_in_version, patch_status, reference_url, published_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (c['cve_id'], c['severity'], c['cvss_score'], c['description'], c['affected_versions'], c['fixed_in_version'], c.get('patch_status', 'unknown'), c['reference_url'], c['published_date'])
                )
    except FileNotFoundError:
        pass

    # Seed Patch History
    patches = [
        ("93", "16623.102.1", "2023-01-15", 5, "https://cloud.google.com/container-optimized-os/docs/release-notes", "demo"),
        ("97", "16919.123.5", "2023-05-20", 12, "https://cloud.google.com/container-optimized-os/docs/release-notes", "demo"),
        ("101", "17162.336.36", "2023-11-10", 8, "https://cloud.google.com/container-optimized-os/docs/release-notes", "demo"),
        ("105", "17412.100.1", "2024-02-05", 15, "https://cloud.google.com/container-optimized-os/docs/release-notes", "demo"),
        ("109", "17800.50.2", "2024-05-15", 3, "https://cloud.google.com/container-optimized-os/docs/release-notes", "demo")
    ]
    for p in patches:
        cursor.execute("INSERT INTO patch_history (cos_milestone, build_number, release_date, cve_fixes_count, changelog_url, data_source) VALUES (?, ?, ?, ?, ?, ?)", p)

    # Seed Comparison
    cursor.execute(
        "INSERT INTO comparison_snapshots (label, overall_score, cis_compliance, network_score, container_score, hardening_score, patch_score, details, data_source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("BEFORE", 42, 35.5, 40, 50, 30, 45, json.dumps({"overall":42,"cis":35.5,"network":40,"container":50,"hardening":30,"patch":45}), "demo")
    )
    cursor.execute(
        "INSERT INTO comparison_snapshots (label, overall_score, cis_compliance, network_score, container_score, hardening_score, patch_score, details, data_source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("AFTER", 87, 85.0, 90, 85, 95, 80, json.dumps({"overall":87,"cis":85.0,"network":90,"container":85,"hardening":95,"patch":80}), "demo")
    )

    db.commit()
