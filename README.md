# lazy_py2neo
Wrapper around py2neo returning Futures, helping support multiple concurrent database queries

**Note: This package has only been tested with py2neo version 3**

Drop in replacement for ``py2neo.Graph``:
```python
from py2neo import Graph
```
becomes
```python
from lazy_py2neo import Graph
```

After changing the import, calls that should return a ``Future`` can be 
modified like this:
```python
graph = Graph()
result = graph.evaluate("MATCH (node) RETURN COUNT(node)")
# result is a dict
```
becomes
```python
graph = Graph()
result = graph.evaluate("MATCH (node) RETURN COUNT(node)", as_future=True)
# result is a Future
evaluated_result = result.result()
# evaluated_result is a dict
```
