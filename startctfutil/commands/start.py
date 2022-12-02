import importlib
import sys
from argparse import ArgumentParser

from startctfutil.arg_parser import get_arg, set_args
from startctfutil.files import create_directory_template
from startctfutil.io import info, success, warn, error
from startctfutil.readme import README, ReadmeSection, HeadingLevel
from startctfutil.shared import STATE
from startctfutil.tools import get_preferred_tool, try_import_preferred_tool, SUPPORTED_TOOLS


def command_start():
    # TODO: Docstring
    parser = ArgumentParser(description="Generate the CTF template and start some scans",
                            add_help=False,
                            usage="""startctf start NAME [<args>])""")

    parser.add_argument("name", type=str, help="The name of the ctf (also the name of the created dir)")

    parser.add_argument("--ip", help="The ip address of the target server", required=False)

    # Operation arguments
    parser.add_argument("-ns", "--network-scan", action="store_true", help="Run a simple network scan on the given ip")

    parser.add_argument("-nsa", "--network-scan-all", action="store_true",
                        help="Run a full network scan on the given ip (all ports, slow)")

    parser.add_argument("-as", "--auto-scan", action="store_true",
                        help="Try to detect which services are running on the target and run the appropriate tools (-nS or -nSA required)")

    parser.add_argument("-f", "--force", action="store_true",
                        help="Overwrite existing files (careful, destructive)",
                        default=False)

    parser.add_argument("-st", "--silent-tools", action="store_true",
                        help="Only silence output from tools, but still show status messages")

    parser.add_argument("-nx", "--no-xterm", action="store_true",
                        help="Don't open new xterm windows for each tool (Output for all tools will be shown in the terminal)")

    for category in SUPPORTED_TOOLS:
        for tool in SUPPORTED_TOOLS[category]:
            module = importlib.import_module(f"startctfutil.tools.{tool}")
            try:
                module.make_args(parser.add_argument_group(tool))
            except AttributeError:
                error(
                    f"'{tool}' is not implemented correctly. Missing 'make_args' function. Please open an issue on GitHub.")
                exit(1)

    set_args(parser.parse_args(sys.argv[2:]))

    create_directory_template(get_arg("name"))
    README.add_section(ReadmeSection(get_arg("name"), HeadingLevel.H1))

    if not get_arg("silent_tools"):
        info("Note: Spawned xterm windows may be stacked on top of each other, move them around to see them all")

    network_scanner_thread = None
    network_scanner = None
    preferred_tool = get_preferred_tool("network_scanner")

    if get_arg("network_scan"):
        if preferred_tool is None:
            warn("No network scanner found, skipping network scan")
        else:
            network_scanner = try_import_preferred_tool("network_scanner")
            if network_scanner is None:
                warn("No network scanner found, skipping network scan")
            else:
                network_scanner = network_scanner()
                network_scanner_thread = network_scanner.run()

    # Wait for the threads to finish
    if network_scanner_thread:
        info(f"Waiting for {preferred_tool} to finish...")
        network_scanner_thread.join()
        success(f"{preferred_tool} finished")

        # Parse the output
        network_scanner.parse_output()

        if get_arg("auto_scan"):
            # At this point, the parsed output should be available in the shared data
            threads = {}

            for port, service in STATE["tools"]["network_scanner"]["parsed_output"].items():
                # TODO: Check this is a more thorough and reliable way
                if service["status"] == "open":
                    if "http" in service["service"]:
                        tool = try_import_preferred_tool("web_fuzzer")
                        if tool is None:
                            warn("No web fuzzer found, skipping...")
                        else:
                            tool = tool(port)
                            threads[port] = {
                                "tool": tool,
                                "thread": tool.run()
                            }

            if len(threads) > 0:
                for port, data in threads.items():
                    info(f"Waiting for {data['tool'].name} on port {port} to finish...")
                    data["thread"].join()
                    success(f"{data['tool'].name} on port {port} finished")

                    # TODO: Don't pass the file to the output, have the tool decide what file to parse
                    data["tool"].parse_output()

    README.write()

    success("All done, get to pwning!")
