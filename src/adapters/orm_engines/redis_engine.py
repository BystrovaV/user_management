import redis.asyncio as redis


class Redis:
    def __init__(self, session_maker):
        self.session_maker = session_maker

    @classmethod
    def start(cls, database_url: str):
        engine = redis.from_url(database_url)
        print(engine)
        return cls(engine)
