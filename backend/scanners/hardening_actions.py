def get_hardening_recommendations():
    return [
        {
            "id": "h_ssh_01",
            "category": "SSH",
            "title": "Disable Root Login",
            "description": "Ensure root login is disabled over SSH.",
            "command": "sed -i 's/^PermitRootLogin.*/PermitRootLogin no/g' /etc/ssh/sshd_config && systemctl restart sshd",
            "risk_level": "high",
            "impact": "High"
        },
        {
            "id": "h_net_01",
            "category": "Network",
            "title": "Disable IPv6",
            "description": "Disable IPv6 if not required.",
            "command": "sysctl -w net.ipv6.conf.all.disable_ipv6=1",
            "risk_level": "low",
            "impact": "Low"
        }
    ]

def apply_hardening_action(vm_info, action_id):
    # In live mode, run command via SSH
    return {"status": "success"}
