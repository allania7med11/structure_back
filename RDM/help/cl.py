from RDM.models import *
from RDM.help.RDM import *
import sympy as sp
import numpy as np
from decimal import *
import json


def fRun(id_pr):
    x = sp.Symbol('x')
    Brs.IN = []
    Brs.Rs = []
    Brs.Eq = []
    Nds_q = Node.objects.filter(project__id=id_pr)
    nd = {gf(Nd, "name"): Nds(Nd) for Nd in Nds_q}
    Brs_q = Bar.objects.filter(project__id=id_pr)
    br = {gf(Br, "name"): Brs(Br) for Br in Brs_q}
    IN = Brs.IN
    Eq = Brs.Eqs(nd, br)
    At = np.mat(fAt(Eq, IN))
    At = np.concatenate(At).astype(None)
    IAt = np.array(At.I)
    Bt = sp.simplify(dt(At, IN) - Eq)
    SO1 = sp.simplify(dt(IAt, Bt))
    SO = [j for j in SO1]
    Vr = dict(zip(IN, SO))
    project = Project.objects.get(pk=id_pr)
    variables={}
    for ky, vl in Vr.items():
        variables[str(ky)]=str(round(vl,13))
    project.variables=variables
    project.save()
    for ky, vl in br.items():
        i = -1
        for v in vl.Qg:
            i = i + 1
            if v in IN:
                vl.Qg[i] = Vr[v]
        vl.Ql = dt(vl.H, tr(vl.Qg))
        dRc = Rc(vl.Ql, vl.L, vl.A, vl.Iy, vl.E, vl.Ch, x)
        vl.Rl = dRc['Rl']
        vl.Rg = dt(tr(vl.H), vl.Rl)
        vl.Req = -dt(tr(vl.H), dRc['Req'])
    Sp = ["Support__{}".format(d) for d in ["UX", "UZ", "RY"]]
    for Nd in Nds_q:
        nd[Nd.name].Rq = np.zeros(3)
        i = -1
        for s in Sp:
            i = i + 1
            for bre in Nd.N1.values_list('name', flat=True):
                nd[Nd.name].Et[i] = nd[Nd.name].Et[i] + br[bre].Req[i]
            for bre in Nd.N2.values_list('name', flat=True):
                nd[Nd.name].Et[i] = nd[Nd.name].Et[i] + br[bre].Req[i + 3]
            if gf(Nd, s):
                nd[Nd.name].Rc[i] = -nd[Nd.name].Fn[i]
                for bre in nd[Nd.name].N1(i):
                    nd[Nd.name].Rc[i] = nd[Nd.name].Rc[i] + br[bre].Rg[i]
                for bre in nd[Nd.name].N2(i):
                    nd[Nd.name].Rc[i] = nd[Nd.name].Rc[i] + br[bre].Rg[i + 3]
                nd[Nd.name].Et[i] = nd[Nd.name].Et[i] + nd[Nd.name].Rc[i]
    VET = np.zeros(3)
    for Nd in Nds_q:
        nd[Nd.name].Et[2] = nd[Nd.name].Et[2] + Nd.X * \
            nd[Nd.name].Et[1] - Nd.Z * nd[Nd.name].Et[0]
        VET = VET + nd[Nd.name].Et
    for v in VET:
        if abs(v) >= 10 ** -7:
            return False

    for ky, vl in br.items():
        vl.Rst()
    for r, v in zip(Brs.Rs, SO):
        if r[0] == 'S':
            nd[r[1]].Dp[r[2]] = v

    for Nd in Nds_q:
        Nd.Fn = nd[Nd.name].Fn.tolist()
        Nd.Dp = nd[Nd.name].Dp.tolist()
        Nd.Rc = nd[Nd.name].Rc.tolist()
        Nd.save()
    for Br in Brs_q:
        Br.L = br[Br.name].L
        Br.Qg = br[Br.name].Qg.tolist()
        Br.Ql = br[Br.name].Ql.tolist()
        Br.Rg = br[Br.name].Rg.tolist()
        Br.Rl = br[Br.name].Rl.tolist()
        Br.EF = {k: ",".join([str(round(v2,13)) for v2 in sp.Poly(v(x), x).all_coeffs()]) for (
            k, v) in zip(["FX", "FZ", "MY"], br[Br.name].EF)}
        Br.EFm = { k:v for (k, v) in zip(["FX", "FZ", "MY"], br[Br.name].EFm)}
        Br.S = {k: ",".join([str(round(v2,10)) for v2 in sp.Poly(v(x), x).all_coeffs()]) for (
            k, v) in zip(["Ssup", "Sinf"], br[Br.name].S)}
        Br.Sm = { k:v for (k, v) in zip(["Ssup", "Sinf"], br[Br.name].Sm)} 
        Br.DP = {k: ",".join([str(round(v2,13)) for v2 in sp.Poly(v(x), x).all_coeffs()]) for (
            k, v) in zip(["UX", "UZ", "RY"], br[Br.name].DP)}
        Br.DPm = { k:v for (k, v) in zip(["UX", "UZ", "RY"], br[Br.name].DPm)}    
        Br.save()
    return True
