from . import __name__


CUSTOMERS = {
    "CUST-1001": {
        "name": "Customer A",
        "plan": "Fiber 500",
        "status": "ACTIVE",
    },
    "CUST-1002": {
        "name": "Customer B",
        "plan": "Fiber 1G",
        "status": "SUSPENDED",
    },
}


SERVICE_STATUS = {
    "CUST-1001": {
        "status": "OUTAGE",
        "incident_id": "INC-2045",
    },
    "CUST-1002": {
        "status": "CONNECTED",
        "incident_id": None,
    },
}


def get_customer_account(customer_id: str) -> dict:
    customer = CUSTOMERS.get(customer_id)

    if customer is None:
        return {
            "success": False,
            "error": "Customer not found",
        }

    return {
        "success": True,
        "data": customer,
    }


def get_service_status(customer_id: str) -> dict:
    status = SERVICE_STATUS.get(customer_id)

    if status is None:
        return {
            "success": False,
            "error": "Service status unavailable",
        }

    return {
        "success": True,
        "data": status,
    }


def create_support_ticket(
    customer_id: str,
    description: str,
) -> dict:
    if customer_id not in CUSTOMERS:
        return {
            "success": False,
            "error": "Customer not found",
        }

    # Simulated ticket creation. No external system is called.
    return {
        "success": True,
        "ticket_id": "TICKET-5001",
        "customer_id": customer_id,
        "status": "OPEN",
        "description": description,
    }
