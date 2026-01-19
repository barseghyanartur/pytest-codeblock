```python name=test_async_example
import asyncio

result = await asyncio.sleep(0.1, result=42)
assert result == 42
```
