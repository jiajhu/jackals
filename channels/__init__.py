import redis
from utils import synchronized

class RedisChannel(object):
    
    def __init__(self):
        self._redis_conn = redis.StrictRedis()
        self._pubsub = self._redis_conn.pubsub()
    
    @synchronized
    def subscribe(self, cname):
        self._pubsub.subscribe(cname)
        res = self._pubsub.parse_response()
        msg = self._pubsub.handle_message(res)
        if msg and msg.get("type") == "subscribe":
            return True
        return False
    
    def unsubscribe(self, *channels):
        self._pubsub.unsubscribe(*channels)
    
    def publish(self, cname, message):
        if cname in self._pubsub.channels:
            self._redis_conn.publish(cname, message)
            return True
        return False
    
    def get_message(self, cname):
        if cname in self._pubsub.channels:
            msg = self._pubsub.get_message(True)
            if msg:
                return msg.get("data", None)
        return None
    
    def get_file_descriptor(self):
        return self._pubsub.connection._sock.fileno()
    