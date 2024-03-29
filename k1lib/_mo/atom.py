# AUTOGENERATED FILE! PLEASE DON'T EDIT HERE. EDIT THE SOURCE NOTEBOOKS INSTEAD
"""This module is for all things related to atoms, molecules and their simulations"""
import k1lib
from typing import Dict, List
settings = k1lib.Settings().add("overOctet", False, "whether to allow making bonds that exceeds the octet rule")
k1lib.settings.add("mo", settings, "from k1lib.mo module")
__all__ = ["Atom", "substances", "NoFreeElectrons", "OctetFull"]
class NoFreeElectrons(RuntimeError): pass                                        # NoFreeElectrons
class OctetFull(RuntimeError): pass                                              # OctetFull
# if Atom's gDepth is smaller than this, then it means that it has not been visited # OctetFull
_depthAuto = k1lib.AutoIncrement()                                               # OctetFull
_idxAuto = k1lib.AutoIncrement()                                                 # OctetFull
class Atom:                                                                      # Atom
    """Just an atom really. Has properties, can bond to other atoms, and can
generate a :class:`System` for simulation."""                                    # Atom
                                                                                 # Atom
    def __init__(self, name:str, atomicN:int, massN:float, valenceE:int, radius:List[float]=[], octetE:int=8): # Atom
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
:param octetE: how many electrons in a full octet? Default 8, but can be 2 for H and He""" # Atom
        self.name = name; self.atomicN = atomicN; self.massN = massN             # Atom
        self.ogValenceE = valenceE # original                                    # Atom
        self.valenceE = valenceE; self.octetE = octetE; self.radius = radius     # Atom
        self._bonds = [] # list of Atoms this Atom is bonded to                  # Atom
        self.gDepth = -1 # graph depth, for graph traversal stuff. Values will be updated from _depthAuto # Atom
        self.idx = f"A{_idxAuto()}" # unique value for Atoms everywhere          # Atom
        # contracts:                                                             # Atom
        # - valenceE = eClouds * 2 + freeE + len(bonds) * 2                      # Atom
        # - valenceE <= octetE. "<" happens when octet not full                  # Atom
        # can only form a new bond if freeE >= 1. Can dec eClouds to inc freeE   # Atom
        if name != "_e":                                                         # Atom
            self.eClouds = []; self.freeE = valenceE % 2                         # Atom
            for i in range(valenceE//2): self.eClouds.append(mo._e)              # Atom
        else: self.eClouds = []; self.freeE = 0                                  # Atom
    @property                                                                    # Atom
    def bonds(self):                                                             # Atom
        """List of Atoms bonded to this Atom"""                                  # Atom
        return self._bonds                                                       # Atom
    @bonds.setter                                                                # Atom
    def bonds(self, v): self._bonds = v                                          # Atom
    @property                                                                    # Atom
    def nonHBonds(self) -> List["Atom"]:                                         # Atom
        """All atoms this atom is bonded to, minus the Hydrogens."""             # Atom
        return [a for a in self.bonds if a.name != "H"]                          # Atom
    @property                                                                    # Atom
    def HBonds(self) -> List["Atom"]:                                            # Atom
        """All hydrogens this atom is bonded to."""                              # Atom
        return [a for a in self.bonds if a.name == "H"]                          # Atom
    @property                                                                    # Atom
    def uniqueBonds(self) -> List["Atom"]:                                       # Atom
        """All unique bonds. Meaning, if there's a double bond, only return 1
atom, not 2."""                                                                  # Atom
        return list(set(self.bonds))                                             # Atom
    @property                                                                    # Atom
    def uniqueNonHBonds(self) -> List["Atom"]:                                   # Atom
        """All unique non Hydrogen bonds."""                                     # Atom
        return list(set(self.nonHBonds))                                         # Atom
    def nBonds(self, atom:"Atom"):                                               # Atom
        """Get number of bonds between this and another atom."""                 # Atom
        return len([bond for bond in self.bonds if bond == atom])                # Atom
    @property                                                                    # Atom
    def availableBonds(self) -> int:                                             # Atom
        """Available bonds. This includes electron clouds, radical electrons, and
