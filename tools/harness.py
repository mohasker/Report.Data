"""Minimal check harness. Standard library only, so the owner can run it anywhere."""


class Checks:
    def __init__(self, group, purpose):
        self.group = group
        self.purpose = purpose
        self.results = []

    def check(self, cid, description, condition, detail=""):
        passed = bool(condition)
        self.results.append({"id": cid, "description": description,
                             "passed": passed, "detail": str(detail)})
        return passed

    def expect_raises(self, cid, description, fn, exc=Exception, detail=""):
        try:
            fn()
        except exc as e:
            return self.check(cid, description, True, detail or f"rejected: {e}")
        except Exception as e:  # wrong exception type is still a failure
            return self.check(cid, description, False, f"unexpected error: {e!r}")
        return self.check(cid, description, False, "the operation was permitted but should not be")

    @property
    def passed(self):
        return sum(1 for r in self.results if r["passed"])

    @property
    def failed(self):
        return sum(1 for r in self.results if not r["passed"])
