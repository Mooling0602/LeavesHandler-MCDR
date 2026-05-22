from mcdreforged.api.all import (
    CommandSource,
    PluginEvent,
    PluginServerInterface,
    Serializable,
    ServerInterface,
    SimpleCommandBuilder,
    new_thread,
)

from leaves_handler.handler import LeavesHandler

psi: PluginServerInterface = ServerInterface.psi()  # Ignore runtime issue here.
builder = SimpleCommandBuilder()


class DefaultConfig(Serializable):
    enable: bool = True


config = DefaultConfig()


def get_config(server: PluginServerInterface) -> DefaultConfig:
    return server.load_config_simple(file_name="config.yml", target_class=DefaultConfig)  # ty:ignore[invalid-return-type]


def disable_register_handler():
    """At present only 1 option in config file.
    If more options are added, the code should be modified accordingly.
    """
    _config = DefaultConfig()
    _config.enable = False
    psi.save_config_simple(config=_config, file_name="config.yml")
    psi.reload_plugin(psi.get_self_metadata().id)


def enable_register_handler() -> str | None:
    """At present only 1 option in config file.
    If more options are added, the code should be modified accordingly.
    """
    plugin_id = psi.get_self_metadata().id
    for i in psi.get_plugin_list():
        if "handler" in i and i != plugin_id:
            return "You may loaded conflict plugins, failed to enable LeavesHandler."
    _config = DefaultConfig()
    _config.enable = True
    psi.save_config_simple(config=_config, file_name="config.yml")
    psi.reload_plugin(plugin_id)


class HandlerMixinEvent(PluginEvent):
    def __init__(
        self,
        handler_name: str,
        handler_class: str,
        handler_mixin: str | None,
        handler_register_disabler: str | None,
        spec_version: str = "0.1.0",
    ):
        super().__init__("HandlerMixinEvent")
        self.spec_version = spec_version
        self.handler_name = handler_name
        self.handler_class = handler_class
        self.handler_mixin = handler_mixin
        self.handler_register_disabler = handler_register_disabler
        self.spec_version = spec_version


def _event_dispatcher(server: PluginServerInterface):
    server.logger.info("Dispatching event...")
    event = HandlerMixinEvent(
        "leaves_handler", "LeavesHandler", None, "disable_register_handler"
    )
    server.dispatch_event(event, (event,))


@new_thread("Event Dispatcher")
def event_dispatcher():
    """API for HandlerMixin Spec."""
    _event_dispatcher(psi)


def on_load(server: PluginServerInterface, _):
    global psi, config
    psi = server
    config = get_config(server)
    if config.enable:
        server.register_server_handler(LeavesHandler())
    builder.register(server)
    if server.is_server_running():
        event_dispatcher()


def on_server_start_pre(server: PluginServerInterface):
    _event_dispatcher(server)


@builder.command("!!leaves_handler disable")
def on_disable_handler_command(src: CommandSource):
    if not src.has_permission(4):
        src.reply("Permission denied")
        return
    disable_register_handler()
    src.reply("LeavesHandler will no longer be registered.")


@builder.command("!!leaves_handler enable")
def on_enable_handler_command(src: CommandSource):
    if not src.has_permission(4):
        src.reply("Permission denied")
        return
    msg = enable_register_handler()
    if msg:
        src.reply(msg)
    else:
        src.reply("LeavesHandler will be registered.")