Hydrogen bonds."""                                                               # Atom
        return len(self.eClouds) * 2 + self.freeE + len([a for a in self.bonds if a.name == "H"]) # Atom
    def __repr__(self):                                                          # Atom
        return f"""<Atom {self.name} ({self.atomicN}), {len(self.bonds)} bonds, {self.valenceE}/{self.octetE} valence electrons, {len(self.eClouds)} electron clouds, {self.freeE} free (radical) electrons>""" # Atom
@k1lib.patch(Atom)                                                               # Atom
def _show(self, g=None, gDepth=-1, H:bool=True, GVKwargs={}):                    # _show
    self.gDepth = gDepth                                                         # _show
    if not H:                                                                    # _show
        nH = len(self.HBonds); nH = "" if nH==0 else ("H" if nH == 1 else f"H{nH}") # _show
        g.node(self.idx, f"{self.name}{nH}", **GVKwargs)                         # _show
    else: g.node(self.idx, self.name, **GVKwargs)                                # _show
    for atom in self.bonds:                                                      # _show
        if atom.gDepth >= gDepth or (not H and atom.name == "H"): continue       # _show
        # all this complexity just to determine arrow direction                  # _show
        d1 = (self.nonHBonds[0] == atom) if len(self.nonHBonds) > 0 else False   # _show
        d2 = (atom.nonHBonds[0] == self) if len(atom.nonHBonds) > 0 else False   # _show
        if d1 and d2: g(self.idx, atom.idx, dir="both")                          # _show
        elif d1: g(self.idx, atom.idx)                                           # _show
        elif d2: g(atom.idx, self.idx)                                           # _show
        else: g(self.idx, atom.idx, arrowhead="none")                            # _show
    if H: [atom._show(g, gDepth, H) for atom in self.bonds if atom.gDepth < gDepth] # _show
    else: [atom._show(g, gDepth, H) for atom in self.nonHBonds if atom.gDepth < gDepth] # _show
@k1lib.patch(Atom)                                                               # _show
def show(self, H:bool=True):                                                     # show
    """Show the molecule graph this atom is a part of. Meant for debugging
simple substances only, as graphs of big molecules look unwieldy. This also
highlights the current :class:`Atom`, and each bond is an arrow, indicating
where :meth:`next` will go next.

:param H: whether to display hydrogens as separate atoms, or bunched into the main atom""" # show
    g = k1lib.digraph(); self._show(g, _depthAuto(), H, {"style": "filled"}); return g # show
@k1lib.patch(Atom)                                                               # show
def _addFreeE(self, amt:int=1):                                                  # _addFreeE
    """Adds free electron to atom."""                                            # _addFreeE
    if amt > 1: [self._addFreeE() for i in range(amt)]                           # _addFreeE
    self.freeE += 1                                                              # _addFreeE
    if self.freeE >= 2: self.eClouds.append(mo._e); self.freeE -= 2              # _addFreeE
@k1lib.patch(Atom)                                                               # _addFreeE
def _subFreeE(self, amt:int=1) -> bool:                                          # _subFreeE
    """Tries to use ``amt`` free electrons. Returns successful or not."""        # _subFreeE
    if amt > 1: [self._subFreeE() for i in range(amt)]                           # _subFreeE
    elif self.freeE > 0: self.freeE -= 1                                         # _subFreeE
    elif len(self.eClouds) > 0:                                                  # _subFreeE
        self.freeE += 1; self.eClouds.pop()                                      # _subFreeE
    else: raise RuntimeError(f"Can't give away any more free electrons on atom {self.name}!") # _subFreeE
@k1lib.patch(Atom)                                                               # _subFreeE
def _makeRoom(self, nBonds:int):                                                 # _makeRoom
    """Tries to remove bonds with Hydrogen to make room for ``nBonds`` more bonds.""" # _makeRoom
    nBondsToRemove = self.valenceE + nBonds - self.octetE                        # _makeRoom
    if nBondsToRemove > 0:                                                       # _makeRoom
        Hs = [bond for bond in self.bonds if bond.name == "H"]                   # _makeRoom
        if len(Hs) >= nBondsToRemove:                                            # _makeRoom
            for i in range(nBondsToRemove): self.removeBond(Hs[i])               # _makeRoom
        elif not settings.overOctet:                                             # _makeRoom
            ans = input(f"Can't remove Hydrogen bonds to make room for new bond! Do you want to do anyway (y/n): ") # _makeRoom
            print("Btw, you can auto accept this by doing `settings.mo.overOctet = True`") # _makeRoom
            if ans.lower()[0] != "y": raise OctetFull("Stopping...")             # _makeRoom
    availableE = len(self.eClouds) * 2 + self.freeE                              # _makeRoom
    if availableE < nBonds: raise NoFreeElectrons(f"Can't make room for {nBonds} new bonds on {self.name}. Only {availableE} electrons left for bonds!") # _makeRoom
@k1lib.patch(Atom)                                                               # _makeRoom
def __call__(self, atom:Atom, nBonds:int=1, main=False) -> Atom:                 # __call__
    """Forms a bond with another atom. If valence electrons are full, will
attempt to disconnect Hydrogens from self to make room.

:param bond: number of bonds. 2 for double, 3 for triple
:param main: whether to put this bond in front of existing bonds, to
    signify the "main" chain, so that it works well with :meth:`next`
