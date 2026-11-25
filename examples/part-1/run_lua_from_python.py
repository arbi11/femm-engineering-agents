"""Run the unchanged Lua model through FEMM's legacy Lua launcher."""
import subprocess

subprocess.run(
    ["femm-lua", "-h", "coil.lua"], check=True
)
