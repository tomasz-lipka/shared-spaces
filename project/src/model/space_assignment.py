from sqlalchemy import Column, Integer, Boolean
from base import Base


class SpaceAssignment(Base):
    """
    Model of the space assignment entity. It assigns users to their spaces
    """
    __tablename__ = 'space_assignment'

    space_assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    space_id = Column(Integer, nullable=False)
    is_admin = Column(Boolean, default=False)

    def __init__(self, user_id, space_id):
        self.user_id = user_id
        self.space_id = space_id

    def __str__(self):
        return f"SpaceAssignment(space_assignment_id='{self.space_assignment_id}', user_id='{self.user_id}', space_id='{self.space_id}')"

