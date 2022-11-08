import os
from datetime import datetime
from xml.dom import minidom
from json import loads

from startctfutil.io import error
from startctfutil.config import read_config_key
from startctfutil import is_true


def create_directory_template(name):
    # First, check if the directory exists
    if os.path.exists(name):
        error(f"A directory with the name {name} already exists")
        exit(1)

    # Create the directory that will hold the ctf files
    os.mkdir(name)
    os.chdir(name)

    # Make the directory for storing logs (from enum tools etc.)
    os.mkdir("logs")

    os.makedirs("logs/feroxbuster")
    # Make the directory to store nmap scan results
    os.makedirs("logs/nmap/xml")

    # Make the directory for exfiltrated documents
    os.mkdir("exfiltrated_docs")

    # Make directory for scripts/exploits/etc
    os.mkdir("tools")


def create_readme_template(ctf_name, ip=None):
    author_name = read_config_key("meta", "author")

    if is_true(read_config_key("meta", "use_day_month_year", "false")):
        date = datetime.now().strftime("%d/%m/%Y")
    else:
        date = datetime.now().strftime("%m/%d/%Y")

    # TODO: Make this not so fucking ugly
    readme = f"""> {author_name} - {date}\n# {ctf_name}\n---\n"""
    if is_true(read_config_key("output", "include_field_templates")):
        readme += "A short description of the CTF goes here\n\n"

    readme += """\n### Files\n---\n\n"""

    if is_true(read_config_key("output", "include_field_templates")):
        # Remove the last newline
        readme = readme[:-1]
        readme += """[remote]/home/foo/bar.txt - Some file that contains text
[local, in exfiltrated_docs]baz.txt - Some file that contains text\n\n\n"""
    readme += """### Creds\n---\n"""

    if is_true(read_config_key("output", "include_field_templates")):
        readme += """username:password - Some credentials for ssh @someip\n\n"""

    if ip:
        readme += f"""\n### Host(s) Info\n---\nIP Address: {ip}"""

    with open("README.md", "w") as f:
        f.write(readme)


def parse_nmap_output(output_file):
    result = parse_nmap_output_to_object(output_file)

    with open("README.md", "a") as f:
        f.write("\n### Ports\n---\n")
        # Write the headers
        f.write("| Port | Status | Service |\n")
        f.write("|:----:|:------:|:-------:|\n")
        for port, info in result.items():
            f.write(f"| {port} | {info['status']} | {info['service']} |\n")


def parse_nmap_output_to_object(xml_file):
    result = minidom.parse(xml_file)
    ports = result.getElementsByTagName("port")

    output = {}

    for port in ports:
        state = port.childNodes[0]
        try:
            service = port.childNodes[1]
        except IndexError:
            service = None

        port_number = port.attributes["portid"].value
        port_status = state.attributes["state"].value
        if service:
            service_name = service.attributes["name"].value
        else:
            service_name = "unknown"

        output[port_number] = {
            "status": port_status,
            "service": service_name
        }

    return output


def parse_feroxbuster_output(output_file):
    with open(output_file, "r") as f:
        data = f.read()

    output = []
    for line in data.splitlines():
        if line.startswith("{"):
            data = loads(line)
            if data.get("type") != "statistics":
                output.append([data.get('path', '???'), data.get('status', '???'), data.get("url", "#")])

    port = output_file.split("/")[-1].split(".")[0]

    output_table = "|Path|Status|\n" \
                   "|:---:|:----:|\n"

    for path, status, url in output:
        output_table += f"|[{path}]({url})|{status}|\n"

    with open("README.md", "a") as f:
        f.write(f"\n### Discovered Web Paths (Port {port})\n---\n")
        f.write(output_table)
