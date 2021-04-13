from vexilux import Command
from lightbulb import WrappedArg
from lightbulb.errors import ConverterFailure

async def convert_arg_to_bool(arg: WrappedArg) -> bool:
    """
    Convert a string to a bool (True/true/False/false)
    """

    if arg.data in ("True", "true"):
        return True

    if arg.data in ("False", "false"):
        return False

    raise ConverterFailure

async def command_converter(arg: WrappedArg) -> Command:
    """
    Convert a string to a command object
    """
    
    command = arg.context.bot.get_command(arg.data)
    if not command:
        raise ConverterFailure

    return command