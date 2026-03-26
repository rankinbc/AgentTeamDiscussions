"""Subprocess wrapper for the Claude CLI (sync + async)."""

import asyncio
import platform
import subprocess
import time


def run_claude_sync(
    system_prompt: str,
    user_message: str,
    timeout: int = 120,
    max_retries: int = 2,
) -> str:
    """Run claude CLI synchronously. Returns response text or '[Error...]' string."""
    cmd = ["claude", "-p", "--system-prompt", system_prompt, "--output-format", "text"]
    use_shell = platform.system() == "Windows"

    for attempt in range(max_retries + 1):
        try:
            result = subprocess.run(
                cmd, input=user_message, capture_output=True, text=True,
                encoding="utf-8", timeout=timeout, shell=use_shell,
            )
            output = result.stdout.strip()
            if result.returncode != 0:
                if attempt < max_retries:
                    time.sleep(2)
                    continue
                return f"[Error from claude CLI (exit {result.returncode})]: {result.stderr.strip()}"
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
    """Async version of run_claude_sync. model param is accepted but unused (set via env)."""
    cmd = ["claude", "-p", "--system-prompt", system_prompt, "--output-format", "text"]
    use_shell = platform.system() == "Windows"

    try:
        if use_shell:
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
            return f"[Error from claude CLI (exit {proc.returncode})]: {stderr.decode('utf-8').strip()}"
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
