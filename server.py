from concurrent import futures
import grpc 
import time 
import file_pb2
import file_pb2_grpc

class ChatServer(file_pb2_grpc.ChatServerServicer):

    def __init__(self):
        self.chats = []
    
    def ChatStream(self, request, context):
        lastIndex = 0
        while True:
            while len(self.chats) > lastIndex:
                n = self.chats[lastIndex]
                lastIndex += 1
                yield n
    
    def SendNote(self, request, context):
        print("[{}] {}".format(request.name, request.message))
        self.chats.append(request)
        return file_pb2.Empty()
    

if __name__ == "__main__":
    port = 5555 
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_pb2_grpc.add_ChatServerServicer_to_server(ChatServer(), server)
    
    print("Start server. Listening...")
    server.add_insecure_port("[::]:" + str(port))
    server.start()

    while True:
        time.sleep(64 * 64 * 100)