#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
result_dir="${1:-results}"
run_mode="${2:-lua}"
if [[ -e "$result_dir" ]]; then
  echo "Choose a new result directory: $result_dir already exists." >&2
  exit 1
fi
case "$run_mode" in
  lua) solver_command=(/opt/femm/bin/femm-lua -h coil.lua) ;;
  python) solver_command=(python3 coil.py) ;;
  python-lua) solver_command=(python3 run_lua_from_python.py) ;;
  *) echo "Mode must be lua, python or python-lua." >&2; exit 1 ;;
esac
mkdir -p -- "$result_dir"
cp -- coil.lua coil.py run_lua_from_python.py "$result_dir/"
task_run_dir="$(realpath -- "$result_dir")"
docker run --rm --init --network none --read-only \
  --tmpfs /tmp:rw,size=256m \
  --user "$(id -u):$(id -g)" \
  -e QT_QPA_PLATFORM=offscreen -e FEMM_MESH_EXPORT=1 \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -e PYTHONPATH=/opt/femm/share/femm/pyfemm \
  -e FEMM_DIR=/opt/femm/bin \
  -e PATH=/opt/femm/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  -v "$task_run_dir:/work" -w /work \
  femm-brain-native:tutorial "${solver_command[@]}"
cat -- "$task_run_dir/results.csv"
