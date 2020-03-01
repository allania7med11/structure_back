import numpy.matlib as npm
import sympy as sp
import numpy as np
from math import pi

x = sp.Symbol('x')
t = sp.Symbol('t')
h = sp.Symbol('h')
Nif = ["N{}__name".format(n) for n in range(1, 3)]
Bif = ["i", "f"]
Sps = ["N{}__Support__{}".format(n, d) for n in range(1, 3)
       for d in ["UX", "UZ", "RY"]]
Rls = ["Release__{}{}".format(d, n) for n in range(1, 3)
       for d in ["UX", "UZ", "RY"]]
dp = ["u", "v", "w"]


def Sre(wi, wf, ri, rf, w, r):
    t = sp.Symbol('t')
    L = t * np.zeros((3, 1))

    L[0] = sp.simplify(sp.integrate(sp.integrate(r, (r, ri, rf)), (w, wi, wf)))
    L[1] = 0
    L[2] = sp.simplify(sp.integrate(
        sp.integrate(r ** 3, (r, ri, rf)), (w, wi, wf)))
    return L


def plrstr(exp, x, n, value):
    exp = sp.simplify(exp)*value
    p = plr(exp, x, n)
    return p


def plr(exp, x, n):
    a = sp.Poly(exp, x)
    f = list(reversed(a.all_coeffs()))
    p = 0 * x
    for i in range(len(f)):
        p = p + round(f[i], n) * x ** i
    return p


def Srg(G, w, r):
    t = sp.Symbol('t')
    Lg = t * np.zeros((3, 1))

    for v in G:
        L = Sre(v[0], v[1], v[2], v[3], w, r)
        Lg = Lg + L
    Lg = sp.simplify(Lg)
    Lg = [float(v) for v in Lg]
    return Lg


def Sce(yi, yf, zi, zf, y, z):
    t = sp.Symbol('t')
    L = t * np.zeros((3, 1))

    L[0] = sp.simplify(sp.integrate(sp.integrate(1, (z, zi, zf)), (y, yi, yf)))
    L[1] = sp.simplify(sp.integrate(sp.integrate(z, (z, zi, zf)), (y, yi, yf)))
    L[2] = sp.simplify(sp.integrate(
        sp.integrate(z ** 2, (z, zi, zf)), (y, yi, yf)))
    return L


def Scg(G, y, z):
    t = sp.Symbol('t')
    Lg = t * np.zeros((3, 1))

    for v in G:
        L = Sce(v[0], v[1], v[2], v[3], y, z)
        Lg = Lg + L

    Lg[1] = Lg[1] / Lg[0]
    Lg[2] = Lg[2] - Lg[1] ** 2 * Lg[0]
    Lg = sp.simplify(Lg)
    Lg = [float(v) for v in Lg]
    return Lg


def CG(typ, dn):
    y = sp.Symbol('y')
    z = sp.Symbol('z')
    w = sp.Symbol('w')
    r = sp.Symbol('r')
    if typ == 'Rectangular':
        b, h = dn["b"], dn["h"]
        G = [[-0.5*b, 0.5*b, 0, h]]
        L = Scg(G, y, z)
        L.append(h)
    elif typ == 'Rectangular_Hollow':
        b, h, t = dn["b"], dn["h"], dn["t"]
        G = [[-0.5*b, 0.5*b, 0, h], [-0.5*(b-2*t), 0.5*(b-2*t), b-t, t]]
        L = Scg(G, y, z)
        L.append(h)
    elif typ == 'Circular':
        d = dn["d"]
        A = pi*d**2/4
        O = 0.5*d
        Iy = pi*d**4/64
        H = d
        L = [A, O, Iy, H]
    elif typ == 'Circular_Hollow':
        d, t = dn["d"], dn["t"]
        di = d-2*t
        A = pi * (d ** 2 - di**2) / 4
        O = 0.5*d
        Iy = pi * (d ** 4 - di**4) / 64
        H = d
        L = [A, O, Iy, H]
    elif typ == 'T_Section':
        b, tf, tw, hw = dn["b"], dn["tf"], dn["tw"], dn["hw"],
        G = [[-0.5*tw, 0.5*tw, 0, hw], [-0.5*b, 0.5*b, hw, hw+tf]]
        L = Scg(G, y, z)
        H = hw+tf
        L.append(H)
    elif typ == 'I_Section':
        b1, tf1, tw, hw, b2, tf2 = dn["b1"], dn["tf1"], dn["tw"], dn["hw"], dn["b2"], dn["tf2"]
        G = [[-0.5*b2, 0.5*b2, 0, tf2], [-0.5*tw, 0.5*tw, tf2, tf2+hw],
             [-0.5*b1, 0.5*b1, tf2+hw, tf2+hw+tf1]]
        L = Scg(G, y, z)
        H = hw + tf1+tf2
        L.append(H)
    elif typ == 'Custom':
        L = [dn["Ax"], dn["Cy"], dn["Iy"], dn["H"]]
    rs = {'Ax': L[0], 'Cy': L[1], 'Iy': L[2], 'H': L[3]}
    return rs


