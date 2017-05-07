#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import socket,threading
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
global socketio
socketio = SocketIO(app, async_mode=async_mode)
thread = None

#!/usr/bin/python           # This is server.py file

def lauchServer():
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12345               # Reserve a port for your service.
    s.bind((host, port))   
    
    s.listen(5)                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client.
        print('Got connection from %s', addr)
        c.send("welcome")
        while True:
            data=c.recv(1024)
            socketio.emit('my_local_response',{'data': 'MESSAGE FROM TCP SERVER', 'count': data},namespace='/local')
            print(data)
            c.send("messae got ack from server")
            

def background_thread():
    
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12345               # Reserve a port for your service.
    s.bind((host, port)) 
    s.listen(5)                 # Now wait for client connection.
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(2)
        count += 1
        print "custom pring calling from server"
        socketio.emit('my_local_response',{'data': 'Server generated event', 'count': count},namespace='/local')
        c, addr = s.accept()     # Establish connection with client.
        print('Got connection from %s', addr)
        c.send("welcome")
        while True:
            data=c.recv(1024)
            socketio.emit('my_local_response',{'data': 'MESSAGE FROM TCP SERVER', 'count': data},namespace='/local')
            print(data)
            c.send("messae got ack from server")


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


class MyNamespace(Namespace):
    def on_my_event(self, message):
        

               
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']})
        emit('my_local_response',
             {'data': message['data'], 'count': session['receive_count']})

    def on_my_broadcast_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_local_response',
             {'data': message['data'], 'count': session['receive_count']},
             broadcast=True)

  
    def on_disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_local_response',
             {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()

    def on_my_ping(self):
        emit('my_pong')

    def on_connect(self):
        global thread
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
        emit('my_response', {'data': 'Connected', 'count': 0})

    def on_disconnect(self):
        print('Client disconnected', request.sid)


socketio.on_namespace(MyNamespace('/local'))


if __name__ == '__main__':
    #t = threading.Thread(target=lauchServer)
    #t.daemon = True
    #t.start()
    socketio.run(app, debug=True)
