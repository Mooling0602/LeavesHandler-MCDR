from mcdreforged.api.all import (
    PluginEvent,
    PluginServerInterface,
    Serializable,
    ServerInterface,
    new_thread,
)

from leaves_handler.handler import LeavesHandler

psi: PluginServerInterface = ServerInterface.psi()


class DefaultConfig(Serializable):
    enable: bool = True


config = DefaultConfig()


def get_config(server: PluginServerInterface) -> DefaultConfig:
    return server.load_config_simple(file_name="config.yml", target_class=DefaultConfig)  # ty: ignore[invalid-return-type]


def disable_register_handler():
    _config = DefaultConfig()
    _config.enable = False
    psi.save_config_simple(config=_config, file_name="config.yml")
    psi.reload_plugin("leaves_handler")


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
    if server.is_server_running():
        event_dispatcher()


def on_server_start_pre(server: PluginServerInterface):
    _event_dispatcher(server)
