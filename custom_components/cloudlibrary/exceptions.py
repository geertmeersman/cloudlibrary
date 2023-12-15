"""Exceptions used by CloudLibrary."""


class CloudLibraryException(Exception):
    """Base class for all exceptions raised by CloudLibrary."""

    pass


class CloudLibraryServiceException(Exception):
    """Raised when service is not available."""

    pass


class BadCredentialsException(Exception):
    """Raised when credentials are incorrect."""

    pass


class NotAuthenticatedException(Exception):
    """Raised when session is invalid."""

    pass


class GatewayTimeoutException(CloudLibraryServiceException):
    """Raised when server times out."""

    pass


class BadGatewayException(CloudLibraryServiceException):
    """Raised when server returns Bad Gateway."""

    pass
