import sys
import paho.mqtt.client as mqtt

class RabbitMQMqttClient:
        
    client = None
    isConnected = False
    username = ""
    password = ""
    url = ""
    port = 0
    on_message = None
    on_connect = None
    on_disconnect = None

    def __init__(self, username, password, url, port, on_message , on_connect = None, on_disconnect = None):
        self.username = username
        self.password = password
        self.url = url
        self.port = port
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.on_message = on_message
        #print(on_connect)
        self.connect()
    
    def connect(self):
        print("RabbitMQMqttClient - connect method")
        try:
            if not(self.isConnected):
                self.client = mqtt.Client()    
                self.client.on_connect = self.on_connect_wrapper
                self.client.on_disconnect = self.on_disconnect_wrapper
                self.client.on_message = self.on_message
                self.client.username_pw_set(self.username, self.password)
                self.client.connect(self.url, self.port, 120)  #?????,???1883,?????60?
                self.client.loop_start()
                self.isConnected = True
                print("connected successfully")
            else:
                print("already connected")
        except Exception as e:
            self.isConnected = False
            print("RabbitMQMqttClient - connection faild due to: ", e , " ", sys.exc_info()[0])
        
    def disconnect(self, queue):
        try:
            if self.isConnected:
                self.client.loop_stop()  # Stop loop 
                self.client.disconnect() # disconnect
            else:
                print("already disconnected")
        except:
            print("disconnect, faild due to: ", sys.exc_info()[0])
    
    def on_connect_wrapper(self):
        self.isConnected = True
        if self.on_connect is not None:
            self.on_connect()

    def on_disconnect_wrapper(self):
        self.isConnected = False
        if self.on_disconnect is not None:
            self.on_disconnect()
    
    def publish(self, queue, message):
        try:
            if self.isConnected:
                self.client.publish(queue, message)
                print("publish to queue: ", queue, ", message: ", message, " success")
            else:
                print("publish to queue: ", queue, ", message: ", message, ", faild, not connected")
        except Exception as e:
            print("publish to queue: ", queue, ", message: ", message, ", faild due to: ",  e, " ," , sys.exc_info()[0])
    
    def subscribe(self, queue):
        try:
            if self.isConnected:
                self.client.subscribe(queue)
            else:
                print("subscribtion to queue: ", queue, "faild, not connected")
        except Exception as e:
            print("subscribtion to queue: ", queue, ", faild due to: ", e, " ," , sys.exc_info()[0])
    
        