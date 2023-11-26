all:
	python3 -m grpc_tools.protoc  -I. --python_out=. --grpc_python_out=. storage.proto 
	python3 -m grpc_tools.protoc  -I. --python_out=. --grpc_python_out=. centralizer.proto 

clean:
	rm *_pb2*.py

run_serv_pares_1:
	python3 server.py ${arg}
run_serv_pares_2:
	python3 server.py ${arg} flag
run_cli_pares:
	python3 client.py ${arg}
run_cli_central:
	python3 central_client.py ${arg}
run_serv_central:
	python3 central_server.py ${arg}