:return: self"""                                                                 # __call__
    self._makeRoom(nBonds); atom._makeRoom(nBonds)                               # __call__
    if main: self.bonds = [atom] * nBonds + self.bonds                           # __call__
    else: self.bonds += [atom] * nBonds                                          # __call__
    atom.bonds += [self] * nBonds                                                # __call__
    self.valenceE += nBonds; self._subFreeE(nBonds)                              # __call__
    atom.valenceE += nBonds; atom._subFreeE(nBonds)                              # __call__
    return self                                                                  # __call__
@k1lib.patch(Atom)                                                               # __call__
def bond(self, atom:Atom, nBonds:int=1, main=False) -> Atom:                     # bond
    """Like :meth:`__call__`, but returns the atom passed in instead, so you
can form the main loop quickly."""                                               # bond
    self(atom, nBonds, main); return atom                                        # bond
@k1lib.patch(Atom)                                                               # bond
def main(self, atom:Atom, nBonds:int=1) -> Atom:                                 # main
    """Like :meth:`bond`, but with ``main`` param defaulted to True."""          # main
    return self.bond(atom, nBonds, True)                                         # main
@k1lib.patch(Atom)                                                               # main
def removeBond(self, atom:"Atom"):                                               # removeBond
    """Removes all bonds between this and another atom"""                        # removeBond
    nBonds = self.nBonds(atom)                                                   # removeBond
    self.bonds = [bond for bond in self.bonds if bond != atom]                   # removeBond
    self.valenceE -= nBonds; self._addFreeE(nBonds)                              # removeBond
    atom.bonds = [bond for bond in atom.bonds if bond != self]                   # removeBond
    atom.valenceE -= nBonds; atom._addFreeE(nBonds)                              # removeBond
@k1lib.patch(Atom, "next")                                                       # removeBond
def _next(self, offset=0, times:int=1) -> "Atom":                                # _next
    """Returns the next atom bonded to this. Tries to avoid going into Hydrogens.
This is the main way to navigate around the molecule.

You kinda have to make sure that your molecule's bonding order is appropriate by
choosing between :meth:`bond` and :meth:`main`. Check the bonding order with
:meth:`show`.

:param offset: if there are multiple non-Hydrogen atoms, which ones should I pick?
:param times: how many times do you want to chain ``.next()``?"""                # _next
    if times < 0: raise RuntimeError("Can't do .next() with negative `times`")   # _next
    if times == 0: return self                                                   # _next
    atoms = self.nonHBonds + self.HBonds                                         # _next
    if len(atoms) == 0: return None                                              # _next
    _next = atoms[offset]                                                        # _next
    if times == 1: return _next                                                  # _next
    else: return _next.next(offset, times-1)                                     # _next
@k1lib.patch(Atom)                                                               # _next
def nexts(self, atoms:int=2) -> List[Atom]:                                      # nexts
    """Kinda like :meth:`next`, but fetches multiple atoms on the backbone.
Example::

    c1, c2 = mo.CH4(mo.CH4).nexts()"""                                           # nexts
    if atoms < 1: raise RuntimeError(f"Zero or negative ({atoms}) number of atoms does not make sense!") # nexts
    if atoms == 1: return [self]                                                 # nexts
    return [self, *(self.next().nexts(atoms-1))]                                 # nexts
empiricalOrder = ["C", "H", "O", "N"]                                            # nexts
def em1(e:str, n:int):                                                           # em1
    if n == 1: return e                                                          # em1
    else: return f"{e}{n}"                                                       # em1
@k1lib.patch(Atom)                                                               # em1
def _empirical(self, d:Dict[str, int], gDepth:int):                              # _empirical
    if self.gDepth >= gDepth: return                                             # _empirical
    self.gDepth = gDepth; d[self.name] += 1                                      # _empirical
    for atom in self.bonds: atom._empirical(d, gDepth)                           # _empirical
@k1lib.patch(Atom)                                                               # _empirical
def empirical(self) -> str:                                                      # empirical
    """Returns an empirical formula for the molecule this :class:`Atom` is attached to.""" # empirical
    d = k1lib.Object().withAutoDeclare(lambda: 0)                                # empirical
    self._empirical(d, _depthAuto()); answer = ""                                # empirical
    for e in empiricalOrder:                                                     # empirical
        if e in d: answer += em1(e,d[e]); del d[e]                               # empirical
    for e in d.state.keys(): answer += em1(e,d[e])                               # empirical
    return answer                                                                # empirical
@k1lib.patch(Atom)                                                               # empirical
def _atoms(self, l, gDepth):                                                     # _atoms
    if self.gDepth >= gDepth: return                                             # _atoms
    self.gDepth = gDepth; l.append(self)                                         # _atoms
    for atom in self.bonds: atom._atoms(l, gDepth)                               # _atoms
@k1lib.patch(Atom)                                                               # _atoms
def atoms(self) -> List[Atom]:                                                   # atoms
    """Returns a list of Atoms in the molecule this specific Atom is attached to.""" # atoms
    l = []; self._atoms(l, _depthAuto()); return l                               # atoms
@k1lib.patch(Atom, "endChain")                                                   # atoms
@property                                                                        # atoms
def endChain(a) -> Atom:                                                         # endChain
    """Do a bunch of .next() until reached the end of the carbon chain.
