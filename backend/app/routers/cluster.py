from fastapi import APIRouter, Depends

from app.auth import verify_basic_auth, get_tenant_header

router = APIRouter(tags=["Cluster"])


@router.get("/managers")
def list_cluster_nodes(
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
):
    return {
        "items": [
            {
                "id": 0,
                "hostname": "node1.windriver.local",
                "private_ip": "172.20.0.2",
                "public_ip": "191.31.72.16",
                "version": "5.1.0",
                "edition": "premium",
                "distribution": "centos",
                "distro_release": "core",
                "fs_sync_node_id": "P56IOI7-MZJNU2Y-IQGDREY-M6J7YFU",
                "networks": {"default": "172.20.0.2", "network_2": "174.40.0.4"},
                "ca_cert_content": "CERT CONTENT",
            }
        ],
        "metadata": {"pagination": {"total": 1, "offset": 0, "size": 1000}},
    }


@router.get("/cluster-status")
def get_cluster_status(
    summary: bool = False,
    _user=Depends(verify_basic_auth),
    tenant: str = Depends(get_tenant_header),
):
    if summary:
        return {"status": "OK", "services": {}}
    return {
        "status": "OK",
        "services": {
            "manager": {
                "status": "OK",
                "nodes": {
                    "cfy-manager": {
                        "status": "OK",
                        "version": "5.1",
                        "public_ip": "172.20.0.2",
                        "private_ip": "172.20.0.2",
                        "services": {
                            "REST Service": {"status": "Active", "extra_info": {}},
                            "Cloudify Composer": {"status": "Active", "extra_info": {}},
                        },
                    }
                },
                "is_external": False,
            },
            "db": {
                "status": "OK",
                "nodes": {
                    "cfy-db": {
                        "status": "OK",
                        "version": "5.1",
                        "private_ip": "172.20.0.2",
                        "services": {
                            "PostgreSQL": {"status": "Active", "extra_info": {}},
                            "Prometheus": {"status": "Active", "extra_info": {}},
                        },
                    }
                },
                "is_external": False,
            },
        },
    }
