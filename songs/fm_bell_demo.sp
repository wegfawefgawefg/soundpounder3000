# FM Bell Demo
# Uses `ifm` (2-op FM) + ADSR tuned for bell-ish hits.

tfm_bell_demo
s140
o5
v0.9

; bright bell
ifm:car=1,mod=2,idx=5,atk=0.001,dec=0.18,sus=0.0,rel=0.35
d1/8
C r E r G r C_o6 r
r_d1/4

; softer, rounder bell (lower index)
ifm:car=1,mod=3,idx=2.5,atk=0.002,dec=0.22,sus=0.0,rel=0.45
d1/8
F r A r C_o6 r A r
r_d1/4

; little phrase
ifm:car=1,mod=2,idx=4,atk=0.001,dec=0.16,sus=0.0,rel=0.30
d1/16
C D E G  E D C r
d1/8
C_o6 r

