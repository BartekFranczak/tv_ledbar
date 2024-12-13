#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import json
import zmq

def main(pub_socket,sub_socket):
    context = zmq.Context()

    # Publisher Socket - Other proceses subscribe to this socket
    frontend = context.socket(zmq.XPUB)
    frontend.bind(f"tcp://*:{sub_socket}")

    # Subscriber Socket - Other proceses publish to this socket
    backend = context.socket(zmq.XSUB)
    backend.bind(f"tcp://*:{pub_socket}")

    zmq.proxy(frontend, backend)

    frontend.close()
    backend.close()
    context.term()

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON: {e}")
    except FileNotFoundError:
        print("File not found.")
        
    main(data["zmq_pub_socket"],data["zmq_sub_socket"])
