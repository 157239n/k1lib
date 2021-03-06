# AUTOGENERATED FILE! PLEASE DON'T EDIT
"""This module is for all things related to atoms, molecules and their simulations"""
import k1lib
from typing import Dict, List
settings = k1lib.Settings().add("overOctet", False, "whether to allow making bonds that exceeds the octet rule")
k1lib.settings.add("mo", settings, "from k1lib.mo module")
__all__ = ["Atom", "substances", "NoFreeElectrons", "OctetFull"]
class NoFreeElectrons(RuntimeError): pass
class OctetFull(RuntimeError): pass
# if Atom's gDepth is smaller than this, then it means that it has not been visited
_depthAuto = k1lib.AutoIncrement()
_idxAuto = k1lib.AutoIncrement()
class Atom:
    """Just an atom really. Has properties, can bond to other atoms, and can
generate a :class:`System` for simulation."""

    def __init__(self, name:str, atomicN:int, massN:float, valenceE:int, radius:List[float]=[], octetE:int=8):
        """Creates a new atom. Not intended to be used by the end user. If you
wish to get a new atom, just do stuff like this::

    c1 = mo.C
    c2 = mo.C
    c1 == c2 # returns False, demonstrating that these are different atoms

If you wish to register new substances with the module, you can do this::

    genF = lambda: Atom(...)
    mo.registerSubstance("elementName", genF)
    mo.elementName # should executes `genF` and returns

:param name: element name (eg. "C")
:param atomicN: atomic number (eg. 6)
:param massN: atomic mass in g/mol (eg. 12)
:param valenceE: how many valence electrons initially?
:param radius: covalent radiuses (in pm) for single, double and triple bonds
:param octetE: how many electrons in a full octet? Default 8, but can be 2 for H and He"""
        self.name = name; self.atomicN = atomicN; self.massN = massN
        self.ogValenceE = valenceE # original
        self.valenceE = valenceE; self.octetE = octetE; self.radius = radius
        self._bonds = [] # list of Atoms this Atom is bonded to
        self.gDepth = -1 # graph depth, for graph traversal stuff. Values will be updated from _depthAuto
        self.idx = f"A{_idxAuto()}" # unique value for Atoms everywhere
        # contracts:
        # - valenceE = eClouds * 2 + freeE + len(bonds) * 2
        # - valenceE <= octetE. "<" happens when octet not full
        # can only form a new bond if freeE >= 1. Can dec eClouds to inc freeE
        if name != "_e":
            self.eClouds = []; self.freeE = valenceE % 2
            for i in range(valenceE//2): self.eClouds.append(mo._e)
        else: self.eClouds = []; self.freeE = 0
    @property
    def bonds(self):
        """List of Atoms bonded to this Atom"""
        return self._bonds
    @bonds.setter
    def bonds(self, v): self._bonds = v
    @property
    def nonHBonds(self) -> List["Atom"]:
        """All atoms this atom is bonded to, minus the Hydrogens."""
        return [a for a in self.bonds if a.name != "H"]
    @property
    def HBonds(self) -> List["Atom"]:
        """All hydrogens this atom is bonded to."""
        return [a for a in self.bonds if a.name == "H"]
    @property
    def uniqueBonds(self) -> List["Atom"]:
        """All unique bonds. Meaning, if there's a double bond, only return 1
atom, not 2."""
        return list(set(self.bonds))
    @property
    def uniqueNonHBonds(self) -> List["Atom"]:
        """All unique non Hydrogen bonds."""
        return list(set(self.nonHBonds))
    def nBonds(self, atom:"Atom"):
        """Get number of bonds between this and another atom."""
        return len([bond for bond in self.bonds if bond == atom])
    @property
    def availableBonds(self) -> int:
        """Available bonds. This includes electron clouds, radical electrons, and
Hydrogen bonds."""
        return len(self.eClouds) * 2 + self.freeE + len([a for a in self.bonds if a.name == "H"])
    def __repr__(self):
        return f"""<Atom {self.name} ({self.atomicN}), {len(self.bonds)} bonds, {self.valenceE}/{self.octetE} valence electrons, {len(self.eClouds)} electron clouds, {self.freeE} free (radical) electrons>"""
@k1lib.patch(Atom)
def _show(self, g=None, gDepth=-1, H:bool=True, GVKwargs={}):
    self.gDepth = gDepth
    if not H:
        nH = len(self.HBonds); nH = "" if nH==0 else ("H" if nH == 1 else f"H{nH}")
        g.node(self.idx, f"{self.name}{nH}", **GVKwargs)
    else: g.node(self.idx, self.name, **GVKwargs)
    for atom in self.bonds:
        if atom.gDepth >= gDepth or (not H and atom.name == "H"): continue
        # all this complexity just to determine arrow direction
        d1 = (self.nonHBonds[0] == atom) if len(self.nonHBonds) > 0 else False
        d2 = (atom.nonHBonds[0] == self) if len(atom.nonHBonds) > 0 else False
        if d1 and d2: g(self.idx, atom.idx, dir="both")
        elif d1: g(self.idx, atom.idx)
        elif d2: g(atom.idx, self.idx)
        else: g(self.idx, atom.idx, arrowhead="none")
    if H: [atom._show(g, gDepth, H) for atom in self.bonds if atom.gDepth < gDepth]
    else: [atom._show(g, gDepth, H) for atom in self.nonHBonds if atom.gDepth < gDepth]
@k1lib.patch(Atom)
def show(self, H:bool=True):
    """Show the molecule graph this atom is a part of. Meant for debugging
simple substances only, as graphs of big molecules look unwieldy. This also
highlights the current :class:`Atom`, and each bond is an arrow, indicating
where :meth:`next` will go next.

:param H: whether to display hydrogens as separate atoms, or bunched into the main atom"""
    g = k1lib.digraph(); self._show(g, _depthAuto(), H, {"style": "filled"}); return g
@k1lib.patch(Atom)
def _addFreeE(self, amt:int=1):
    """Adds free electron to atom."""
    if amt > 1: [self._addFreeE() for i in range(amt)]
    self.freeE += 1
    if self.freeE >= 2: self.eClouds.append(mo._e); self.freeE -= 2
@k1lib.patch(Atom)
def _subFreeE(self, amt:int=1) -> bool:
    """Tries to use ``amt`` free electrons. Returns successful or not."""
    if amt > 1: [self._subFreeE() for i in range(amt)]
    elif self.freeE > 0: self.freeE -= 1
    elif len(self.eClouds) > 0:
        self.freeE += 1; self.eClouds.pop()
    else: raise RuntimeError(f"Can't give away any more free electrons on atom {self.name}!")
@k1lib.patch(Atom)
def _makeRoom(self, nBonds:int):
    """Tries to remove bonds with Hydrogen to make room for ``nBonds`` more bonds."""
    nBondsToRemove = self.valenceE + nBonds - self.octetE
    if nBondsToRemove > 0:
        Hs = [bond for bond in self.bonds if bond.name == "H"]
        if len(Hs) >= nBondsToRemove:
            for i in range(nBondsToRemove): self.removeBond(Hs[i])
        elif not settings.overOctet:
            ans = input(f"Can't remove Hydrogen bonds to make room for new bond! Do you want to do anyway (y/n): ")
            print("Btw, you can auto accept this by doing `settings.mo.overOctet = True`")
            if ans.lower()[0] != "y": raise OctetFull("Stopping...")
    availableE = len(self.eClouds) * 2 + self.freeE
    if availableE < nBonds: raise NoFreeElectrons(f"Can't make room for {nBonds} new bonds on {self.name}. Only {availableE} electrons left for bonds!")
@k1lib.patch(Atom)
def __call__(self, atom:Atom, nBonds:int=1, main=False) -> Atom:
    """Forms a bond with another atom. If valence electrons are full, will
attempt to disconnect Hydrogens from self to make room.

:param bond: number of bonds. 2 for double, 3 for triple
:param main: whether to put this bond in front of existing bonds, to
    signify the "main" chain, so that it works well with :meth:`next`
:return: self"""
    self._makeRoom(nBonds); atom._makeRoom(nBonds)
    if main: self.bonds = [atom] * nBonds + self.bonds
    else: self.bonds += [atom] * nBonds
    atom.bonds += [self] * nBonds
    self.valenceE += nBonds; self._subFreeE(nBonds)
    atom.valenceE += nBonds; atom._subFreeE(nBonds)
    return self
@k1lib.patch(Atom)
def bond(self, atom:Atom, nBonds:int=1, main=False) -> Atom:
    """Like :meth:`__call__`, but returns the atom passed in instead, so you
can form the main loop quickly."""
    self(atom, nBonds, main); return atom
@k1lib.patch(Atom)
def main(self, atom:Atom, nBonds:int=1) -> Atom:
    """Like :meth:`bond`, but with ``main`` param defaulted to True."""
    return self.bond(atom, nBonds, True)
@k1lib.patch(Atom)
def removeBond(self, atom:"Atom"):
    """Removes all bonds between this and another atom"""
    nBonds = self.nBonds(atom)
    self.bonds = [bond for bond in self.bonds if bond != atom]
    self.valenceE -= nBonds; self._addFreeE(nBonds)
    atom.bonds = [bond for bond in atom.bonds if bond != self]
    atom.valenceE -= nBonds; atom._addFreeE(nBonds)
@k1lib.patch(Atom, "next")
def _next(self, offset=0, times:int=1) -> "Atom":
    """Returns the next atom bonded to this. Tries to avoid going into Hydrogens.
This is the main way to navigate around the molecule.

You kinda have to make sure that your molecule's bonding order is appropriate by
choosing between :meth:`bond` and :meth:`main`. Check the bonding order with
:meth:`show`.

:param offset: if there are multiple non-Hydrogen atoms, which ones should I pick?
:param times: how many times do you want to chain ``.next()``?"""
    if times < 0: raise RuntimeError("Can't do .next() with negative `times`")
    if times == 0: return self
    atoms = self.nonHBonds + self.HBonds
    if len(atoms) == 0: return None
    _next = atoms[offset]
    if times == 1: return _next
    else: return _next.next(offset, times-1)
@k1lib.patch(Atom)
def nexts(self, atoms:int=2) -> List[Atom]:
    """Kinda like :meth:`next`, but fetches multiple atoms on the backbone.
Example::

    c1, c2 = mo.CH4(mo.CH4).nexts()"""
    if atoms < 1: raise RuntimeError(f"Zero or negative ({atoms}) number of atoms does not make sense!")
    if atoms == 1: return [self]
    return [self, *(self.next().nexts(atoms-1))]
empiricalOrder = ["C", "H", "O", "N"]
def em1(e:str, n:int):
    if n == 1: return e
    else: return f"{e}{n}"
@k1lib.patch(Atom)
def _empirical(self, d:Dict[str, int], gDepth:int):
    if self.gDepth >= gDepth: return
    self.gDepth = gDepth; d[self.name] += 1
    for atom in self.bonds: atom._empirical(d, gDepth)
@k1lib.patch(Atom)
def empirical(self) -> str:
    """Returns an empirical formula for the molecule this :class:`Atom` is attached to."""
    d = k1lib.Object().withAutoDeclare(lambda: 0)
    self._empirical(d, _depthAuto()); answer = ""
    for e in empiricalOrder:
        if e in d: answer += em1(e,d[e]); del d[e]
    for e in d.state.keys(): answer += em1(e,d[e])
    return answer
@k1lib.patch(Atom)
def _atoms(self, l, gDepth):
    if self.gDepth >= gDepth: return
    self.gDepth = gDepth; l.append(self)
    for atom in self.bonds: atom._atoms(l, gDepth)
@k1lib.patch(Atom)
def atoms(self) -> List[Atom]:
    """Returns a list of Atoms in the molecule this specific Atom is attached to."""
    l = []; self._atoms(l, _depthAuto()); return l
@k1lib.patch(Atom, "endChain")
@property
def endChain(a) -> Atom:
    """Do a bunch of .next() until reached the end of the carbon chain.
Example::

    c1 = mo.alcohol(3, 1)
    c3 = c1.endChain
    c3(mo.NH3)
    c1.show() # displays in cell"""
    lastA = None
    for i in range(200): # for loop to prevent infinite recursion
        nextA = a.next()
        if nextA == lastA: return a
        lastA = a; a = nextA
@k1lib.patch(Atom)
def moveLastCTo2ndC(a:Atom) -> Atom:
    """Move last carbon to 2nd carbon. Useful in constructing iso- and tert-."""
    end = a.endChain; nearEnd = end.next()
    end.removeBond(nearEnd); nearEnd(mo.H); a.next()(mo.CH4); return a
_a = {} # dict of atoms, which will be used to patch the entire module
class _Mo:
    def __init__(self): self._MoWrap_dirs = []
    def registerSubstance(self, name:str, _f):
        setattr(_Mo, name, property(lambda self: _f()))
        self._MoWrap_dirs.append(name)
    def __dir__(self):
        return super().__dir__() + self._MoWrap_dirs
    pass
mo = _Mo() # internal convenience object so that I can use the same style as the module
def _atom(name, *args, **kwargs):
    _a[name] = f = lambda: Atom(name, *args, **kwargs)
    mo.registerSubstance(name, f)
def substances() -> List[str]:
    """Get a list of builtin substances. To register new substances, check over
:class:`Atom`."""
    return [k for k in _a.keys() if not k.startswith("_")]
# covalent radius taken from (Pyykko & Atsumi) https://chem.libretexts.org/@api/deki/pages/2182/pdf/A3%253A%2bCovalent%2bRadii.pdf?stylesheet=default
_atom("_e", 0,   0.1,    0, [25]) # electron cloud, for internal use
_atom("H",  1,   1.008,  1, [32], octetE=2)
_atom("Li", 3,   6.94,   1, [133, 124])
_atom("Be", 4,   9.0122, 2, [102, 90, 85])
_atom("B",  5,  10.81,   3, [85,  78, 73])
_atom("C",  6,  12.011,  4, [75,  67, 60])
_atom("N",  7,  14.007,  5, [71,  60, 54])
_atom("O",  8,  15.999,  6, [63,  57, 53])
_atom("F",  9,  18.998,  7, [64,  59, 53])
_atom("Na", 11, 22.990, 1, [155, 160])
_atom("Mg", 12, 24.305, 2, [139, 132, 127])
_atom("Al", 13, 26.982, 3, [126, 113, 111])
_atom("Si", 14, 28.085, 4, [116, 107, 102])
_atom("P",  15, 30.974, 5, [111, 102, 94])
_atom("S",  16, 32.06,  6, [103, 94,  95])
_atom("Cl", 17, 35.45,  7, [99,  95,  93])
_atom("K",  19,  39.098, 1, [196, 193])
_atom("Ca", 20,  40.078, 2, [171, 147, 133])
_atom("Ga", 31,  69.723, 3, [124, 117, 121])
_atom("Ge", 32,  72.630, 4, [121, 111, 114])
_atom("As", 33,  74.922, 5, [121, 114, 106])
_atom("Se", 34,  78.971, 6, [116, 107, 107])
_atom("Br", 35,  79.904, 7, [114, 109, 110])
_atom("I",  53, 126.9,   7, [133, 129, 125])