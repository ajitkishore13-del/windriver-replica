import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


class PaginationInfo(BaseModel):
    total: int
    offset: int = 0
    size: int = 1000


class PaginationMetadata(BaseModel):
    pagination: PaginationInfo


class PaginatedResponse(BaseModel):
    items: list
    metadata: PaginationMetadata


class BlueprintCreate(BaseModel):
    id: str
    description: Optional[str] = ""
    main_file_name: Optional[str] = "blueprint.yaml"
    plan: Optional[dict] = {}
    visibility: Optional[str] = "tenant"
    labels: Optional[list] = []
    blueprint_archive_url: Optional[str] = None
    application_file_name: Optional[str] = "blueprint.yaml"


class BlueprintUpdate(BaseModel):
    labels: Optional[list] = None
    description: Optional[str] = None


class BlueprintResponse(BaseModel):
    id: str
    description: str = ""
    main_file_name: str = "blueprint.yaml"
    plan: dict = {}
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: str = "admin"
    tenant_name: str = "default_tenant"
    visibility: str = "tenant"
    private_resource: bool = False
    labels: list = []


class DeploymentCreate(BaseModel):
    id: str
    blueprint_id: str
    display_name: Optional[str] = ""
    inputs: Optional[dict] = {}
    visibility: Optional[str] = "tenant"
    site_name: Optional[str] = None
    runtime_only_evaluation: Optional[bool] = False
    skip_plugins_validation: Optional[bool] = False
    labels: Optional[list] = []


class DeploymentUpdate(BaseModel):
    labels: Optional[list] = None
    inputs: Optional[dict] = None
    visibility: Optional[str] = None


class DeploymentResponse(BaseModel):
    id: str
    display_name: str = ""
    blueprint_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: str = "admin"
    tenant_name: str = "default_tenant"
    visibility: str = "tenant"
    private_resource: bool = False
    labels: list = []
    inputs: dict = {}
    outputs: dict = {}
    capabilities: dict = {}
    site_name: Optional[str] = None
    runtime_only_evaluation: bool = False
    skip_plugins_validation: bool = False
    status: str = "active"


class ExecutionStart(BaseModel):
    deployment_id: str
    workflow_id: str
    parameters: Optional[dict] = {}
    force: Optional[bool] = False


class ExecutionAction(BaseModel):
    action: str


class ExecutionResponse(BaseModel):
    id: str
    deployment_id: str
    blueprint_id: str = ""
    workflow_id: str
    status: str
    created_at: datetime.datetime
    started_at: Optional[datetime.datetime] = None
    ended_at: Optional[datetime.datetime] = None
    error: Optional[str] = None
    created_by: str = "admin"
    tenant_name: str = "default_tenant"
    parameters: dict = {}
    is_system_workflow: bool = False


class DeploymentGroupCreate(BaseModel):
    id: str
    display_name: Optional[str] = ""
    description: Optional[str] = ""
    visibility: Optional[str] = "tenant"
    default_blueprint_id: Optional[str] = None
    default_inputs: Optional[dict] = {}
    labels: Optional[list] = []


class DeploymentGroupUpdate(BaseModel):
    display_name: Optional[str] = None
    description: Optional[str] = None
    visibility: Optional[str] = None
    default_blueprint_id: Optional[str] = None
    default_inputs: Optional[dict] = None
    deployment_ids: Optional[list] = None
    labels: Optional[list] = None


class DeploymentGroupResponse(BaseModel):
    id: str
    display_name: str = ""
    description: str = ""
    created_at: datetime.datetime
    created_by: str = "admin"
    tenant_name: str = "default_tenant"
    visibility: str = "tenant"
    private_resource: bool = False
    default_blueprint_id: Optional[str] = None
    default_inputs: dict = {}
    deployment_ids: list = []
    labels: list = []


class SecretCreate(BaseModel):
    key: str
    value: str
    hidden: Optional[bool] = False
    visibility: Optional[str] = "tenant"


class SecretUpdate(BaseModel):
    value: Optional[str] = None
    visibility: Optional[str] = None
    hidden: Optional[bool] = None


class SecretResponse(BaseModel):
    key: str
    hidden: bool = False
    tenant_name: str = "default_tenant"
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: str = "admin"
    visibility: str = "tenant"


class PluginCreate(BaseModel):
    id: str
    package_name: str
    package_version: Optional[str] = "1.0.0"
    supported_platform: Optional[str] = "linux"
    visibility: Optional[str] = "tenant"


class PluginResponse(BaseModel):
    id: str
    package_name: str
    package_version: str
    supported_platform: str
    distribution: str
    distribution_release: str
    uploaded_at: datetime.datetime
    created_by: str = "admin"
    tenant_name: str = "default_tenant"
    visibility: str = "tenant"


class SiteCreate(BaseModel):
    name: str
    location: Optional[str] = ""
    visibility: Optional[str] = "tenant"


class SiteResponse(BaseModel):
    name: str
    location: str = ""
    tenant_name: str = "default_tenant"
    created_at: datetime.datetime
    visibility: str = "tenant"


class AgentResponse(BaseModel):
    id: str
    host_id: Optional[str] = None
    ip: str = "127.0.0.1"
    install_method: str = "remote"
    system: str = "centos core"
    version: str = "4.5.0"
    node: str = ""
    deployment: Optional[str] = None


class FilterCreate(BaseModel):
    id: str
    blueprint_id: Optional[str] = None
    deployment_id: Optional[str] = None
    execution_id: Optional[str] = None
    rules: Optional[dict] = {}


class FilterResponse(BaseModel):
    id: str
    blueprint_id: Optional[str] = None
    deployment_id: Optional[str] = None
    execution_id: Optional[str] = None
    rules: dict = {}
    created_at: datetime.datetime


class TokenResponse(BaseModel):
    value: str
    role: str = "admin"


class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"
    tenant_name: Optional[str] = "default_tenant"


class UserUpdate(BaseModel):
    role: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    username: str
    role: str = "user"
    tenant_name: str = "default_tenant"
    created_at: datetime.datetime
    groups: list = []


class GroupCreate(BaseModel):
    name: str
    role: Optional[str] = "user"
    tenant_name: Optional[str] = "default_tenant"


class GroupUpdate(BaseModel):
    role: Optional[str] = None
    users: Optional[list] = None


class GroupResponse(BaseModel):
    name: str
    role: str = "user"
    tenant_name: str = "default_tenant"
    ldap_group: bool = False
    created_at: datetime.datetime
    users: list = []


class TenantCreate(BaseModel):
    name: str


class TenantResponse(BaseModel):
    name: str
    created_at: datetime.datetime


class EventResponse(BaseModel):
    id: int
    timestamp: datetime.datetime
    message: str = ""
    level: str = "info"
    event_type: str = "workflow_succeeded"
    execution_id: Optional[str] = None
    deployment_id: Optional[str] = None
    blueprint_id: Optional[str] = None


class SnapshotResponse(BaseModel):
    id: str
    created_at: datetime.datetime
    status: str = "created"
    created_by: str = "admin"


class ClusterStatusResponse(BaseModel):
    status: str
    services: dict = {}
