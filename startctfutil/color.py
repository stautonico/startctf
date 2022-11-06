class Colors:
    RESET = "\033[0m"
    BOLD = "\033[01m"
    DISABLE = "\033[02m"
    UNDERLINE = "\033[04m"
    REVERSE = "\033[07m"
    STRIKETHROUGH = "\033[09m"
    INVISIBLE = "\033[08m"

    class FG:
        BLACK = "\033[30m"
        RED = "\033[31m"
        GREEN = "\033[32m"
        ORANGE = "\033[33m"
        BLUE = "\033[34m"
        PURPLE = "\033[35m"
        CYAN = "\033[36m"
        LIGHT_GREY = "\033[37m"
        DARK_GREY = "\033[90m"
        LIGHT_RED = "\033[91m"
        LIGHT_GREEN = "\033[92m"
        YELLOW = "\033[93m"
        LIGHT_BLUE = "\033[94m"
        PINK = "\033[95m"
        LIGHT_CYAN = "\033[96m"

    class BG:
        BLACK = "\033[40m"
        RED = "\033[41m"
        GREEN = "\033[42m"
        ORANGE = "\033[43m"
        BLUE = "\033[44m"
        PURPLE = "\033[45m"
        CYAN = "\033[46m"
        LIGHTGREY = "\033[47m"


DEFAULT_COLOR_MODIFIERS = {
    "bold": False,
    "underline": False,
    "reverse": False,
    "strikethrough": False,
    "invisible": False
}


def colorize(text, color, modifiers=None):
    if modifiers is None:
        modifiers = DEFAULT_COLOR_MODIFIERS

    output = color

    if modifiers.get("bold"):
        output += Colors.BOLD
    if modifiers.get("underline"):
        output += Colors.UNDERLINE
    if modifiers.get("reverse"):
        output += Colors.REVERSE
    if modifiers.get("strikethrough"):
        output += Colors.STRIKETHROUGH
    if modifiers.get("invisible"):
        output += Colors.INVISIBLE

    output += text + Colors.RESET

    return output
