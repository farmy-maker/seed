import uuid
from config import DEBUG
from data import socketio
from werkzeug.contrib.cache import SimpleCache


cache = SimpleCache()


def get_qr_key():
    qr_key = cache.get('qr_key')
    if not qr_key:
        qr_key = uuid.uuid4().hex[-7:]
        cache.set('qr_key', qr_key)
        cache.set('old_qr_key', '')
    return qr_key


def update_key():
    old_key = cache.get('qr_key')
    new_key = uuid.uuid4().hex[-7:]
    cache.set('qr_key', new_key)
    cache.set('old_qr_key', old_key)
    return new_key


def verify_key(key):
    if DEBUG:
        return True
    if not key:
        return False
    old_key = cache.get('old_qr_key')
    new_key = cache.get('qr_key')
    if key == old_key:
        return True
    elif key == new_key:
        new_key = update_key()
        socketio.emit('qr_code', new_key)
        return True
    else:
        return False

