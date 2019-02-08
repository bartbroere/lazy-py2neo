from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import py2neo


class Graph:
    """
    Neo4j queries often only use 1 CPU core.
    This simple wrapper can make it handle a
    defined maximum of concurrent queries.
    It's not very nice, but it could speed things up.
    """

    def __init__(self, *a, concurrent_queries=1, **k):
        self.executor = ThreadPoolExecutor(max_workers=concurrent_queries)
        self.graph = py2neo.Graph(*a, **k)
        self.graphs = Queue()
        for _ in range(concurrent_queries):
            self.graphs.put(py2neo.Graph(*a, **k))
        self.__dict__.update(
            {parent_attribute: self.graph.__getattribute__(parent_attribute)
             for parent_attribute in dir(self.graph)
             if not parent_attribute.startswith('_')
             and parent_attribute not in ['data', 'run']}
        )

    def data(self, *a, **k):
        """
        Does the same things as py2neo.Graph.run, only returns Futures
        instead of results. Call .result() in the calling code to get
        the actual output.
        """
        def graph_data(*a, **k):
            graph = self.graphs.get(block=True)
            data = graph.data(*a, **k)
            self.graphs.put(graph)
            return data
        return self.executor.submit(graph_data, *a, **k)

    def run(self, *a, **k):
        """
        Does the same things as py2neo.Graph.run, only returns Futures
        instead of results. Call .result() in the calling code to get
        the actual output.
        """
        def graph_run(*a, **k):
            graph = self.graphs.get(block=True)
            data = graph.run(*a, **k)
            self.graphs.put(graph)
            return data
        return self.executor.submit(graph_run, *a, **k)
