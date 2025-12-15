import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
proto_dir = project_root / "proto"
output_dir = project_root / "app" / "grpc" / "generated"

output_dir.mkdir(parents=True, exist_ok=True)
subprocess.run([
    sys.executable, "-m", "grpc_tools.protoc",
    f"--proto_path={proto_dir}",
    f"--python_out={output_dir}",
    f"--grpc_python_out={output_dir}",
    str(proto_dir / "author.proto")
], check=True)