Example::

    c1 = mo.alcohol(3, 1)
    c3 = c1.endChain
    c3(mo.NH3)
    c1.show() # displays in cell"""                                              # endChain
    lastA = None                                                                 # endChain
    for i in range(200): # for loop to prevent infinite recursion                # endChain
        nextA = a.next()                                                         # endChain
        if nextA == lastA: return a                                              # endChain
        lastA = a; a = nextA                                                     # endChain
@k1lib.patch(Atom)                                                               # endChain
def moveLastCTo2ndC(a:Atom) -> Atom:                                             # moveLastCTo2ndC
    """Move last carbon to 2nd carbon. Useful in constructing iso- and tert-.""" # moveLastCTo2ndC
    end = a.endChain; nearEnd = end.next()                                       # moveLastCTo2ndC
    end.removeBond(nearEnd); nearEnd(mo.H); a.next()(mo.CH4); return a           # moveLastCTo2ndC
_a = {} # dict of atoms, which will be used to patch the entire module           # moveLastCTo2ndC
class _Mo:                                                                       # _Mo
    def __init__(self): self._MoWrap_dirs = []                                   # _Mo
    def registerSubstance(self, name:str, _f):                                   # _Mo
        setattr(_Mo, name, property(lambda self: _f()))                          # _Mo
        self._MoWrap_dirs.append(name)                                           # _Mo
    def __dir__(self):                                                           # _Mo
        return super().__dir__() + self._MoWrap_dirs                             # _Mo
    pass                                                                         # _Mo
mo = _Mo() # internal convenience object so that I can use the same style as the module # _Mo
def _atom(name, *args, **kwargs):                                                # _atom
    _a[name] = f = lambda: Atom(name, *args, **kwargs)                           # _atom
    mo.registerSubstance(name, f)                                                # _atom
def substances() -> List[str]:                                                   # substances
    """Get a list of builtin substances. To register new substances, check over
:class:`Atom`."""                                                                # substances
    return [k for k in _a.keys() if not k.startswith("_")]                       # substances
# covalent radius taken from (Pyykko & Atsumi) https://chem.libretexts.org/@api/deki/pages/2182/pdf/A3%253A%2bCovalent%2bRadii.pdf?stylesheet=default # substances
_atom("_e", 0,   0.1,    0, [25]) # electron cloud, for internal use             # substances
_atom("H",  1,   1.008,  1, [32], octetE=2)                                      # substances
_atom("Li", 3,   6.94,   1, [133, 124])                                          # substances
_atom("Be", 4,   9.0122, 2, [102, 90, 85])                                       # substances
_atom("B",  5,  10.81,   3, [85,  78, 73])                                       # substances
_atom("C",  6,  12.011,  4, [75,  67, 60])                                       # substances
_atom("N",  7,  14.007,  5, [71,  60, 54])                                       # substances
_atom("O",  8,  15.999,  6, [63,  57, 53])                                       # substances
_atom("F",  9,  18.998,  7, [64,  59, 53])                                       # substances
_atom("Na", 11, 22.990, 1, [155, 160])                                           # substances
_atom("Mg", 12, 24.305, 2, [139, 132, 127])                                      # substances
_atom("Al", 13, 26.982, 3, [126, 113, 111])                                      # substances
_atom("Si", 14, 28.085, 4, [116, 107, 102])                                      # substances
_atom("P",  15, 30.974, 5, [111, 102, 94])                                       # substances
_atom("S",  16, 32.06,  6, [103, 94,  95])                                       # substances
_atom("Cl", 17, 35.45,  7, [99,  95,  93])                                       # substances
_atom("K",  19,  39.098, 1, [196, 193])                                          # substances
_atom("Ca", 20,  40.078, 2, [171, 147, 133])                                     # substances
_atom("Ga", 31,  69.723, 3, [124, 117, 121])                                     # substances
_atom("Ge", 32,  72.630, 4, [121, 111, 114])                                     # substances
_atom("As", 33,  74.922, 5, [121, 114, 106])                                     # substances
_atom("Se", 34,  78.971, 6, [116, 107, 107])                                     # substances
_atom("Br", 35,  79.904, 7, [114, 109, 110])                                     # substances
_atom("I",  53, 126.9,   7, [133, 129, 125])                                     # substances