def MX(f, L):
    x = sp.Symbol('x')
    y1 = []
    ls = sp.solve(sp.diff(f(x), x), x)
    y1.extend([0])
    for i in range(len(ls)):

        if abs(abs(ls[i]) - ls[i]) < 10 ** -5 * abs(ls[i]) and abs(ls[i]) > 10 ** -5 and abs(ls[i]) < (1 - 10 ** -5) * L:
            y1.extend([abs(ls[i])])
    y1.extend([L])
    y = ",".join([str(x) for x in y1])+";"+",".join([str(f(x)) for x in y1])
    return y


def fAt(Eq, IN):
    n = len(Eq)
    m = len(IN)
    y = x * np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            y[i][j] = sp.diff(Eq[i], IN[j])
    return y


def fcht(chto, L, x):
    cht = x * np.zeros(3)
    i = -1

    for K in chto:
        i = i + 1

        if K[0] != 0 or K[1] != 0:
            cht[i] = K[0] + (K[1] - K[0]) / L * x
    return cht


def tr(v):
    y = np.array(np.transpose(v))
    return y


def dt(v, w):
    y = np.array(np.dot(v, w))
    return y


def intM(M, x, a, b):
    y = x * np.zeros((len(M), len(M[0])))
    n = -1
    for i in M:
        n = n + 1
        m = -1
        for j in i:
            m = m + 1
            y[n][m] = sp.integrate(eval('%s' % (j)), (x, a, b))
    return y


def intV(M, x, a, b):
    y = x * np.zeros(len(M))
    n = -1
    for i in M:
        n = n + 1
        y[n] = sp.integrate(eval('%s' % (i)), (x, a, b))
    return y


def Rc(qe, L, S, I, E, Ch, x):
    N1 = 1 - x / L
    N2 = x / L
    N3 = (2 * x ** 3) / L ** 3 - (3 * x ** 2) / L ** 2 + 1
    N4 = x - (2 * x ** 2) / L + x ** 3 / L ** 2
    N5 = (3 * x ** 2) / L ** 2 - (2 * x ** 3) / L ** 3
    N6 = x ** 3 / L ** 2 - x ** 2 / L
    A = np.array([[N1, 0, 0, N2, 0, 0], [0, N3, N4, 0, N5, N6],
                  [0, sp.diff(N3, x), sp.diff(N4, x), 0, sp.diff(N5, x), sp.diff(N6, x)]])
    B = np.array([[sp.diff(N1, x), 0, 0, sp.diff(N2, x), 0, 0],
                  [0, sp.diff(N3, x, 2), sp.diff(N4, x, 2), 0, sp.diff(N5, x, 2), sp.diff(N6, x, 2)]])
    D = np.array([[E, 0], [0, E * I / S]])
    K1 = dt(dt(tr(B), D), B)
    Ke = np.array(intM(S * K1, x, 0, L))
    Qe = tr(dt(Ke, tr(qe)))
    f = sp.simplify(dt(tr(A), tr(Ch)))
    Req = np.array(-intV(tr(f), x, 0, L))
    Ri = sp.simplify(Qe + Req)
    return {'Rl': Ri, 'Req': Req}


