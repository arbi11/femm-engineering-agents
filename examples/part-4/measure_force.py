"""Read forces from an existing VM270 model/solution through native FEMM 5.

Run from the directory containing model.fem and model.ans. This script does
not call the field solver or change the physical model.
"""
import json
import math
from pathlib import Path
import femm

femm.openfemm(1)
try:
    # Verify the material-definition excerpt on a separate temporary document.
    femm.newdocument(0)
    mu0 = 4e-7 * math.pi
    Br, Hc = 1.02, 720_000
    mu_r = Br / (mu0 * Hc)
    femm.mi_addmaterial("SmCo", mu_r, mu_r, Hc, 0, 0)
    femm.mi_close()

    femm.opendocument(str(Path('model.fem').resolve()))
    femm.mi_loadsolution()
    femm.mo_selectblock(0.7493, 0.8)
    magnet_force_N = femm.mo_blockintegral(19)
    femm.mo_clearblock()
    femm.mo_selectblock(1.7526, 2.723)
    coil_force_N = femm.mo_blockintegral(12)
    coil_stress_force_N = femm.mo_blockintegral(19)
    femm.mo_clearblock()
    result={'force_magnet_z_N':magnet_force_N,'force_coil_z_N':coil_force_N,
            'force_coil_wst_z_N':coil_stress_force_N,'material_mu_r':mu_r}
    Path('python-force-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    femm.mo_close();femm.mi_close()
finally:
    femm.closefemm()
