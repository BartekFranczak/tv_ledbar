import zmq

class ZMQClass():
    def __init__(self, pub_port, sub_port, sub_topics):
        self.pub_port = pub_port
        self.sub_port = sub_port
        self.sub_topics = sub_topics

        self.socket_pub = zmq.socket(zmq.PUB)
        self.socket_pub.bind(f"tcp://127.0.0.1:{self.pub_port}")

        self.socket_sub = zmq.socket(zmq.SUB)
        self.socket_sub.bind(f"tcp://127.0.0.1:{self.sub_port}")

        for topic in self.sub_topics:
            config_sub.setsockopt_string(zmq.SUBSCRIBE, topic)   

        self.poller = zmq.Poller()
        self.poller.register(self.socket_pub, zmq.POLLOUT)
        self.poller.register(self.socket_pub, zmq.POLLIN)   
    
    def poll_messages(self):
        events = dict(self.poller.poll())
        if self.socket_sub in events and events[self.socket_sub] == zmq.POLLIN:
            topic, message = self.socket_sub.recv_multipart()
            return topic.decode(), message.decode()
        else:
            return None, None