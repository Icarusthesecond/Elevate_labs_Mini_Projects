import os
import stat
import subprocess

class LinuxAuditTool:
    def __init__(self):
        self.score = 0
        self.max_score = 5
        self.findings = []
        self.remediations = []

    def run_command(self, command):
        """Helper to run shell commands safely"""
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout.strip()
        except Exception:
            return ""

    def check_firewall(self):
        print("[*] Checking Firewall Status...")
        ufw_status = self.run_command("sudo ufw status")
        if "Status: active" in ufw_status:
            self.score += 1
            print("  [PASS] UFW Firewall is active.")
        else:
            self.findings.append("UFW Firewall is inactive or not installed.")
            self.remediations.append("Run 'sudo ufw enable' to activate the firewall.")
            print("  [FAIL] UFW Firewall is NOT active.")

    def check_ssh_config(self):
        print("[*] Checking SSH Configuration...")
        ssh_config_path = "/etc/ssh/sshd_config"
        
        if not os.path.exists(ssh_config_path):
            print("  [SKIP] SSH is not installed.")
            self.max_score -= 2 # Adjust max score if SSH isn't applicable
            return

        with open(ssh_config_path, "r") as f:
            config = f.read()

        # Check Root Login
        if "PermitRootLogin no" in config and not "#PermitRootLogin no" in config:
            self.score += 1
            print("  [PASS] Direct root login is disabled.")
        else:
            self.findings.append("SSH permits direct root login.")
            self.remediations.append(f"Set 'PermitRootLogin no' in {ssh_config_path} and restart sshd.")
            print("  [FAIL] Direct root login over SSH is permitted.")

        # Check Password Auth
        if "PasswordAuthentication no" in config and not "#PasswordAuthentication no" in config:
            self.score += 1
            print("  [PASS] SSH Password authentication is disabled (Keys enforced).")
        else:
            self.findings.append("SSH Password Authentication is enabled.")
            self.remediations.append(f"Set 'PasswordAuthentication no' in {ssh_config_path} and restart sshd.")
            print("  [FAIL] SSH Password authentication is enabled.")

    def check_file_permissions(self):
        print("[*] Checking Critical File Permissions...")
        
        # Check /etc/shadow
        try:
            st = os.stat("/etc/shadow")
            octal_perm = oct(st.st_mode)[-3:]
            if octal_perm in ["640", "600", "000"]:
                self.score += 1
                print(f"  [PASS] /etc/shadow permissions are secure ({octal_perm}).")
            else:
                self.findings.append(f"/etc/shadow has overly permissive rights: {octal_perm}")
                self.remediations.append("Run 'sudo chmod 640 /etc/shadow' to secure password hashes.")
                print(f"  [FAIL] /etc/shadow permissions are {octal_perm}.")
        except PermissionError:
            print("  [ERROR] Must run script as root/sudo to check /etc/shadow.")
            self.findings.append("Could not read /etc/shadow (Run as root).")

    def check_rootkits(self):
        print("[*] Checking for Rootkit indicators...")
        # Check if rkhunter or chkrootkit is installed
        rkhunter = self.run_command("which rkhunter")
        chkrootkit = self.run_command("which chkrootkit")
        
        if rkhunter or chkrootkit:
            self.score += 1
            print("  [PASS] Rootkit detection tools are installed.")
        else:
            self.findings.append("No standard rootkit scanners found (rkhunter/chkrootkit).")
            self.remediations.append("Run 'sudo apt install rkhunter chkrootkit' to enable scanning.")
            print("  [FAIL] No rootkit scanners installed.")

    def generate_report(self):
        print("\n" + "="*50)
        print("          SYSTEM HARDENING AUDIT REPORT")
        print("="*50)
        
        compliance_pct = (self.score / self.max_score) * 100
        print(f"COMPLIANCE SCORE: {self.score}/{self.max_score} ({compliance_pct:.1f}%)\n")
        
        if self.findings:
            print("[!] VULNERABILITIES FOUND:")
            for i, finding in enumerate(self.findings, 1):
                print(f"  {i}. {finding}")
                
            print("\n[+] RECOMMENDED REMEDIATION ACTIONS:")
            for i, remediation in enumerate(self.remediations, 1):
                print(f"  {i}. {remediation}")
        else:
            print("[+] Excellent! No severe misconfigurations found. System aligns with baseline.")
        print("="*50 + "\n")

    def execute_audit(self):
        print("Starting Security Audit...\n")
        self.check_firewall()
        self.check_ssh_config()
        self.check_file_permissions()
        self.check_rootkits()
        self.generate_report()

if __name__ == "__main__":
    # Ensure the script is run as root for accurate file permission checks
    if os.geteuid() != 0:
        print("[!] WARNING: You are not running this script as root.")
        print("[!] Some checks (like /etc/shadow permissions) will fail.")
        print("    Please run: sudo python3 audit_tool.py\n")
    
    auditor = LinuxAuditTool()
    auditor.execute_audit()