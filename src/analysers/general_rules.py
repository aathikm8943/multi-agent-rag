from .base_rule import BaseRuleEngine

class GenericCodeRuleEngine(BaseRuleEngine):
    def run(self):
        lines = self.code.splitlines()
        for idx, line in enumerate(lines, 1):
            if 'eval(' in line:
                self.issues.append({
                    "rule": "GEN001",
                    "severity": "HIGH",
                    "message": "Avoid using eval() due to security risks",
                    "line": idx
                })
            if 'exec(' in line:
                self.issues.append({
                    "rule": "GEN002",
                    "severity": "HIGH",
                    "message": "Avoid using exec() due to security risks",
                    "line": idx
                })
            if 'import *' in line:
                self.issues.append({
                    "rule": "GEN003",
                    "severity": "MEDIUM",
                    "message": "Avoid wildcard imports for clarity and maintainability",
                    "line": idx
                })
            if 'TODO' in line:
                self.issues.append({
                    "rule": "GEN004",
                    "severity": "INFO",
                    "message": "Remove TODO comments before production",
                    "line": idx
                })
            if 'print(' in line:
                self.issues.append({
                    "rule": "GEN005",
                    "severity": "LOW",
                    "message": "Avoid using print statements in production code",
                    "line": idx
                })
            if 'password' in line.lower() and ('=' in line or ':' in line):
                self.issues.append({
                    "rule": "GEN006",
                    "severity": "CRITICAL",
                    "message": "Hardcoded password detected",
                    "line": idx
                })

