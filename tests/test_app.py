from pyagent.app import run


def test_run_returns_greeting():
    result = run("Tester")
    assert "Hello" in result
    assert "Tester" in result
