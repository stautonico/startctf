import os
from threading import Thread
from xml.dom import minidom

from startctfutil.arg_parser import get_arg, arg_parser
from startctfutil.io import info, warn
from startctfutil.markdown.table import Table
from startctfutil.readme import README, ReadmeSection, HeadingLevel
from startctfutil.tools import Tool, run

# TODO: Find a better way to do this
group = arg_parser.add_argument_group("nmap")
group.add_argument("-nSA", "--nmap-all", action="store_true",
                   help="Run a full nmap scan on the given ip (all ports, slow)")
group.add_argument("--nmap-Pn", action="store_true", help="Don't ping the target")
group.add_argument("-nSV", "--no-sV", action="store_true",
                   help="Don't run nmap with the -sV flag (don't detect service versions)")
group.add_argument("-nmap-ep", "--nmap-exclude-ports", type=str, help="Ports to exclude from the scan", default="")
group.add_argument("--nmap-args", type=str, help="Extra arguments to pass to nmap", default="")


class nmap(Tool):
    # TODO: Docstring
    def __init__(self):
        super().__init__("nmap", "A tool for network discovery and security auditing")

    def make_log_dir(self) -> None:
        # TODO: Docstring
        if not os.path.exists("logs/nmap"):
            os.mkdir("logs/nmap")
            os.mkdir("logs/nmap/xml")

    def run(self) -> Thread:
        # TODO: Docstring
        if get_arg("ip"):
            command = f"{self.tool_path} {get_arg('ip')} -v"

            if get_arg("nmap_Pn"):
                command += " -Pn"

            if not get_arg("no_sV"):
                command += " -sV"

            if get_arg("exclude_ports") not in ["", None]:
                command += f" --exclude-ports {get_arg('exclude_ports')}"

            if get_arg("nmap_args"):
                command += f" {get_arg('nmap_args')}"

            if get_arg("nmap_all"):
                command += " -p- -oN logs/nmap/all_ports.nmap -oX logs/nmap/xml/all_ports.xml"
            else:
                command += " -oN logs/nmap/initial.nmap -oX logs/nmap/xml/initial.xml"

            # TODO: Change this message based on the verbosity level
            info(f"Running nmap scan on {get_arg('ip')}")

            self.make_log_dir()

            return run(command, f"nmap - {get_arg('ip')}")
        else:
            warn("No IP address provided, skipping nmap scan.")

    def parse_nmap_output_to_object(self, xml_file: str) -> dict:
        # TODO: Docstring
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

    def parse_output(self, file: str) -> None:
        # TODO: Docstring
        result = self.parse_nmap_output_to_object(file)

        table = Table(["Port", "Status", "Service"])
        for port, data in result.items():
            table.add_row([port, data["status"], data["service"]])

        section = ReadmeSection("Ports (nmap)", HeadingLevel.H3)
        section.add_content(table.render())

        README.add_section(section)
