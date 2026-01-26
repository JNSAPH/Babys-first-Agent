from __future__ import annotations

from pathlib import Path

from langchain_core.tools import tool
from langchain_core.messages import ToolMessage

# Docs: https://docs.langchain.com/oss/python/langchain/tools   

@tool("write_text_file")
def write_text_file_tool(path: str, text: str) -> str:
    """Write text to a file at the specified path.

    Args:
        path: The file path where the text should be written.
        text: The text content to write to the file.
    """
    print("[write_text_file_tool] Writing to file:", path)

    # Make sure the directory is is always in /tmp/
    target = Path("/tmp") / Path(path).relative_to("/").parent
    target.mkdir(parents=True, exist_ok=True)
    file_path = target / Path(path).name    
    with open(file_path, "w") as f:
        f.write(text)

    return f"SUCCESS: Text written to {target}" # Return a confirmation message for the model. If this is not returned, the agent may think the tool call failed and try to call it again.
