"""EchoUI exception types."""


class EchoUIError(Exception):
    """Base error for EchoUI."""


class UnsupportedCapability(EchoUIError):
    """Raised when a feature is not available on the current build target."""
