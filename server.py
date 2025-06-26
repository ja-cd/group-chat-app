import eventlet
import socketio

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.event
def connect(sid, environ):
    sio.emit('usercon', sid)
    print('connect ', sid)


@sio.event
def my_message(sid, data):
    print('message ', data)


@sio.on('message')
def message(sid, data):
    print(data['user'] + ": " + data['message'])
    sio.emit('broadcast', data)


@sio.event
def disconnect(sid):
    sio.emit('userdc', sid)
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 3000)), app)
