"""The Article 1 coil built through FEMM 5's bundled native Python binding.

Run from a new writable result directory. The isolated container launcher
supplies the binding and FEMM binaries. This is not the old PyPI pyfemm 0.1.3.
"""
import csv
import math
from pathlib import Path
import femm

turns, current = 100, 1
ri, ro, length, radius = 1, 2, 1, 4  # inches
mesh_scale = 1
mu0 = 4e-7 * math.pi

femm.openfemm(1)
try:
    femm.newdocument(0)
    femm.callfemm('mi_probdef(0,"inches","axi",1e-8,0,30)')

    femm.mi_addnode(ri,-length/2)
    femm.mi_addnode(ro,-length/2)
    femm.mi_addsegment(ri,-length/2,ro,-length/2)
    femm.mi_addnode(ro,length/2)
    femm.mi_addsegment(ro,-length/2,ro,length/2)
    femm.mi_addnode(ri,length/2)
    femm.mi_addsegment(ro,length/2,ri,length/2)
    femm.mi_addsegment(ri,length/2,ri,-length/2)

    femm.mi_addnode(0,-radius)
    femm.mi_addnode(0,radius)
    femm.mi_addarc(0,-radius,0,radius,180,5)
    femm.mi_addsegment(0,-radius,0,radius)
    femm.mi_addblocklabel((ri+ro)/2,0)
    femm.mi_addblocklabel(.75*radius,0)

    femm.mi_addmaterial("winding",1,1,0,0,0)
    femm.mi_addmaterial("air",1,1,0,0,0)
    femm.mi_addcircprop("coil",current,1)
    femm.mi_selectlabel((ri+ro)/2,0)
    femm.mi_setblockprop("winding",0,radius/20*mesh_scale,"coil",0,0,turns)
    femm.mi_clearselected()
    femm.mi_selectlabel(.75*radius,0)
    femm.mi_setblockprop("air",0,radius/100*mesh_scale,"<None>",0,0,0)
    femm.mi_clearselected()

    femm.mi_addboundprop("open-space",0,0,0,0,0,0,1/(radius*.0254*mu0),0,2)
    femm.mi_selectarcsegment(radius,0)
    femm.mi_setarcsegmentprop(5,"open-space",0,0)
    femm.mi_clearselected()
    femm.mi_saveas(str(Path('coil.fem').resolve()))
    femm.mi_createmesh()
    femm.mi_analyze(1)
    femm.mi_loadsolution()

    applied_current,voltage,linkage=femm.mo_getcircuitproperties("coil")
    point=femm.mo_getpointvalues(0,0)
    values=[('current',applied_current,'A'),('flux_linkage',linkage,'Wb-turn'),
            ('inductance',linkage/applied_current,'H'),('center_Br',point[1],'T'),
            ('center_Bz',point[2],'T'),('elements',femm.mo_numelements(),'count')]
    with open('results.csv','w',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['quantity','value','unit']);writer.writerows(values)
    print(dict((name,value) for name,value,unit in values))
    femm.mo_close()
    femm.mi_close()
finally:
    femm.closefemm()
