address = 'localhost'
port = 5555
import grpc
import file_pb2
import file_pb2_grpc
import threading

class Client:
    def __init__(self, u:str, window=False):
        self.window = window
        self.username = u 
        channel = grpc.insecure_channel(address + ":" + str(port))
        self.conn = file_pb2_grpc.ChatServerStub(channel)
        threading.Thread(target=self.__listen_for_message, daemon=True).start()
        #self.__setup_ui()
        #self.window.mainloop()
        self.enter()
    
    def enter(self):
        while(1):
            self.send_message()
        
    
    def __listen_for_message(self):
        for note in self.conn.ChatStream(file_pb2.Empty()):
            print("R[{}] {}".format(note.name, note.message))
            #self.chat_list.insert(END, "[{}] {}\n".format(note.name, note.message))
    
    def send_message(self, event = False):
        message = input()
        if(message != ''):
            n = file_pb2.Note()
            n.name = self.username
            n.message = message
            print("S[{}] {}".format(n.name, n.message))
            self.conn.SendNote(n)
    
    ## Implement the setup function ()


if __name__ == "__main__":
    username = input("Username? ")
    c = Client(username)


