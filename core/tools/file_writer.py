from __future__ import annotations

import logging
from pathlib import Path

from langchain_core.tools import tool
from langchain_core.messages import ToolMessage

# Docs: https://docs.langchain.com/oss/python/langchain/tools   

logger = logging.getLogger(__name__)

@tool("write_text_file")
def write_text_file_tool(path: str, text: str) -> str:
    """Write text to a file at the specified path.

    Args:
        path: The file path where the text should be written.
        text: The text content to write to the file.
    """
    # Force all paths to /tmp
    p = Path(path)
    if p.is_absolute():
        forced_path = Path("/tmp") / p.relative_to(p.anchor)
    else:
        forced_path = Path("/tmp") / p
    
    logger.debug(f"> Writing text to file at {forced_path}")
    
    # Ensure parent directory exists
    forced_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the file
    forced_path.write_text(text)

    return f"SUCCESS: Text written to {forced_path}"
