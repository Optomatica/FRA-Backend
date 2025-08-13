from sqlalchemy import Column, Integer, String, ForeignKey, Table, ARRAY, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

Base = declarative_base()

# Association table for many-to-many relationship between users and companies
user_company_association = Table(
    'user_company_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('company_id', Integer, ForeignKey('companies.id')),
    Column('created_at', DateTime(timezone=True), server_default=func.now()),
    Column('updated_at', DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to companies
    companies = relationship(
        "Company",
        secondary=user_company_association,
        back_populates="users"
    )

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship to users
    users = relationship(
        "User",
        secondary=user_company_association,
        back_populates="companies"
    )

    # Relationship to files
    files = relationship("File", back_populates="company")

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    vector_ids = Column(ARRAY(String), nullable=False)  # Array of vector IDs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Foreign key to company
    company_id = Column(Integer, ForeignKey('companies.id'))

    # Relationship to company
    company = relationship("Company", back_populates="files")