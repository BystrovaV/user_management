from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


class SqlAlchemy:
    def __init__(self, session_maker):
        self.session_maker = session_maker

    @classmethod
    def start(cls, database_url: str):
        engine = create_async_engine(database_url, echo=True, future=True)
        async_session = async_sessionmaker(engine, expire_on_commit=False)

        return cls(async_session)
