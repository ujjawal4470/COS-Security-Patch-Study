from flask import Blueprint, request, jsonify
from models import (
    get_vm_connection,
    save_scan_result,
    get_latest_scan,
    get_scan_history,
)
from scanners.os_scanner import OSScanner

assessment_bp = Blueprint(
    "assessment", __name__, url_prefix="/api/assessment"
)


def calculate_score(results):
    findings = results.get("sysctl_findings", [])
    known = [
        item for item in findings
        if item.get("status") in ("PASS", "FAIL")
    ]
    if not known:
        return None
    passed = sum(item["status"] == "PASS" for item in known)
    return round(100 * passed / len(known))


@assessment_bp.route("/run", methods=["POST"])
def run_assessment():
    data = request.get_json(silent=True) or {}
    label = data.get("label", "Manual Scan")

    target = data.get("target", "vm")
    vm = get_vm_connection()
    is_connected = bool(vm and vm.get("status") == "connected")
    scanner = OSScanner(vm if is_connected else None)

    try:
        if target == "cloud_shell":
            results = scanner.run_local()
            label = data.get("label", "Cloud Shell Live Scan")
        else:
            results = scanner.run()
    except Exception as exc:
        # Never label a failed live scan as demo or successful.
        return jsonify({
            "data_source": "live" if is_connected else "demo",
            "message": "Assessment failed",
            "error": str(exc),
        }), 502 if is_connected else 500

    source = results.get("data_source", "demo")
    if target == "cloud_shell" and source != "live":
        return jsonify({"data_source": "live", "message": "Cloud Shell scan did not return live results"}), 502

    if is_connected and target != "cloud_shell" and source != "live":
        return jsonify({
            "data_source": "live",
            "message": "Live scan did not return live results",
        }), 502

    score = calculate_score(results)
    if score is None:
        if source == "live":
            return jsonify({
                "data_source": "live",
                "message": "No usable security findings were collected",
            }), 502
        score = 65

    scan_id = save_scan_result(
        "comprehensive", source, label, results, score
    )

    return jsonify({
        "data_source": source,
        "message": "Scan completed",
        "scan_id": scan_id,
        "score": score,
        "results": results,
    })


@assessment_bp.route("/latest", methods=["GET"])
def get_latest_assessment():
    scan = get_latest_scan("comprehensive")
    if scan:
        results = scan.get("results", {})
        os_info = results.get("os_info", {})
        return jsonify({
            "data_source": scan["data_source"],
            "score": scan.get("security_score", 65),
            "os_info": os_info,
            "scan": scan,
        })

    return jsonify({
        "data_source": "demo",
        "score": 65,
        "os_info": {
            "name": "Container-Optimized OS",
            "os": "Container-Optimized OS",
            "version": "cos-101-17162.336.36",
            "kernel": "5.15.109+",
            "arch": "x86_64",
            "architecture": "x86_64",
        },
        "message": "No scans run yet - showing demo data",
    })


@assessment_bp.route("/history", methods=["GET"])
def get_history():
    history = get_scan_history("comprehensive")
    return jsonify({
        "data_source": "demo" if not history else history[0]["data_source"],
        "history": history,
    })
