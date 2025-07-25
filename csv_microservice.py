import zmq
import csv
import os

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5554")

print("CSV Microservice started on port 5554")

def convert_value(value, data_type):
    """Convert string value to specified data type"""
    if data_type == "int":
        return int(value)
    elif data_type == "float":
        return float(value)
    elif data_type == "bool":
        return value.lower() in ['true', '1', 'yes', 'on']
    else:
        return value

def handle_import():
    """Import CSV data from ./import.csv"""
    try:
        if not os.path.exists("./import.csv"):
            return {"status": "error", "message": "import.csv not found", "data": None}
        with open("./import.csv", 'r', newline='') as f:
            data = list(csv.DictReader(f))
        return {"status": "success", "message": f"Imported {len(data)} records", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e), "data": None}

def handle_export(data):
    """Export data to ./export.csv"""
    try:
        if not data or not isinstance(data, list):
            return {"status": "error", "message": "Invalid data for export"}
        with open("./export.csv", 'w', newline='') as f:
            if isinstance(data[0], dict):
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            else:
                csv.writer(f).writerows(data)
        return {"status": "success", "message": f"Exported {len(data)} records"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def handle_validate(data, types):
    """Validate and convert data types"""
    try:
        if not data or not types: return {"status": "error", "message": "Invalid data or types"}
        converted = []
        for row in data:
            converted_row = {k: convert_value(v, types[k]) if k in types else v for k, v in row.items()}
            converted.append(converted_row)
        return {"status": "success", "message": f"Validated {len(converted)} records", "data": converted}
    except Exception as e:
        return {"status": "error", "message": str(e)}

while True:
    try:
        request = socket.recv_pyobj()
        print(f"Request: {request}")
        action = request.get("action") if isinstance(request, dict) else None

        if action == "import":
            response = handle_import()
        elif action == "export":
            response = handle_export(request.get("data"))
        elif action == "validate":
            response = handle_validate(request.get("data"), request.get("types"))
        else:
            response = {"status": "error", "message": "Invalid action"}

        print(f"Response: {response}")
        socket.send_pyobj(response)

    except KeyboardInterrupt:
        print("\nShutting down...")
        break
    except Exception as e:
        response = {"status": "error", "message": f"Service error: {str(e)}"}
        socket.send_pyobj(response)

socket.close()
context.term()