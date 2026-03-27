// ClaudeRunner.cs — Subprocess wrapper for the `claude` CLI tool.
// Every turn is a stateless `claude -p` call (no persistent conversation).
// Platform-aware: uses cmd.exe /c on Windows, direct exec on Unix.
// Retry logic: 2 retries on timeout or empty response, 2s backoff between attempts.
// Never throws — returns error strings like "[Claude CLI timed out after Xs]"
// that downstream health checks detect.

using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;
using EngineStandalone.Abstractions;

namespace EngineStandalone.Runner;

/// <summary>
/// Subprocess wrapper for the Claude CLI (async implementation).
/// </summary>
public class ClaudeRunner : IClaudeRunner
{
    private readonly int _defaultTimeout;
    private readonly int _maxRetries;

    public ClaudeRunner(int defaultTimeout = 120, int maxRetries = 2)
    {
        _defaultTimeout = defaultTimeout;
        _maxRetries = maxRetries;
    }

    /// <summary>
    /// Run claude CLI asynchronously. Returns response text or '[Error...]' string.
    /// </summary>
    public async Task<string> RunAsync(string systemPrompt, string userMessage, int? timeout = null)
    {
        var effectiveTimeout = timeout ?? _defaultTimeout;
        var useShell = RuntimeInformation.IsOSPlatform(OSPlatform.Windows);

        for (int attempt = 0; attempt <= _maxRetries; attempt++)
        {
            try
            {
                var result = await RunClaudeProcessAsync(systemPrompt, userMessage, effectiveTimeout, useShell);

                if (result.ExitCode != 0)
                {
                    if (attempt < _maxRetries)
                    {
                        await Task.Delay(2000);
                        continue;
                    }
                    return $"[Error from claude CLI (exit {result.ExitCode})]: {result.StdErr}";
                }

                if (string.IsNullOrWhiteSpace(result.StdOut))
                {
                    if (attempt < _maxRetries)
                    {
                        await Task.Delay(2000);
                        continue;
                    }
                    return "[Empty response from claude CLI after retries]";
                }

                return result.StdOut.Trim();
            }
            catch (OperationCanceledException)
            {
                if (attempt < _maxRetries)
                {
                    continue;
                }
                return $"[Claude CLI timed out after {effectiveTimeout}s]";
            }
            catch (FileNotFoundException)
            {
                return "[Error: 'claude' CLI not found. Make sure it's installed and on PATH.]";
            }
            catch (Exception ex)
            {
                return $"[Unexpected error: {ex.Message}]";
            }
        }

        return "[Error: Max retries exceeded]";
    }

    /// <summary>
    /// Run claude CLI synchronously. Returns response text or '[Error...]' string.
    /// </summary>
    public string RunSync(string systemPrompt, string userMessage, int? timeout = null)
    {
        return RunAsync(systemPrompt, userMessage, timeout).GetAwaiter().GetResult();
    }

    private async Task<ProcessResult> RunClaudeProcessAsync(string systemPrompt, string userMessage, int timeout, bool useShell)
    {
        var startInfo = new ProcessStartInfo
        {
            FileName = useShell ? "cmd.exe" : "claude",
            RedirectStandardInput = true,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
            StandardInputEncoding = Encoding.UTF8,
            StandardOutputEncoding = Encoding.UTF8,
            StandardErrorEncoding = Encoding.UTF8
        };

        if (useShell)
        {
            // On Windows, use cmd /c to run the command
            var escapedSystemPrompt = systemPrompt.Replace("\"", "\\\"");
            startInfo.Arguments = $"/c claude -p --model claude-sonnet-4-6 --system-prompt \"{escapedSystemPrompt}\" --output-format text";
        }
        else
        {
            startInfo.Arguments = $"-p --model claude-sonnet-4-6 --system-prompt \"{EscapeArgument(systemPrompt)}\" --output-format text";
        }

        using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(timeout));
        using var process = new Process { StartInfo = startInfo };

        var stdOutBuilder = new StringBuilder();
        var stdErrBuilder = new StringBuilder();

        process.OutputDataReceived += (_, e) =>
        {
            if (e.Data != null)
                stdOutBuilder.AppendLine(e.Data);
        };

        process.ErrorDataReceived += (_, e) =>
        {
            if (e.Data != null)
                stdErrBuilder.AppendLine(e.Data);
        };

        try
        {
            process.Start();
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            // Write user message to stdin
            await process.StandardInput.WriteAsync(userMessage);
            await process.StandardInput.FlushAsync();
            process.StandardInput.Close();

            // Wait for exit with timeout
            await process.WaitForExitAsync(cts.Token);

            return new ProcessResult
            {
                ExitCode = process.ExitCode,
                StdOut = stdOutBuilder.ToString(),
                StdErr = stdErrBuilder.ToString()
            };
        }
        catch (OperationCanceledException)
        {
            try
            {
                process.Kill(entireProcessTree: true);
            }
            catch
            {
                // Ignore errors killing the process
            }
            throw;
        }
    }

    private static string EscapeArgument(string arg)
    {
        // Escape double quotes and wrap in quotes if contains spaces
        var escaped = arg.Replace("\\", "\\\\").Replace("\"", "\\\"");
        return escaped;
    }

    private class ProcessResult
    {
        public int ExitCode { get; set; }
        public string StdOut { get; set; } = "";
        public string StdErr { get; set; } = "";
    }
}
