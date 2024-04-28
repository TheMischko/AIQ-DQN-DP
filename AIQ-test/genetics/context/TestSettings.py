from typing import NamedTuple


class TestSettings(NamedTuple):
    """
    Container for genetic testing context that contains data about AIQ test.
    """
    agent: str
    iterations: int
    samples: int
    threads: int
    log: bool
    log_el: bool
