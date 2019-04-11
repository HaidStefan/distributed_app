# Distributed Calculator
Calculator that splits the calculation of a mathematical expression between multiple machines. 
The calculator itself runs on three different machines. The first machine will interpret the 
entered equation and build a AST (abstract syntax tree) that contains operators as intermediate nodes and the numbers as leaves. This tree is then recursively parsed and the calculation either done by machine one or sent to one of the other two machines.

#### Error Handling
When an error occurs during solving an equation, the server sends back an error as the status code.Currently, the following errors are distinguished:  ZeroDivisionError, InvalidExpressionFormat.

### Installing grpc tools:
```python -m pip install grpcio-tools```

```python -m pip install grpcio```

### Generate the stub files:
```python -m grpc_tools.protoc -I ./protos --python_out=. --grpc_python_out=. ./protos/calculator.proto```

### Usage
To use the calculator, start the server_master, server_slave and client. \
\
Start the server master: \
```python server_master.py```

Start the server slave: \
```python server_slave.py```

Start the client: \
```python client.py```

### Resolving the AST 
[Explanation how an AST work](https://stackoverflow.com/questions/20748202/valueerror-malformed-string-when-using-ast-literal-eval)