class Nds:
    def __init__(self, Nd):
        self.Nd = Nd
        self.Fn = np.zeros(3)
        self.Et = np.zeros(3)
        self.Dp = np.zeros(3)
        self.Rc = np.zeros(3)
        Fn = np.zeros(3)
        for fn in Nd.pls.all():
            Fn = Fn + np.array([fn.FX, fn.FZ, fn.CY])
        self.Fn = Fn
        self.Et = self.Et + self.Fn

    def N1(self, i):
        return self.Nd.N1.filter(**{Rls[i]: False}).values_list('name', flat=True)

    def N2(self, i):
        return self.Nd.N2.filter(**{Rls[i]: False}).values_list('name', flat=True)


def gf(instance, field):
    ft = field.split('___')
    f1 = ft[0].split('__')
    attr = instance
    for elem in f1:
        try:
            attr = getattr(attr, elem)
        except AttributeError:
            return None
    if len(ft) > 1:
        f2 = ft[1].split('__')
        for elem in f2:
            try:
                attr = attr[elem]
            except AttributeError:
                return None
    return attr


class Brs:
    IN = []
    Rs = []
    Eq = []

    def __init__(self, Br):
        self.Br = Br
        self.L = ((gf(Br, "N2__X") - gf(Br, "N1__X")) ** 2 +
                  (gf(Br, "N2__Z") - gf(Br, "N1__Z")) ** 2) ** 0.5
        co = (gf(Br, "N2__X") - gf(Br, "N1__X")) / self.L
        si = (gf(Br, "N2__Z") - gf(Br, "N1__Z")) / self.L
        self.G = np.mat([[co, si, 0], [-si, co, 0], [0, 0, 1]])
        Z = npm.zeros((3, 3))
        self.H = np.array(np.bmat(([[self.G, Z], [Z, self.G]])))
        qt = x * np.zeros(6)
        for i in range(6):
            if not (gf(Br, Sps[i])):
                if not (gf(Br, Rls[i])):
                    a = sp.Symbol(dp[i % 3] + str(gf(Br, Nif[i // 3])))
                    qt[i] = a
                    if a not in self.IN:
                        self.IN.extend([a])
                        self.Rs.append(['S', gf(Br, Nif[i // 3]), i % 3])
                elif gf(Br, Rls[i]):
                    a = sp.Symbol(dp[i % 3] + Bif[i // 3] +
                                  str(gf(Br, "name")))
                    qt[i] = a
                    if a not in self.IN:
                        self.IN.extend([a])
                        self.Rs.append(['R', gf(Br, 'name'), i])
        self.Qg = qt
        self.Ql = dt(self.H, tr(self.Qg))

        self.Ch = np.zeros(3)

        Ch_u_l = np.zeros(3)
        for c in Br.dls.filter(Axes="L", type="Uniform_Load"):
            ch = c.features
            Ch_u_l = Ch_u_l + np.array([ch['PX'], ch['PZ'], ch['MY']])
        self.Ch = self.Ch + Ch_u_l
        Ch_u_g = np.zeros(3)
        for c in Br.dls.filter(Axes="G", type="Uniform_Load"):
            ch = c.features
            Ch_u_g = Ch_u_g + np.array([ch['PX'], ch['PZ'], ch['MY']])

        self.Ch = self.Ch + dt(self.G, tr(Ch_u_g))

        Ch_t_l = np.zeros((3, 2))
        for c in Br.dls.filter(Axes="L", type="Trapezoidal_Load"):
            ch = c.features
            Ch_t_l = Ch_t_l + \
                np.array([[ch['PX1'], ch['PX2']], [ch['PZ1'],
                                                   ch['PZ2']], [ch['MY1'], ch['MY2']]])
        self.Ch = self.Ch + fcht(Ch_t_l, self.L, x)
        Ch_t_g = np.zeros((3, 2))
        for c in Br.dls.filter(Axes="G", type="Trapezoidal_Load"):
            ch = c.features
            Ch_t_g = Ch_t_g + \
                np.array([[ch['PX1'], ch['PX2']], [ch['PZ1'],
                                                   ch['PZ2']], [ch['MY1'], ch['MY2']]])
        self.Ch = self.Ch + dt(self.G, tr(fcht(Ch_t_g, self.L, x)))
 
        self.A = gf(Br, "Section__Ax")
        Ch_pp = 0
        for c in Br.dls.filter(type="Self_Weight"):
            ch = c.features
            Ch_pp = Ch_pp + ch['Factor']
        Ch_pp_m = Ch_pp * gf(Br, "Section__material__Density") * \
            self.A * np.array([0, -1, 0])
        self.Ch = self.Ch + dt(self.G, tr(Ch_pp_m))

        self.Ch = self.Ch[0]
        self.Iy = gf(Br, "Section__Iy")
        self.vmax = gf(Br, "Section__H")-gf(Br, "Section__Cy")
        self.vmin = - gf(Br, "Section__Cy")
        self.E = gf(Br, "Section__material__YM")
        self.Rl = Rc(self.Ql, self.L, self.A, self.Iy,
                     self.E, self.Ch, x)['Rl']
        self.Rg = dt(tr(self.H), tr(self.Rl))

    @classmethod
    def Eqs(cls, nd, br):
        for L in cls.Rs:
            if L[0] == 'R':
                cls.Eq.extend([-br[L[1]].Rg[L[2]]])
            if L[0] == 'S':
                r = nd[L[1]].Fn[L[2]]
                for bre in nd[L[1]].N1(L[2]):
                    r = r - br[bre].Rg[L[2]]
                for bre in nd[L[1]].N2(L[2]+3):
                    r = r - br[bre].Rg[L[2] + 3]
                cls.Eq.extend([r])
        return cls.Eq

    def Rst(self):
        N = sp.lambdify(t, self.Rl[0] + sp.integrate(self.Ch[0], (x, 0, t)))
        Nm = MX(N, self.L)
        V = sp.lambdify(t, self.Rl[1] + sp.integrate(self.Ch[1], (x, 0, t)))
        Vm = MX(V, self.L)
        Vin = self.Rl[1] + sp.integrate(self.Ch[1], (x, 0, h))
        M = sp.lambdify(
            t, self.Rl[2] - sp.integrate(self.Ch[2], (x, 0, t)) - sp.integrate(Vin, (h, 0, t)))
        Mm = MX(M, self.L)
        self.EF = [N, V, M]
        self.EFm = [Nm, Vm, Mm]
        Ssup = sp.lambdify(x, N(x)/self.A+M(x)*self.vmax/self.Iy)
        Ssupm = MX(Ssup, self.L)
        Sinf = sp.lambdify(x, N(x)/self.A + M(x) * self.vmin / self.Iy)
        Sinfm = MX(Sinf, self.L)
        self.S = [Ssup, Sinf]
        self.Sm = [Ssupm, Sinfm]
        u = sp.lambdify(
            x, self.Ql[0] + sp.integrate(N(t) / (self.E * self.A), (t, 0, x)))
        um = MX(u, self.L)
        win = self.Ql[2] - sp.integrate(M(t) / (self.E * self.Iy), (t, 0, h))
        v = sp.lambdify(x, self.Ql[1] + sp.integrate(win, (h, 0, x)))
        vm = MX(v, self.L)
        w = sp.lambdify(
            x, self.Ql[2] - sp.integrate(M(t) / (self.E * self.Iy), (t, 0, x)))
        wm = MX(w, self.L)
        self.DP = [u, v, w]
        self.DPm = [um, vm, wm]
