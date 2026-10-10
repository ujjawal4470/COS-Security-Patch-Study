import json
from datetime import datetime
from database import get_db

def get_vm_connection():
    db = get_db()
    row = db.execute("SELECT * FROM vm_connection ORDER BY id DESC LIMIT 1").fetchone()
    return dict(row) if row else None

def save_vm_connection(project, zone, instance, status, cos_version):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO vm_connection (gcp_project, zone, instance_name, status, cos_version, connected_at) VALUES (?, ?, ?, ?, ?, ?)",
        (project, zone, instance, status, cos_version, datetime.now())
    )
    db.commit()
    return cursor.lastrowid

def clear_vm_connection():
    db = get_db()
    db.execute("DELETE FROM vm_connection")
    db.commit()

def save_scan_result(scan_type, data_source, label, results_json, score):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO scan_results (scan_type, data_source, label, results, security_score) VALUES (?, ?, ?, ?, ?)",
        (scan_type, data_source, label, json.dumps(results_json), score)
    )
    db.commit()
    return cursor.lastrowid

def get_latest_scan(scan_type):
    db = get_db()
    row = db.execute("SELECT * FROM scan_results WHERE scan_type = ? ORDER BY id DESC LIMIT 1", (scan_type,)).fetchone()
    if row:
        d = dict(row)
        d['results'] = json.loads(d['results'])
        return d
    return None

def get_scan_history(scan_type, limit=10):
    db = get_db()
    rows = db.execute("SELECT * FROM scan_results WHERE scan_type = ? ORDER BY id DESC LIMIT ?", (scan_type, limit)).fetchall()
    res = []
    for r in rows:
        d = dict(r)
        d['results'] = json.loads(d['results'])
        res.append(d)
    return res

def save_cis_checks(scan_id, checks_list):
    db = get_db()
    cursor = db.cursor()
    for chk in checks_list:
        cursor.execute(
            "INSERT INTO cis_checks (scan_id, benchmark_id, category, description, status, severity, evidence, remediation) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (scan_id, chk['benchmark_id'], chk['category'], chk['description'], chk['status'], chk['severity'], chk.get('evidence', ''), chk.get('remediation', ''))
        )
    db.commit()

def get_cis_checks(scan_id):
    db = get_db()
    rows = db.execute("SELECT * FROM cis_checks WHERE scan_id = ?", (scan_id,)).fetchall()
    return [dict(r) for r in rows]

def save_firewall_rules(scan_id, rules_list, data_source):
    db = get_db()
    cursor = db.cursor()
    for rule in rules_list:
        cursor.execute(
            "INSERT INTO firewall_rules (scan_id, rule_name, direction, action, protocol, ports, source_ranges, target_tags, priority, risk_rating, data_source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (scan_id, rule['rule_name'], rule['direction'], rule['action'], rule.get('protocol', ''), rule.get('ports', ''), rule.get('source_ranges', ''), rule.get('target_tags', ''), rule.get('priority', 1000), rule.get('risk_rating', 'medium'), data_source)
        )
    db.commit()

def get_hardening_actions():
    db = get_db()
    rows = db.execute("SELECT * FROM hardening_actions").fetchall()
    return [dict(r) for r in rows]

def update_hardening_status(action_id, status):
    db = get_db()
    db.execute("UPDATE hardening_actions SET status = ?, applied_at = ? WHERE action_id = ?", (status, datetime.now(), action_id))
    db.commit()

def save_comparison_snapshot(label, scores_dict, data_source):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO comparison_snapshots (label, overall_score, cis_compliance, network_score, container_score, hardening_score, patch_score, details, data_source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (label, scores_dict.get('overall', 0), scores_dict.get('cis', 0), scores_dict.get('network', 0), scores_dict.get('container', 0), scores_dict.get('hardening', 0), scores_dict.get('patch', 0), json.dumps(scores_dict), data_source)
    )
    db.commit()
    return cursor.lastrowid

def get_latest_comparison():
    db = get_db()
    before = db.execute("SELECT * FROM comparison_snapshots WHERE label = 'BEFORE' ORDER BY id DESC LIMIT 1").fetchone()
    after = db.execute("SELECT * FROM comparison_snapshots WHERE label = 'AFTER' ORDER BY id DESC LIMIT 1").fetchone()
    res = {}
    if before:
        res['before'] = dict(before)
        res['before']['details'] = json.loads(res['before']['details'])
    if after:
        res['after'] = dict(after)
        res['after']['details'] = json.loads(res['after']['details'])
    return res

def get_cve_list(page=1, per_page=10, severity_filter=None):
    db = get_db()
    offset = (page - 1) * per_page
    query = "SELECT * FROM cve_entries"
    params = []
    if severity_filter:
        query += " WHERE severity = ?"
        params.append(severity_filter)
    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([per_page, offset])
    
    rows = db.execute(query, params).fetchall()
    count_query = "SELECT COUNT(*) FROM cve_entries"
    if severity_filter:
        count_query += " WHERE severity = ?"
        total = db.execute(count_query, (severity_filter,)).fetchone()[0]
    else:
        total = db.execute(count_query).fetchone()[0]
        
    return [dict(r) for r in rows], total

def get_cve_statistics():
    db = get_db()
    stats = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'total': 0}
    rows = db.execute("SELECT severity, COUNT(*) as cnt FROM cve_entries GROUP BY severity").fetchall()
    for r in rows:
        stats[r['severity'].lower()] = r['cnt']
        stats['total'] += r['cnt']
    return stats

def get_patch_history():
    db = get_db()
    rows = db.execute("SELECT * FROM patch_history ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]
