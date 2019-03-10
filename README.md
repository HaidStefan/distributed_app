# Distributed Calculator
Calculator that splits the calculation of a mathematical expression between multiple machines.

### Generate the stub files:
```python -m grpc_tools.protoc -I ./protos --python_out=. --grpc_python_out=. ./protos/calculator.proto```

### Explanation on resolving the AST
https://stackoverflow.com/questions/20748202/valueerror-malformed-string-when-using-ast-literal-eval