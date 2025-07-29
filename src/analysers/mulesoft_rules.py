from typing import Dict, List
import re

class MuleSoftRuleEngine:
    def __init__(self):
        self.code = ""
        self.issues = []

    def analyze_code(self, code: str) -> Dict:
        """Analyze MuleSoft code and return structured results"""
        self.code = code
        self.issues = []
        self._check_rules()
        return self._format_results()

    def _check_rules(self):
        """Run all rule checks"""
        lines = self.code.splitlines()
        for idx, line in enumerate(lines, 1):
            self._check_line(line, idx)

    def _check_line(self, line: str, idx: int):
        """Check single line against all rules"""
        # ... existing rule checks ...
        if '<flow' in line and 'name="' not in line:
            self._add_issue("MULE001", "HIGH", "Flow missing name attribute", idx)
            
        if 'password="' in line and '${' not in line:
            self._add_issue("MULE002", "CRITICAL", "Hardcoded credentials detected", idx)
            
        if '<http:listener' in line and ('config-ref="' not in line or 'path="' not in line):
            self._add_issue("MULE003", "HIGH", "HTTP Listener missing required attributes", idx)
            
        if '<db:select' in line and 'config-ref="' not in line:
            self._add_issue("MULE004", "HIGH", "Database operation missing configuration reference", idx)

    def _add_issue(self, rule_id: str, severity: str, message: str, line: int):
        self.issues.append({
            "rule_id": rule_id,
            "severity": severity,
            "message": message,
            "line": line
        })

    def _format_results(self) -> Dict:
        return {
            "total_issues": len(self.issues),
            "issues": self.issues,
            "summary": self._generate_summary()
        }

    def _generate_summary(self) -> str:
        if not self.issues:
            return "No issues found in the code."
        
        severity_count = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for issue in self.issues:
            severity_count[issue["severity"]] += 1
            
        return f"Found {len(self.issues)} issues: " + \
               f"{severity_count['CRITICAL']} critical, " + \
               f"{severity_count['HIGH']} high, " + \
               f"{severity_count['MEDIUM']} medium, " + \
               f"{severity_count['LOW']} low severity."

# from .base_rule import BaseRuleEngine

# class MuleSoftRuleEngine(BaseRuleEngine):
#     def run(self):
#         lines = self.code.splitlines()
#         for idx, line in enumerate(lines, 1):
#             if '<flow' in line and 'name="' not in line:
#                 self.issues.append({
#                     "rule": "MULE001",
#                     "severity": "MEDIUM",
#                     "message": "Flow missing name attribute",
#                     "line": idx
#                 })
#             if '<set-payload' in line and 'doc:name' not in line:
#                 self.issues.append({
#                     "rule": "MULE002",
#                     "severity": "LOW",
#                     "message": "Missing doc:name in set-payload",
#                     "line": idx
#                 })
#             if '<http:listener' in line and 'path="' not in line:
#                 self.issues.append({
#                     "rule": "MULE003",
#                     "severity": "HIGH",
#                     "message": "HTTP listener missing path attribute",
#                     "line": idx
#                 })
#             if 'logger' not in line.lower() and ('error' in line.lower() or 'exception' in line.lower()):
#                 self.issues.append({
#                     "rule": "MULE004",
#                     "severity": "MEDIUM",
#                     "message": "Possible error handling block missing logger",
#                     "line": idx
#                 })
#             if '<set-variable' in line and 'doc:name' not in line:
#                 self.issues.append({
#                     "rule": "MULE005",
#                     "severity": "LOW",
#                     "message": "Missing doc:name in set-variable",
#                     "line": idx
#                 })

