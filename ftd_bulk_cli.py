import argparse
import os
import sys
import time
import requests

BASE_URL = "https://api.us.security.cisco.com/firewall"
PAGE_SIZE = 100


class SCCClient:
    def __init__(self):
        token = os.environ.get("API_TOKEN")
        if not token:
            print("Error: API_TOKEN environment variable is not set.", file=sys.stderr)
            sys.exit(1)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )
        self.manager = None
        self.ftds = []

    @property
    def _domain_url(self):
        return f"{BASE_URL}/v1/cdfmc/api/fmc_config/v1/domain/{self.manager['fmcDomainUid']}"

    def get_manager(self):
        url = f"{BASE_URL}/v1/inventory/managers"
        response = self.session.get(url, params={"q": "deviceType:CDFMC"})
        response.raise_for_status()
        items = response.json().get("items", [])
        if not items:
            print("Error: No cdFMC manager found.", file=sys.stderr)
            sys.exit(1)
        self.manager = items[0]
        return self.manager

    def get_ftds(self):
        url = f"{BASE_URL}/v1/inventory/devices"
        ftds = []
        offset = 0
        while True:
            params = {
                "q": "deviceType:CDFMC_MANAGED_FTD",
                "limit": PAGE_SIZE,
                "offset": offset,
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            items = data.get("items", [])
            ftds.extend(items)
            total_count = data.get("count", 0)
            offset += len(items)
            if offset >= total_count or not items:
                break
        self.ftds = ftds
        return ftds

    def bulk_command(self, cmd):
        url = f"{self._domain_url}/devices/devicerecords/operational/bulkcommands"
        payload = {
            "command": cmd,
            "devices": [ftd["uidOnFmc"] for ftd in self.ftds],
            "type": "BulkCommand",
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()["metadata"]["task"]

    def get_task_status(self, task):
        url = f"{self._domain_url}/job/taskstatuses/{task['id']}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def wait_for_task(self, task, interval=5):
        while True:
            result = self.get_task_status(task)
            if result["status"] == "SUCCESS":
                return result
            time.sleep(interval)

    def download_reports(self, task):
        url = f"{self._domain_url}/job/taskstatuses/{task['id']}/operational/downloadreports"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def command(self, cmd, device_uid, parameters=None):
        url = f"{self._domain_url}/devices/devicerecords/{device_uid}/operational/commands"
        params = {"command": cmd}
        if parameters is not None:
            params["parameters"] = parameters
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", nargs="+", help="Command string (may include spaces)")
    args = parser.parse_args()
    cmd = " ".join(args.cmd)

    # Create the client
    client = SCCClient()

    # Get the FMC UUID
    manager = client.get_manager()
    print(f"Manager: {manager['address']}")

    # Get the list of FTDs
    ftds = client.get_ftds()
    print(f"Retrieved {len(ftds)} FTD device(s).")

    # Testing a single command execution. This is a synchronous call
    result = client.command(cmd, ftds[0]["uidOnFmc"])

    # Run a bulk command against all devices
    task = client.bulk_command(cmd)

    # Poll for bulk command completion
    client.wait_for_task(task)

    # Get the command results
    # TODO: Deal with paging the result if needed
    reports = client.download_reports(task)

    # Print the results to the terminal
    print(f"Command: {reports['command']}\n")
    for device in reports["deviceResponse"]:
        print(f"Device: {device['deviceName']}")
        print(device["response"])


if __name__ == "__main__":
    main()
