# LeavesHandler-MCDR
A plugin-build server handler of MCDReforged for Leaves(a fork of Paper).

> 一个为MCDReforged开发的插件式服务端处理器，适用于Leaves（一个Paper的分支）。

## HandlerMixin Spec / HandlerMixin 规范
LeavesHandler is a standalone server handler, does not provide any handler mixin class.

But it does support and could be managed by [HandlerManager](https://github.com/Mooling0602/HandlerManager-MCDR).

> LeavesHandler 是一个独立的服务端处理器，不提供任何 handler mixin 类。
>
> 但它支持 [HandlerManager](https://github.com/Mooling0602/HandlerManager-MCDR) 并可受其管理。

## NOTE / 注意事项
LeavesHandler is only designed for English log outputs.

LeavesHandler 设计时仅考虑了英文日志输出，不保证能够在中文日志下正常工作，建议不要修改服务端的相关默认配置。
