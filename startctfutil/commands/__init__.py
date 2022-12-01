from startctfutil.arg_parser import ARG_PARSER
from startctfutil.commands.scripts import command_scripts
from startctfutil.commands.start import command_start


def load_commands():
    ARG_PARSER.add_command("start", command_start)
    ARG_PARSER.add_command("new", command_start)

    ARG_PARSER.add_command("scripts", command_scripts)
    ARG_PARSER.add_command("script", command_scripts)
