# CSV Processing Microservice
This microservice provides CSV file import, export, and data validation functionality using ZeroMQ communication protocol.
#
# Requesting Data
To request data, send a Python object using ZeroMQ with the following format:
#
## Request Format
* "action": Operation type ("import", "export", or "validate")
* "data": Array of records (for export and validate operations)
* "types": Data type mapping (for validate operation only)
```
{
  "action": "import"
}
```

```
{
  "action": "export",
  "data": [{"name": "Alice", "age": 25}]
}
```


```
{
  "action": "validate",
  "data": [{"name": "Bob", "age": "30", "active": "true"}],
  "types": {"age": "int", "active": "bool"}
}
```
# Example Code (Sending a Request with ZeroMQ in Python)
