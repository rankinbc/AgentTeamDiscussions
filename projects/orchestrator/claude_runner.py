"""Subprocess wrapper for the claude CLI."""

import asyncio
import platform
import subprocess
import sys
import time


def run_claude_sync(
    system_prompt: str,
    user_message: str,
    timeout: int = 120,
    max_retries: int = 2,
) -> str:
    """Run claude CLI synchronously with system prompt and message via stdin.

    System prompt goes via --system-prompt flag.
    User message (including conversation history) goes via stdin to avoid
    Windows 8191 char command line limit.
    """
    cmd = [
        "claude",
        "-p",
        "--system-prompt", system_prompt,
        "--output-format", "text",
    ]

    use_shell = platform.system() == "Windows"

    for attempt in range(max_retries + 1):
        try:
            result = subprocess.run(
                cmd,
                input=user_message,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=timeout,
                shell=use_shell,
            )

            output = result.stdout.strip()

            if result.returncode != 0:
                stderr = result.stderr.strip()
                if attempt < max_retries:
                    time.sleep(2)
                    continue
                return f"[Error from claude CLI (exit {result.returncode})]: {stderr}"

            if not output:
                if attempt < max_retries:
                    time.sleep(2)
                    continue
                return "[Empty response from claude CLI after retries]"

            return output

        except subprocess.TimeoutExpired:
            if attempt < max_retries:
                continue
            return f"[Claude CLI timed out after {timeout}s]"
        except FileNotFoundError:
            return "[Error: 'claude' CLI not found. Make sure it's installed and on PATH.]"
        except Exception as e:
            return f"[Unexpected error: {e}]"


async def run_claude_async(
    system_prompt: str,
    user_message: str,
    timeout: int = 120,
) -> str:
    """Async version -- runs claude CLI in a subprocess.

    Uses asyncio subprocess for true concurrency in multi-agent modes.
    """
    cmd = [
        "claude",
        "-p",
        "--system-prompt", system_prompt,
        "--output-format", "text",
    ]

    use_shell = platform.system() == "Windows"

    try:
        if use_shell:
            # On Windows, join command for shell execution
            cmd_str = subprocess.list2cmdline(cmd)
            proc = await asyncio.create_subprocess_shell(
                cmd_str,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        else:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

        stdout, stderr = await asyncio.wait_for(
            proc.communicate(input=user_message.encode("utf-8")),
            timeout=timeout,
        )

        output = stdout.decode("utf-8").strip()

        if proc.returncode != 0:
            err = stderr.decode("utf-8").strip()
            return f"[Error from claude CLI (exit {proc.returncode})]: {err}"

        if not output:
            return "[Empty response from claude CLI]"

        return output

    except asyncio.TimeoutError:
        proc.kill()
        return f"[Claude CLI timed out after {timeout}s]"
    except FileNotFoundError:
        return "[Error: 'claude' CLI not found.]"
    except Exception as e:
        return f"[Unexpected error: {e}]"
