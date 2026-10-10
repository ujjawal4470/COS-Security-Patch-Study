from .os_scanner import OSScanner
from .network_scanner import NetworkScanner
from .cis_scanner import CISScanner
from .container_scanner import ContainerScanner
from .patch_scanner import PatchScanner
from .cve_analyzer import CVEAnalyzer

def run_all_scanners(vm_info):
    results = {}
    
    scanners = [
        OSScanner(vm_info),
        NetworkScanner(vm_info),
        CISScanner(vm_info),
        ContainerScanner(vm_info),
        PatchScanner(vm_info),
        CVEAnalyzer(vm_info)
    ]
    
    for scanner in scanners:
        res = scanner.run()
        results.update(res)
        
    return results
