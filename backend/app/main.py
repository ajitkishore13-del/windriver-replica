import hashlib
import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, SessionLocal, Base
from app.models import User, Tenant, Blueprint, Deployment, Execution, Secret, Plugin, Site, Agent, Group, Event, Snapshot
from app.routers import (
    status, tokens, blueprints, deployments, executions, deployment_groups,
    agents, secrets, plugins, sites, filters, users, groups as groups_router,
    tenants, events, snapshots, cluster, labels,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WindRiver Studio Conductor API",
    description="Replica of WindRiver Studio Conductor REST API v3.1",
    version="3.1.0",
    docs_url="/api/docs",
    openapi_url="/api/docs.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(status.router, prefix="/api/v3.1")
app.include_router(tokens.router, prefix="/api/v3.1")
app.include_router(blueprints.router, prefix="/api/v3.1")
app.include_router(deployments.router, prefix="/api/v3.1")
app.include_router(executions.router, prefix="/api/v3.1")
app.include_router(deployment_groups.router, prefix="/api/v3.1")
app.include_router(agents.router, prefix="/api/v3.1")
app.include_router(secrets.router, prefix="/api/v3.1")
app.include_router(plugins.router, prefix="/api/v3.1")
app.include_router(sites.router, prefix="/api/v3.1")
app.include_router(filters.router, prefix="/api/v3.1")
app.include_router(users.router, prefix="/api/v3.1")
app.include_router(groups_router.router, prefix="/api/v3.1")
app.include_router(tenants.router, prefix="/api/v3.1")
app.include_router(events.router, prefix="/api/v3.1")
app.include_router(snapshots.router, prefix="/api/v3.1")
app.include_router(cluster.router, prefix="/api/v3.1")
app.include_router(labels.router, prefix="/api/v3.1")


def seed_data():
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            return

        admin_hash = hashlib.sha256(b"admin").hexdigest()
        admin = User(username="admin", password=admin_hash, role="sys-admin", tenant_name="default_tenant")
        dev = User(username="developer", password=admin_hash, role="user", tenant_name="default_tenant")
        db.add_all([admin, dev])

        db.add(Tenant(name="default_tenant"))

        dev_group = Group(name="developers", role="user", tenant_name="default_tenant", users=["developer", "admin"])
        db.add(dev_group)

        now = datetime.datetime.utcnow()
        blueprints = [
            Blueprint(
                id="hello-world",
                description="A simple web server blueprint",
                main_file_name="singlehost-blueprint.yaml",
                plan={"node_templates": {"http_server": {"type": "cloudify.nodes.WebServer"}}},
                created_by="admin", tenant_name="default_tenant",
                labels=[{"type": "web"}, {"os": "linux"}],
                created_at=now, updated_at=now,
            ),
            Blueprint(
                id="kubernetes-cluster",
                description="Kubernetes cluster deployment blueprint",
                main_file_name="k8s-blueprint.yaml",
                plan={"node_templates": {"k8s_master": {"type": "cloudify.nodes.kubernetes.Master"}}},
                created_by="admin", tenant_name="default_tenant",
                labels=[{"type": "kubernetes"}, {"os": "linux"}],
                created_at=now, updated_at=now,
            ),
            Blueprint(
                id="iot-edge-gateway",
                description="IoT Edge gateway with MQTT broker",
                main_file_name="iot-gateway.yaml",
                plan={"node_templates": {"mqtt_broker": {"type": "cloudify.nodes.mqtt.Broker"}}},
                created_by="developer", tenant_name="default_tenant",
                labels=[{"type": "iot"}, {"protocol": "mqtt"}],
                created_at=now, updated_at=now,
            ),
        ]
        db.add_all(blueprints)

        deployments = [
            Deployment(id="hello-world-dep-1", display_name="Hello World Production",
                       blueprint_id="hello-world", outputs={"endpoint": "http://10.0.0.1:8080"},
                       capabilities={"health_url": "http://10.0.0.1:8080/health"},
                       created_by="admin", tenant_name="default_tenant", status="active",
                       labels=[{"env": "production"}], created_at=now, updated_at=now),
            Deployment(id="hello-world-dep-2", display_name="Hello World Staging",
                       blueprint_id="hello-world", outputs={"endpoint": "http://10.0.0.2:8080"},
                       capabilities={"health_url": "http://10.0.0.2:8080/health"},
                       created_by="admin", tenant_name="default_tenant", status="active",
                       labels=[{"env": "staging"}], created_at=now, updated_at=now),
            Deployment(id="k8s-prod", display_name="Kubernetes Production Cluster",
                       blueprint_id="kubernetes-cluster",
                       outputs={"api_server": "https://10.0.0.10:6443"},
                       capabilities={"node_count": 5},
                       created_by="admin", tenant_name="default_tenant", status="active",
                       labels=[{"env": "production"}], created_at=now, updated_at=now),
            Deployment(id="iot-gateway-1", display_name="IoT Gateway - Factory Floor A",
                       blueprint_id="iot-edge-gateway",
                       outputs={"mqtt_endpoint": "tcp://10.0.0.20:1883"},
                       capabilities={"device_count": 42},
                       created_by="developer", tenant_name="default_tenant", status="active",
                       labels=[{"env": "production"}, {"site": "factory-a"}], created_at=now, updated_at=now),
        ]
        db.add_all(deployments)

        exec_statuses = ["started", "succeeded", "failed", "cancelled", "pending"]
        executions = []
        for i, dep in enumerate(deployments):
            for j, wf in enumerate(["install", "uninstall", "heal", "scale"]):
                status = exec_statuses[(i + j) % len(exec_statuses)]
                e = Execution(
                    id=f"exec_{dep.id}_{wf}_{i}_{j}",
                    deployment_id=dep.id,
                    blueprint_id=dep.blueprint_id,
                    workflow_id=wf,
                    status=status,
                    started_at=now - datetime.timedelta(hours=i + j + 1),
                    ended_at=now - datetime.timedelta(hours=i + j) if status in ("succeeded", "failed", "cancelled") else None,
                    parameters={"input_key": f"value_{i}_{j}"},
                    created_by="admin",
                    tenant_name="default_tenant",
                    execution_token=f"token_{i}_{j}_{hashlib.md5(f'{i}{j}'.encode()).hexdigest()[:16]}",
                    error="Deployment failed" if status == "failed" else None,
                )
                executions.append(e)
        db.add_all(executions)

        secrets = [
            Secret(key="aws_access_key", value="AKIA****EXAMPLE", hidden=True, tenant_name="default_tenant",
                   created_by="admin", created_at=now, updated_at=now),
            Secret(key="db_password", value="supersecret123", hidden=True, tenant_name="default_tenant",
                   created_by="admin", created_at=now, updated_at=now),
        ]
        db.add_all(secrets)

        plugins = [
            Plugin(id="cloudify-openstack-plugin", package_name="cloudify-openstack-plugin",
                   package_version="3.2.1", tenant_name="default_tenant", created_by="admin"),
            Plugin(id="cloudify-kubernetes-plugin", package_name="cloudify-kubernetes-plugin",
                   package_version="2.8.0", tenant_name="default_tenant", created_by="admin"),
            Plugin(id="cloudify-ansible-plugin", package_name="cloudify-ansible-plugin",
                   package_version="2.6.3", tenant_name="default_tenant", created_by="admin"),
        ]
        db.add_all(plugins)

        sites = [
            Site(name="us-east-1", location="Virginia, USA", tenant_name="default_tenant"),
            Site(name="eu-west-1", location="Dublin, Ireland", tenant_name="default_tenant"),
            Site(name="ap-southeast-1", location="Singapore", tenant_name="default_tenant"),
        ]
        db.add_all(sites)

        agents = [
            Agent(id="agent-node-1", host_id="host-1", ip="10.0.0.101",
                  system="ubuntu 22.04", version="4.5.0", node="http_server",
                  deployment="hello-world-dep-1", tenant_name="default_tenant"),
            Agent(id="agent-node-2", host_id="host-2", ip="10.0.0.102",
                  system="centos core", version="4.5.0", node="k8s_master",
                  deployment="k8s-prod", tenant_name="default_tenant"),
        ]
        db.add_all(agents)

        for i in range(20):
            db.add(Event(
                message=f"Workflow execution event #{i + 1}",
                level="info" if i % 4 != 0 else "error",
                event_type="workflow_succeeded" if i % 4 != 0 else "workflow_failed",
                execution_id=executions[i % len(executions)].id,
                deployment_id=deployments[i % len(deployments)].id,
                blueprint_id=blueprints[i % len(blueprints)].id,
                tenant_name="default_tenant",
                timestamp=now - datetime.timedelta(minutes=i * 15),
            ))

        db.commit()
        print("Seed data loaded successfully")
    finally:
        db.close()


seed_data()
