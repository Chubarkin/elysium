import constants as const


class Command(object):
    TYPE = NotImplemented

    def __init__(self, args_string):
        self._args_string = args_string

    def to_str(self):
        return const.COMMAND_TMPL % (self.TYPE, self._args_string)


class SelectCommand(Command):
    TYPE = const.SELECT


class FromCommand(Command):
    TYPE = const.FROM


class InnerCommand(Command):
    TYPE = const.INNER


class OuterCommand(Command):
    TYPE = const.OUTER


class LeftCommand(Command):
    TYPE = const.LEFT


class RightCommand(Command):
    TYPE = const.RIGHT


class JoinCommand(Command):
    TYPE = const.JOIN


class OnCommand(Command):
    TYPE = const.ON


class WhereCommand(Command):
    TYPE = const.WHERE
