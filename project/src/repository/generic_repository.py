from persistence.sqlalchemy_connector import SQLAlchemyConnector

sql_alchemy_connector = SQLAlchemyConnector()

connection = sql_alchemy_connector.connect()
sql_alchemy_connector.create_schema(connection)
session = sql_alchemy_connector.establish_session(connection)


def add(object):
    """Add or update entity in repo"""
    session.add(object)
    session.commit()


def delete(object):
    """Delete entity from repo"""
    pass


def get_by_id(model, id):
    """Get entity of given model from repo by id"""
    return session.query(model).get(id)


def get_by_filter(model, query_filter):
    """Get entity of given model using a query filter"""
    return session.query(model).filter(query_filter).first()


def get_all(reference_object):
    """Get all entities associated to a given reference object"""
    pass
