#!/usr/bin/env python3
"""Script de entrada para el servidor MCP en FastMCP Cloud."""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Establecer modo MCP antes de cualquier importación
os.environ["MCP_SERVER_MODE"] = "true"

# Importar y ejecutar el servidor MCP
from app.mcp.server import mcp

if __name__ == "__main__":
    mcp.run()

