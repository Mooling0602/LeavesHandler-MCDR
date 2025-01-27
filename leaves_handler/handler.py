import re

# Import apis from MCDReforged for build a server handler.
from typing_extensions import override
from mcdreforged.utils import string_utils
from mcdreforged.info_reactor.info import InfoSource, Info
from mcdreforged.handler.impl import BukkitHandler
# Import a basic plugin api provided by MCDReforged.
from mcdreforged.api.types import PluginServerInterface


def strip_ansi(o: str) -> str:
    """
    Removes ANSI escape sequences from `o`, as defined by ECMA-048 in
    https://www.ecma-international.org/wp-content/uploads/ECMA-48_5th_edition_june_1991.pdf
    """

    pattern = re.compile(r'\x1B\[\d+(;\d+){0,2}m')
    stripped = pattern.sub('', o)
    return stripped

# Core codes for this handler.
class LeavesHandler(BukkitHandler):
    # Name this handler as "leaves_handler".
    def get_name(self) -> str:
        return 'leaves_handler'

    # Parse text log results from the server std output with ANSI codes removed.
    @classmethod
    def get_server_stdout_raw_result(cls, text: str) -> Info:
        if type(text) is not str:
            raise TypeError('The text to parse should be a string')
        result = Info(InfoSource.SERVER, text)
        result.content = strip_ansi(string_utils.clean_console_color_code(text))
        return result

    # Accurate offline player identification.
    __player_left_regex = re.compile(r'(?P<name>[^ ]+) lost connection: (.+)')

    @override
    def parse_player_left(self, info: Info):
        if not info.is_user:
            if (m := self.__player_left_regex.fullmatch(info.content)) is not None:
                if self._verify_player_name(m['name']):
                    return m['name']
        return None

# To load this handler in a simple plugin framework.
def on_load(server: PluginServerInterface, prev_module):
    server.register_server_handler(LeavesHandler())