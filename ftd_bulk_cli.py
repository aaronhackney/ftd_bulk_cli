import argparse
import os
import sys
import time
import requests

BASE_URL = "https://api.us.security.cisco.com/firewall"
PAGE_SIZE = 100


def get_headers():
    token = os.environ.get("API_TOKEN")
    if not token:
        print("Error: API_TOKEN environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def get_manager(session):
    url = f"{BASE_URL}/v1/inventory/managers"
    response = session.get(url, params={"q": "deviceType:CDFMC"})
    response.raise_for_status()
    items = response.json().get("items", [])
    if not items:
        print("Error: No cdFMC manager found.", file=sys.stderr)
        sys.exit(1)
    return items[0]


def get_ftds(session):
    url = f"{BASE_URL}/v1/inventory/devices"
    ftds = []
    offset = 0

    while True:
        params = {
            "q": "deviceType:CDFMC_MANAGED_FTD",
            "limit": PAGE_SIZE,
            "offset": offset,
        }
        response = session.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        items = data.get("items", [])
        ftds.extend(items)

        total_count = data.get("count", 0)
        offset += len(items)

        if offset >= total_count or not items:
            break

    return ftds


def bulk_command(session, cmd, manager, ftds):
    url = f"{BASE_URL}/v1/cdfmc/api/fmc_config/v1/domain/{manager['fmcDomainUid']}/devices/devicerecords/operational/bulkcommands"
    payload = {
        "command": cmd,
        "devices": [ftd["uidOnFmc"] for ftd in ftds],
        "type": "BulkCommand",
    }
    response = session.post(url, json=payload)
    response.raise_for_status()
    return response.json()["metadata"]["task"]


def get_task_status(session, manager, task):
    url = f"{BASE_URL}/v1/cdfmc/api/fmc_config/v1/domain/{manager['fmcDomainUid']}/job/taskstatuses/{task['id']}"
    response = session.get(url)
    response.raise_for_status()
    return response.json()


def download_reports(session, manager, task):
    url = f"{BASE_URL}/v1/cdfmc/api/fmc_config/v1/domain/{manager['fmcDomainUid']}/job/taskstatuses/{task['id']}/operational/downloadreports"
    response = session.get(url)
    response.raise_for_status()
    return response.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", nargs="+", help="Command string (may include spaces)")
    args = parser.parse_args()
    cmd = " ".join(args.cmd)

    session = requests.Session()
    session.headers.update(get_headers())

    manager = get_manager(session)
    print(f"Manager: {manager['address']}")

    ftds = get_ftds(session)
    print(f"Retrieved {len(ftds)} FTD device(s).")

    task = bulk_command(session, cmd, manager, ftds)

    while True:
        task_results = get_task_status(session, manager, task)
        if task_results["status"] == "SUCCESS":
            break
        time.sleep(5)

    reports = download_reports(session, manager, task)
    print(f"Command: {reports['command']}\n")
    for device in reports["deviceResponse"]:
        print(f"Device: {device['deviceName']}")
        print(device["response"])


if __name__ == "__main__":
    main()
