from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Workspace(Base):
    __tablename__ = 'workspaces'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)

class Request(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey('workspaces.id'))
    status = Column(String(50), nullable=False, default='PENDING')
    company_name = Column(String(255))
    nit = Column(String(64))
    contract_value = Column(Float)
    term_months = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey('requests.id'))
    path = Column(String(1024))
    pages = Column(Integer)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class ExtractedField(Base):
    __tablename__ = 'extracted_fields'
    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey('requests.id'))
    key = Column(String(255))
    value = Column(Text)
    confidence = Column(Float)
    source = Column(String(32), default='llm')
    evidence_page = Column(Integer)
    evidence_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey('workspaces.id'))
    request_id = Column(Integer, ForeignKey('requests.id'))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    action = Column(String(255))
    field_key = Column(String(255))
    before = Column(Text)
    after = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
