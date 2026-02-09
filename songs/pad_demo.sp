# Pad Demo (no dedicated pad instrument yet)
# This uses `isaw` + slow ADSR + lowpass + filter envelope to get a pad-like swell.

tpad_demo
s90
o4
v0.8

; slow swell pad: saw + filter envelope
isaw:atk=0.25,dec=0.20,sus=0.65,rel=0.60,cut=500,fenv=2800,fatk=0.30,fdec=0.40,fsus=0.0,frel=0.80
d1/2
[ C E G ] r [ A C_o5 E_o5 ] r
[ F A C_o5 ] r [ G B D_o5 ] r
d1
[ C E G ] r [ F A C_o5 ] r [ G B D_o5 ] r [ C_o5 E_o5 G_o5 ] r

