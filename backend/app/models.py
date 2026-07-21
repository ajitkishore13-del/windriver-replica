import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
    tenant_name = Column(String, default="default_tenant")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    groups = Column(JSON, default=list)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    tenant_name = Column(String, default="default_tenant")
    role = Column(String, default="user")
    ldap_group = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    users = Column(JSON, default=list)


class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Blueprint(Base):
    __tablename__ = "blueprints"
    id = Column(String, primary_key=True, index=True)
    description = Column(Text, default="")
    main_file_name = Column(String, default="blueprint.yaml")
    plan = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = Column(String, default="admin")
    tenant_name = Column(String, default="default_tenant")
    visibility = Column(String, default="tenant")
    private_resource = Column(Boolean, default=False)
    labels = Column(JSON, default=list)
    icon = Column(Text, nullable=True)


class Deployment(Base):
    __tablename__ = "deployments"
    id = Column(String, primary_key=True, index=True)
    display_name = Column(String, default="")
    blueprint_id = Column(String, ForeignKey("blueprints.id"), nullable=False)
    blueprint = relationship("Blueprint")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = Column(String, default="admin")
    tenant_name = Column(String, default="default_tenant")
    visibility = Column(String, default="tenant")
    private_resource = Column(Boolean, default=False)
    labels = Column(JSON, default=list)
    inputs = Column(JSON, default=dict)
    outputs = Column(JSON, default=dict)
    capabilities = Column(JSON, default=dict)
    deployment_type = Column(String, default="service")
    site_name = Column(String, nullable=True)
    runtime_only_evaluation = Column(Boolean, default=False)
    skip_plugins_validation = Column(Boolean, default=False)
    status = Column(String, default="active")


class Execution(Base):
    __tablename__ = "executions"
    id = Column(String, primary_key=True, index=True)
    deployment_id = Column(String, ForeignKey("deployments.id"), nullable=False)
    deployment = relationship("Deployment")
    blueprint_id = Column(String, nullable=False)
    workflow_id = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    error = Column(Text, nullable=True)
    created_by = Column(String, default="admin")
    tenant_name = Column(String, default="default_tenant")
    parameters = Column(JSON, default=dict)
    is_system_workflow = Column(Boolean, default=False)
    execution_token = Column(String, nullable=True)


class DeploymentGroup(Base):
    __tablename__ = "deployment_groups"
    id = Column(String, primary_key=True, index=True)
    display_name = Column(String, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String, default="admin")
    tenant_name = Column(String, default="default_tenant")
    visibility = Column(String, default="tenant")
    private_resource = Column(Boolean, default=False)
    description = Column(Text, default="")
    default_blueprint_id = Column(String, nullable=True)
    default_inputs = Column(JSON, default=dict)
    deployment_ids = Column(JSON, default=list)
    labels = Column(JSON, default=list)


class Site(Base):
    __tablename__ = "sites"
    name = Column(String, primary_key=True, index=True)
    location = Column(String, default="")
    tenant_name = Column(String, default="default_tenant")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    visibility = Column(String, default="tenant")


class Secret(Base):
    __tablename__ = "secrets"
    key = Column(String, primary_key=True, index=True)
    value = Column(Text, default="")
    hidden = Column(Boolean, default=False)
    tenant_name = Column(String, default="default_tenant")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    created_by = Column(String, default="admin")
    visibility = Column(String, default="tenant")


class Plugin(Base):
    __tablename__ = "plugins"
    id = Column(String, primary_key=True, index=True)
    package_name = Column(String, default="")
    package_version = Column(String, default="")
    supported_platform = Column(String, default="linux")
    distribution = Column(String, default="centos")
    distribution_release = Column(String, default="core")
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String, default="admin")
    tenant_name = Column(String, default="default_tenant")
    visibility = Column(String, default="tenant")


class Agent(Base):
    __tablename__ = "agents"
    id = Column(String, primary_key=True, index=True)
    host_id = Column(String, nullable=True)
    ip = Column(String, default="127.0.0.1")
    install_method = Column(String, default="remote")
    system = Column(String, default="centos core")
    version = Column(String, default="4.5.0")
    node = Column(String, default="")
    deployment = Column(String, ForeignKey("deployments.id"), nullable=True)
    tenant_name = Column(String, default="default_tenant")


class Filter(Base):
    __tablename__ = "filters"
    id = Column(String, primary_key=True, index=True)
    blueprint_id = Column(String, nullable=True)
    deployment_id = Column(String, nullable=True)
    execution_id = Column(String, nullable=True)
    tenant_name = Column(String, default="default_tenant")
    rules = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(String, unique=True, nullable=False)
    role = Column(String, default="admin")
    username = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    message = Column(Text, default="")
    level = Column(String, default="info")
    event_type = Column(String, default="workflow_succeeded")
    execution_id = Column(String, ForeignKey("executions.id"), nullable=True)
    deployment_id = Column(String, nullable=True)
    blueprint_id = Column(String, nullable=True)
    tenant_name = Column(String, default="default_tenant")


class Snapshot(Base):
    __tablename__ = "snapshots"
    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="created")
    created_by = Column(String, default="admin")
    tenant_name = Column(String, default="default_tenant")
