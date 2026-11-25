-- Air-core coil: complete construction and solve, using FEMM's Lua interface.
-- Geometry follows FEMM's published AirCore short-coil example.
-- Coordinates are inches. Output field components are tesla.
-- Change meshScale to 0.5 for the mesh comparison; keep physics unchanged.
turns = 100
current = 1
ri = 1
ro = 2
length = 1
R = 4
meshScale = 1
mu0 = 4e-7 * 3.141592653589793

-- 1. DC magnetostatics in the radial/axial section.
newdocument(0)
mi_probdef(0,"inches","axi",1e-8,0,30)

-- 2. The four sides of the winding cross-section.
mi_addnode(ri,-length/2)
mi_addnode(ro,-length/2)
mi_addsegment(ri,-length/2,ro,-length/2)
mi_addnode(ro,length/2)
mi_addsegment(ro,-length/2,ro,length/2)
mi_addnode(ri,length/2)
mi_addsegment(ro,length/2,ri,length/2)
mi_addsegment(ri,length/2,ri,-length/2)

-- 3. Surrounding air: a semicircle in section, a sphere after revolution.
mi_addnode(0,-R)
mi_addnode(0,R)
mi_addarc(0,-R,0,R,180,5)
mi_addsegment(0,-R,0,R)
mi_addblocklabel((ri+ro)/2,0)
mi_addblocklabel(0.75*R,0)

-- 4. Air and a homogenized nonmagnetic winding, both with relative mu = 1.
mi_addmaterial("winding",1,1,0,0,0)
mi_addmaterial("air",1,1,0,0,0)
mi_addcircprop("coil",current,1)
mi_selectlabel((ri+ro)/2,0)
mi_setblockprop("winding",0,R/20*meshScale,"coil",0,0,turns)
mi_clearselected()
mi_selectlabel(0.75*R,0)
mi_setblockprop("air",0,R/100*meshScale,"<None>",0,0,0)
mi_clearselected()

-- 5. The source example's mixed asymptotic condition on the outer arc.
mi_addboundprop("open-space",0,0,0,0,0,0,1/(R*0.0254*mu0),0,2)
mi_selectarcsegment(R,0)
mi_setarcsegmentprop(5,"open-space",0,0)
mi_clearselected()

-- 6. Save the model, generate triangles, solve, then open the solution.
mi_saveas("coil.fem")
mi_createmesh()
mi_analyze(1)
mi_loadsolution()

-- 7. Measure the circuit linkage and the field at the center.
I,V,linkage = mo_getcircuitproperties("coil")
L = linkage/I
A,Br,Bz = mo_getpointvalues(0,0)
out = openfile("results.csv","w")
write(out,"quantity,value,unit\n")
write(out,"current,",I,",A\n")
write(out,"flux_linkage,",linkage,",Wb-turn\n")
write(out,"inductance,",L,",H\n")
write(out,"center_Br,",Br,",T\n")
write(out,"center_Bz,",Bz,",T\n")
write(out,"elements,",mo_numelements(),",count\n")
closefile(out)

-- 8. Export samples for the article's plots. These do not affect the solve.
out = openfile("field.csv","w")
write(out,"r_in,z_in,psi_Wb,Br_T,Bz_T\n")
for j=0,120 do
    z = -3.9 + j*7.8/120
    for k=0,60 do
        r = k*3.9/60
        if r*r + z*z < (0.99*R)^2 then
            A,Br,Bz = mo_getpointvalues(r,z)
            write(out,r,",",z,",",A,",",Br,",",Bz,"\n")
        end
    end
end
closefile(out)
out = openfile("axis-field.csv","w")
write(out,"z_in,Bz_T\n")
for j=0,160 do
    z = -3.8 + j*7.6/160
    A,Br,Bz = mo_getpointvalues(0,z)
    write(out,z,",",Bz,"\n")
end
closefile(out)
mo_close()
mi_close()
