import zmq

def test_microservice():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5554")
    print("Connected to CSV Microservice on port 5554\n")
    
    # Create test CSV file
    with open("import.csv", "w") as f:
        f.write("name,age,salary,active\nAlice,25,50000.50,true\nBob,30,75000.75,false\n")
    print("Created import.csv test file")
    
    # Test 1: Import
    print("\n1. Testing IMPORT:")
    socket.send_pyobj({"action": "import"})
    response = socket.recv_pyobj()
    print(f"Status: {response['status']}")
    print(f"Message: {response['message']}")
    
    # Test 2: Export
    print("\n2. Testing EXPORT:")
    test_data = [{"name": "Charlie", "age": 35, "city": "Seattle"}]
    socket.send_pyobj({"action": "export", "data": test_data})
    response = socket.recv_pyobj()
    print(f"Status: {response['status']}")
    print(f"Message: {response['message']}")
    
    # Test 3: Validation
    print("\n3. Testing VALIDATION:")
    validate_data = [{"name": "Diana", "age": "28", "active": "true"}]
    types = {"age": "int", "active": "bool"}
    socket.send_pyobj({"action": "validate", "data": validate_data, "types": types})
    response = socket.recv_pyobj()
    print(f"Status: {response['status']}")
    print(f"Converted data: {response['data']}")
    
    # Test 4: Error handling
    print("\n4. Testing ERROR HANDLING:")
    socket.send_pyobj({"action": "invalid"})
    response = socket.recv_pyobj()
    print(f"Status: {response['status']}")
    print(f"Error: {response['message']}")
    
    socket.close()
    context.term()
    print("\nAll tests completed (Whoop Whoop)!")

if __name__ == "__main__":
    test_microservice()