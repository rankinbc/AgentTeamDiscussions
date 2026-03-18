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

    On Windows, long system prompts are passed via stdin to avoid the
    8191-char command line limit.
    """
    use_shell = platform.system() == "Windows"

    if use_shell and len(system_prompt) > 4000:
        cmd = ["claude", "-p", "--output-format", "text"]
        actual_input = (
            f"[SYSTEM INSTRUCTIONS - follow these exactly]\n\n"
            f"{system_prompt}\n\n"
            f"[END SYSTEM INSTRUCTIONS]\n\n"
            f"[USER MESSAGE]\n\n"
            f"{user_message}"
        )
    else:
        cmd = ["claude", "-p", "--system-prompt", system_prompt, "--output-format", "text"]
        actual_input = user_message

    for attempt in range(max_retries + 1):
        try:
            result = subprocess.run(
                cmd,
                input=actual_input,
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
    model: str = None,
) -> str:
    """Async version -- runs claude CLI in a subprocess.

    Uses asyncio subprocess for true concurrency in multi-agent modes.
    On Windows, long system prompts are passed via stdin to avoid the
    8191-char command line limit.
    """
    use_shell = platform.system() == "Windows"

    # On Windows, if the system prompt is long, pass it via stdin
    # by prepending it to the user message with a clear separator
    if use_shell and len(system_prompt) > 4000:
        cmd = [
            "claude",
            "-p",
            "--output-format", "text",
        ]
        if model:
            cmd.extend(["--model", model])
        # Combine system prompt and user message into stdin
        combined_input = (
            f"[SYSTEM INSTRUCTIONS - follow these exactly]\n\n"
            f"{system_prompt}\n\n"
            f"[END SYSTEM INSTRUCTIONS]\n\n"
            f"[USER MESSAGE]\n\n"
            f"{user_message}"
        )
    else:
        cmd = [
            "claude",
            "-p",
            "--system-prompt", system_prompt,
            "--output-format", "text",
        ]
        if model:
            cmd.extend(["--model", model])
        combined_input = user_message

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
            proc.communicate(input=combined_input.encode("utf-8")),
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
