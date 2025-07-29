class BaseRuleEngine:
    def __init__(self, code: str, language: str):
        self.code = code
        self.language = language
        self.issues = []

    def run(self):
        raise NotImplementedError("Subclasses must implement run()")

    def report(self):
        return self.issues
