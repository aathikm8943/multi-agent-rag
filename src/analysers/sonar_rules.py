# Code for src/rules/sonar_rules.py

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass

class SeverityLevel(Enum):
    BLOCKER = "BLOCKER"
    CRITICAL = "CRITICAL"
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    INFO = "INFO"

@dataclass
class SonarRule:
    rule_id: str
    name: str
    severity: SeverityLevel
    description: str
    examples: Dict[str, str]  # Bad and good examples
    tags: List[str]

class MuleSoftSonarRules:
    def __init__(self):
        self.rules = self._initialize_rules()

    def _initialize_rules(self) -> Dict[str, SonarRule]:
        return {
            "MULE001": SonarRule(
                rule_id="MULE001",
                name="Avoid Hardcoded Credentials",
                severity=SeverityLevel.BLOCKER,
                description="Credentials should not be hardcoded in configuration files",
                examples={
                    "bad": """<db:mysql-connection username="admin" password="123456"/>""",
                    "good": """<db:mysql-connection username="${db.user}" password="${db.password}"/>"""
                },
                tags=["security", "config"]
            ),
            "MULE002": SonarRule(
                rule_id="MULE002",
                name="Use Error Handlers",
                severity=SeverityLevel.CRITICAL,
                description="Each flow should have proper error handling",
                examples={
                    "bad": """<flow name="mainFlow"></flow>""",
                    "good": """<flow name="mainFlow"><error-handler><on-error-continue></on-error-continue></error-handler></flow>"""
                },
                tags=["reliability", "error-handling"]
            ),
            "DWL001": SonarRule(
                rule_id="DWL001",
                name="Avoid Complex DataWeave Transformations",
                severity=SeverityLevel.MAJOR,
                description="DataWeave transformations should be simple and maintainable",
                examples={
                    "bad": """output application/json --- payload map ((item) -> item.data map ((data) -> data.nested))""",
                    "good": """output application/json --- payload map {
    data: $.data map {
        value: $.nested
    }
}"""
                },
                tags=["maintainability", "dataweave"]
            )
        }

    def analyze_code(self, code: str, file_type: str) -> List[Dict]:
        """
        Analyzes code against relevant rules based on file type
        Returns list of violations found
        """
        violations = []
        
        if file_type == ".xml":
            # XML specific rules
            if "password=" in code and "${" not in code:
                violations.append({
                    "rule": self.rules["MULE001"],
                    "line": None,  # Would need proper parsing to get line numbers
                    "message": "Hardcoded credentials detected"
                })
            
            if "<flow" in code and "<error-handler>" not in code:
                violations.append({
                    "rule": self.rules["MULE002"],
                    "line": None,
                    "message": "Flow missing error handler"
                })

        elif file_type == ".dwl":
            # DataWeave specific rules
            if code.count("map") > 2:  # Simple example - could be more sophisticated
                violations.append({
                    "rule": self.rules["DWL001"],
                    "line": None,
                    "message": "Complex nested mapping detected"
                })

        return violations

    def get_rule_description(self, rule_id: str) -> Optional[SonarRule]:
        """Returns detailed information about a specific rule"""
        return self.rules.get(rule_id)

# Usage example:
if __name__ == "__main__":
    analyzer = MuleSoftSonarRules()
    
    # Example analysis
    mule_code = """<flow name="testFlow">
        <db:mysql-connection username="admin" password="123456"/>
    </flow>"""
    
    violations = analyzer.analyze_code(mule_code, ".xml")
    print(violations)
    print("*"*100)
    for violation in violations:
        print(f"Rule {violation['rule'].rule_id}: {violation['message']}")
        print(f"Severity: {violation['rule'].severity.value}")
        print(f"How to fix: Use {violation['rule'].examples['good']}")
        print("---")