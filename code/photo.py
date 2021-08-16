import numpy
import xraylib


def GetTotalCrossSection(z, energy_array):
    cross_array = []

    for e in energy_array:
        cross_array.append(xraylib.CSb_Photo(z,e))

    return cross_array


def GetShellCrossSection(z, shell, energy_array):
    cross_array = []

    if shell==xraylib.K_SHELL:
        edge = xraylib.EdgeEnergy(z,shell)
    elif shell==xraylib.L1_SHELL:
        if z<=2:
            return cross_array
        else:
            edge = xraylib.EdgeEnergy(z,shell)
    elif shell==xraylib.L2_SHELL:
        if z<=4:
            return cross_array
        else:
            edge = xraylib.EdgeEnergy(z,shell)
    elif shell==xraylib.L3_SHELL:
        if z<=4:
            return cross_array
        else:
            edge = xraylib.EdgeEnergy(z,shell)

    for e in energy_array:
        if shell==xraylib.K_SHELL and ((z<=2 and 10<e) or (3<=z and e<edge)):
            cross_array.append(0)
        elif shell==xraylib.L1_SHELL and e<edge:
            cross_array.append(0)
        elif shell==xraylib.L2_SHELL and e<edge:
            cross_array.append(0)
        elif shell==xraylib.L3_SHELL and e<edge:
            cross_array.append(0)
        else:
            cross_array.append(xraylib.CSb_Photo_Partial(z,shell,e))
    
    return cross_array


def WriteCrossSection(z, shell, energy_array, cross_array):
    if shell==-1:
        name = "pe-cs-{}.dat".format(z)
    elif shell==xraylib.K_SHELL:
        name = "pe-cs-ss-{}-K.dat".format(z)
    elif shell==xraylib.L1_SHELL:
        name = "pe-cs-ss-{}-L1.dat".format(z)
    elif shell==xraylib.L2_SHELL:
        name = "pe-cs-ss-{}-L2.dat".format(z)
    elif shell==xraylib.L3_SHELL:
        name = "pe-cs-ss-{}-L3.dat".format(z)

    with open(name,mode="w") as data:
        for n in range(len(cross_array)):
            data.write("{0:.8e} {1:.8e}\n".format(1e-3*energy_array[n], cross_array[n]))
        data.write("-1 -1\n")
        data.write("-2 -2\n")


if __name__=="__main__":
    energy_array = numpy.logspace(-1,+2,10000)

    for z in range(1,31):
        cross_array_total   = GetTotalCrossSection(z,                   energy_array)
        cross_array_kshell  = GetShellCrossSection(z,  xraylib.K_SHELL, energy_array)
        cross_array_l1shell = GetShellCrossSection(z, xraylib.L1_SHELL, energy_array)
        cross_array_l2shell = GetShellCrossSection(z, xraylib.L2_SHELL, energy_array)
        cross_array_l3shell = GetShellCrossSection(z, xraylib.L3_SHELL, energy_array)
        WriteCrossSection(z,               -1, energy_array, cross_array_total)
        WriteCrossSection(z,  xraylib.K_SHELL, energy_array, cross_array_kshell)
        WriteCrossSection(z, xraylib.L1_SHELL, energy_array, cross_array_l1shell)
        WriteCrossSection(z, xraylib.L2_SHELL, energy_array, cross_array_l2shell)
        WriteCrossSection(z, xraylib.L3_SHELL, energy_array, cross_array_l3shell)
