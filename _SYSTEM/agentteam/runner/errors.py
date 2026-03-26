"""Exception hierarchy for Claude CLI runner errors."""


class ClaudeError(Exception):
    """Base error for all Claude CLI failures."""


class ClaudeTimeoutError(ClaudeError):
    """Claude CLI call exceeded the timeout."""


class ClaudeNotFoundError(ClaudeError):
    """'claude' CLI not found on PATH."""


class ClaudeEmptyResponseError(ClaudeError):
    """Claude CLI returned an empty response."""


class ClaudeProcessError(ClaudeError):
    """Claude CLI exited with a non-zero return code."""
    def __init__(self, message: str, returncode: int = -1):
        super().__init__(message)
        self.returncode = returncode


def is_error_response(response: str) -> bool:
    """Check if a string response from run_claude_* is an error string.

    Legacy helper for code that hasn't migrated to exceptions yet.
    Error strings are prefixed with '['.
    """
    return response.startswith("[")
