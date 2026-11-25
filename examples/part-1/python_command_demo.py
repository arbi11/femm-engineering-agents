"""The short command-string example shown in the article; no solve."""
import femm

femm.openfemm(1)
try:
    femm.newdocument(0)
    femm.callfemm('mi_probdef(0,"inches","axi",1e-8,0,30)')
    femm.mi_close()
finally:
    femm.closefemm()
