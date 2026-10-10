import sqlite3
from flask import current_app, g
from contextlib import contextmanager

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE_PATH'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()
    
    schema = """
    CREATE TABLE IF NOT EXISTS vm_connection (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gcp_project TEXT NOT NULL,
        zone TEXT NOT NULL,
        instance_name TEXT NOT NULL,
        status TEXT DEFAULT 'disconnected',
        cos_version TEXT,
        connected_at TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS scan_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_type TEXT NOT NULL,
        data_source TEXT NOT NULL DEFAULT 'demo',
        label TEXT DEFAULT 'scan',
        results TEXT NOT NULL,  -- JSON string
        security_score INTEGER DEFAULT 0,
        scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS cis_checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_id INTEGER,
        benchmark_id TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL,  -- PASS, FAIL, WARN, N/A
        severity TEXT NOT NULL, -- critical, high, medium, low, info
        evidence TEXT,
        remediation TEXT,
        FOREIGN KEY (scan_id) REFERENCES scan_results(id)
    );

    CREATE TABLE IF NOT EXISTS hardening_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_id TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        command TEXT,
        risk_level TEXT DEFAULT 'medium',
        impact TEXT,
        status TEXT DEFAULT 'pending',  -- pending, applied, skipped
        applied_at TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS firewall_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_id INTEGER,
        rule_name TEXT NOT NULL,
        direction TEXT NOT NULL,
        action TEXT NOT NULL,
        protocol TEXT,
        ports TEXT,
        source_ranges TEXT,
        target_tags TEXT,
        priority INTEGER DEFAULT 1000,
        risk_rating TEXT DEFAULT 'medium',
        data_source TEXT DEFAULT 'demo',
        FOREIGN KEY (scan_id) REFERENCES scan_results(id)
    );

    CREATE TABLE IF NOT EXISTS cve_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cve_id TEXT UNIQUE NOT NULL,
        severity TEXT NOT NULL,
        cvss_score REAL,
        description TEXT,
        affected_versions TEXT,
        fixed_in_version TEXT,
        patch_status TEXT DEFAULT 'unknown',
        reference_url TEXT,
        published_date TEXT
    );

    CREATE TABLE IF NOT EXISTS patch_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cos_milestone TEXT NOT NULL,
        build_number TEXT NOT NULL,
        release_date TEXT,
        cve_fixes_count INTEGER DEFAULT 0,
        changelog_url TEXT,
        data_source TEXT DEFAULT 'demo'
    );

    CREATE TABLE IF NOT EXISTS comparison_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label TEXT NOT NULL,  -- BEFORE or AFTER
        overall_score INTEGER DEFAULT 0,
        cis_compliance REAL DEFAULT 0,
        network_score INTEGER DEFAULT 0,
        container_score INTEGER DEFAULT 0,
        hardening_score INTEGER DEFAULT 0,
        patch_score INTEGER DEFAULT 0,
        details TEXT,  -- JSON string with full details
        data_source TEXT DEFAULT 'demo',
        captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    db.executescript(schema)
    db.commit()
