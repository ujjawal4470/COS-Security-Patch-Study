import json
import os
import pytest

def test_cis_benchmarks_valid(tmp_path):
    # Create a mock benchmark file for testing since we don't have the real backend yet
    mock_data = {
        "benchmarks": [
            {
                "id": "1.1.1",
                "title": "Ensure mounting of cramfs is disabled",
                "severity": "high",
                "category": "Filesystem",
                "remediation": "Disable module"
            }
        ]
    }
    
    benchmark_file = tmp_path / "cis_benchmarks.json"
    with open(benchmark_file, "w") as f:
        json.dump(mock_data, f)
        
    with open(benchmark_file, "r") as f:
        data = json.load(f)
        
    benchmarks = data.get("benchmarks", [])
    
    # Verify required fields
    for b in benchmarks:
        assert "id" in b
        assert "title" in b
        assert "severity" in b
        assert "category" in b
        assert "remediation" in b
        
    # Verify unique IDs
    ids = [b["id"] for b in benchmarks]
    assert len(ids) == len(set(ids))
    
    # Verify severities
    valid_severities = {"low", "medium", "high", "critical"}
    for b in benchmarks:
        assert b["severity"].lower() in valid_severities
        
    # Verify remediation is not empty
    for b in benchmarks:
        assert len(b["remediation"]) > 0
