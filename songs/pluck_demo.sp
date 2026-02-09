# Pluck Demo
# Uses `ipluck` (Karplus-Strong) with a couple settings.

tpluck_demo
s160
o4
v0.95

; warm pluck
ipluck:decay=0.992,bright=0.08,damp=0.45,atk=0.001,rel=0.12
d1/12
C E G C_o5  B A G E  D C r r
r_d1/6

; brighter, snappier
ipluck:decay=0.988,bright=0.22,damp=0.20,atk=0.001,rel=0.08
d1/16
C_o5 C_o5 D_o5 E_o5  G_o5 E_o5 D_o5 C_o5
r_d1/8

; low string
ipluck:decay=0.995,bright=0.06,damp=0.55,atk=0.002,rel=0.20
d1/8
C_o2 r G_o2 r C_o3 r G_o2 r C_o2_d2

