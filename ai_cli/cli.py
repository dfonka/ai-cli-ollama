from __future__ import annotations
import json, os, sys
from typing import Optional
import click
from .ollama_client import OllamaClient, OllamaError

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

@click.group(context_settings=dict(help_option_names=['-h','--help']))
@click.option("--host", default=DEFAULT_HOST, show_default=True, help="Base URL of the local Ollama server.")
@click.option("--timeout", default=60, show_default=True, help="HTTP timeout in seconds for Ollama requests.")
@click.pass_context
def cli(ctx: click.Context, host: str, timeout: int):
    """AI CLI powered by a local Ollama instance."""
    ctx.obj = OllamaClient(host=host, timeout=timeout)

@cli.command("list")
@click.pass_obj
def list_cmd(client: OllamaClient):
    """List all Ollama models currently available on the system."""
    try:
        data = client.list_models()
    except OllamaError as e:
        click.echo(f"Error: {e}", err=True); raise SystemExit(1)
    models = data.get("models", [])
    if not models:
        click.echo("No models found. Use `ollama pull <model>` to download one.")
        return
    click.echo(f"Found {len(models)} model(s):\n")
    click.echo(f"{'NAME':40}  {'SIZE':>8}  {'MODIFIED'}")
    click.echo("-"*70)
    for m in models:
        click.echo(f"{m.get('name','?'):40}  {m.get('size',''):>8}  {m.get('modified_at',m.get('modified',''))}")

@cli.command("run")
@click.option("-m","--model",required=True,help="The Ollama model to use (e.g., 'llama3:latest').")
@click.option("--stream/--no-stream",default=False,show_default=True,help="Stream tokens as they are generated.")
@click.option("--system",default=None,help="Optional system prompt to steer behavior.")
@click.option("--options",default=None,help="JSON string of model options (e.g., '{\"temperature\":0.2}').")
@click.option("-f","--file",type=click.Path(exists=True,dir_okay=False,readable=True),help="Read the prompt from a file instead of CLI args/stdin.")
@click.argument("prompt", required=False)
@click.pass_obj
def run_cmd(client: OllamaClient, model:str, stream:bool, system:Optional[str], options:Optional[str], file:Optional[str], prompt:Optional[str]):
    """Send a prompt to a selected model and display the response."""
    if file:
        with open(file,"r",encoding="utf-8") as fh:
            prompt_text = fh.read()
    elif prompt:
        prompt_text = prompt
    else:
        if sys.stdin.isatty():
            click.echo("Enter prompt, then Ctrl-D (macOS/Linux) or Ctrl-Z Enter (Windows):\n", err=True)
        prompt_text = sys.stdin.read()

    prompt_text = prompt_text.strip()
    if not prompt_text:
        click.echo("Error: Prompt is empty.", err=True)
        raise SystemExit(2)

    options_dict = None
    if options:
        try:
            options_dict = json.loads(options)
        except json.JSONDecodeError:
            click.echo("Error: --options must be valid JSON.", err=True)
            raise SystemExit(2)

    try:
        result = client.generate(
            model=model,
            prompt=prompt_text,
            stream=stream,
            system=system,
            options=options_dict,
        )
    except OllamaError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if stream:
        for chunk in result:
            click.echo(chunk, nl=False)
        click.echo()
    else:
        click.echo(result)

def main():
    cli(prog_name="ai-cli")

if __name__ == "__main__":
    main()
