import py2neo
from concurrent.futures import ThreadPoolExecutor


class Graph(py2neo.Graph):
    """
    Neo4j queries often only use 1 CPU core.
    This simple wrapper can make it handle a
    defined maximum of concurrent queries.
    It's not very nice, but it could speed things up.
    """

    def __init__(self, *a, concurrent_queries=1, **k):
        self.graphs = ThreadPoolExecutor(max_workers=concurrent_queries)
        super().__init__(*a, **k)

    def run(self, *a, **k):
        """
        Does the same things as py2neo.Graph.run, only returns Futures
        instead of results. Call .result() in the calling code to get
        the actual output.
        """
        return self.graphs.submit(super().run, *a, **k)
