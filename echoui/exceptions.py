"""EchoUI exception types."""


class EchoUIError(Exception):
    """Base error for EchoUI."""


class UnsupportedCapability(EchoUIError):
    """Raised when a feature is not available on the current build target."""


class SSSError(EchoUIError):
    """Raised when Screen/Stage/Sprite tree violates SSS rules."""


class CompileError(EchoUIError):
    """Raised when a handler cannot compile to local client JS."""
