# AUTOGENERATED FILE! PLEASE DON'T EDIT
import re as _re, difflib as _difflib
from typing import Dict as _Dict, Union as _Union, List as _List,\
Optional as _Optional
from collections import OrderedDict as _OrderedDict
settings = {
    "spaceBetweenValueSymbol": True,
    "eqnPrintExtras": True
}
class Eqn:
    def __init__(self, system:"System"):
        """Creates a blank equation. Not expected to be instantiated by
the end user."""
        self.system = system
        self.terms:_Dict[str, float] = {}
    def _removeZeros(self):
        self.terms = {k: v for k, v in self.terms.items() if abs(v) > 1e-6}; return self
    def parse(self, line:str):
        line = line.strip().replace(" +", "+").replace("+ ", "+").replace(" ->", "->").replace("-> ", "->")
        reactants, products = line.split("->")
        for i, side in enumerate(line.split("->")):
            sign = i * 2 - 1
            for e in side.split("+"): # side is reactants or products
                e = e.strip()
                number = _re.findall("^[0-9.\/]*", e)[0]
                term, number = (e, 1) if number == "" else (e[e.find(number) + len(number):], eval(str(number)))
                term = term.strip(); self.system.terms.add(term)
                if term not in self: self[term] = 0
                self[term] += sign * number
        return self._removeZeros()
    def save(self):
        """Saves this (potentially new) equation to the system, so that it
can be used directly later on"""
        self.system.parse(str(self)); return self
    def __contains__(self, x:str):
        """Whether a term is in this equation"""
        return x in self.terms
    def __getattr__(self, term:str):
        """Gets the value of the term in this equation. Negative if on
consumer side, positive if on producer side"""
        if term in self.terms: return self.terms[term]
        else: return 0
    def __setitem__(self, idx:str, value:float): self.terms[idx] = value; return self
    def __getitem__(self, idx:str):
        """Same as :meth:`__getattr__`"""
        return getattr(self, idx)
    def __iter__(self):
        for k, v in self.terms.items(): yield k, v
    def __len__(self):
        """Returns number of terms in this equation"""
        return len(self.terms)
    def __hash__(self): return hash(tuple(self.terms.keys()))
    def __str__(self):
        a = " + ".join((f"{-v}{k}" for k, v in self.terms.items() if v < 0))
        b = " + ".join((f"{v}{k}" for k, v in self.terms.items() if v > 0))
        return f"{a} -> {b}"
    def copy(self):
        answer = Eqn(self.system)
        answer.terms = dict(self.terms); return answer
    def __repr__(self, printExtras=None):
        space = " " if settings["spaceBetweenValueSymbol"] else ""
        def formatValue(value:float):
            if abs(value - 1) < 1e-9: return ""
            if abs(value - round(value)) < 1e-9:
                return f"{round(value)}{space}"
            return f"{round(value, 3)}{space}"
        a = " + ".join((f"{formatValue(-v)}{k}" for k, v in self.terms.items() if v < 0))
        b = " + ".join((f"{formatValue(v)}{k}" for k, v in self.terms.items() if v > 0))
        answer = f"{a} \033[1m->\033[0m {b}"
        printExtras = printExtras if printExtras is not None else settings["eqnPrintExtras"]
        return answer if not printExtras else f"""{answer}. Can...
- "MJ" in eqn: to check whether this equation has a specific term
- eqn["MJ"], or eqn.MJ: to get the actual value of the term
- eqn.terms: to get dict of all term -> values
- eqn["MJ"] = 5: to modify a term's value
- eqn * 2: to use normal math operations on the entire equation
- eqn1 @ eqn2: to try to zero out some common terms, useful for unit conversions
- eqn1 == eqn2: see if 2 equations are the same, scale invariant
- for term, value in eqn: to loop over every term and its value
- len(eqn): to get number of terms in the equation
- eqn.copy()"""
    def __mul__(self, number:float):
        answer = self.copy()
        answer.terms = {k: v*number for k, v in self.terms.items()}
        return answer._removeZeros()
    def __rmul__(self, number:float): return self.__mul__(number)
    def __neg__(self): return -1 * self
    def __truediv__(self, number:float):
        answer = self.copy()
        answer.terms = {k: v/number for k, v in self.terms.items()}
        return answer._removeZeros()
    def __rtruediv__(self, number:float): raise Exception("Can't be divided by a number. It doesn't mean anything")
    def __add__(self, eqn):
        answer = self.copy(); answer.terms = {}
        for term, value in self: answer[term] = value + eqn[term]
        for term, value in eqn:
            if term not in answer: answer[term] = value + self[term]
        return answer._removeZeros()
    def __sub__(self, eqn): return self + -1*eqn
    def __eq__(self, eqn):
        if len(self) != len(eqn): return False
        if set(self.terms.keys()) != set(eqn.terms.keys()): return False
        term = list(self.terms.keys())[0]
        eqn = eqn * self[term] / eqn[term]
        for term, value in self:
            if abs(self[term] - eqn[term]) > 1e-9: return False
        return True
    def sharedTerms(self, eqn:"Eqn") -> _List[str]:
        """Gets a list of shared terms between this equation and the
specified one."""
        ts = set(self.terms.keys())
        return [t for t in eqn.terms.keys() if t in ts]
    def join(self, eqn:"Eqn", term:str) -> "Eqn":
        """Tries to cancel out this equation with another equation at the
specified term. Example::

    s = eqn.System(\"\"\"a + b -> c + d
    c + 2e -> f\"\"\")
    s.a.c.join(s.c.f, "c") # returns the equation "a + b + 2e -> d + f"

For simpler cases, where the shared term to be joined is obvious, use
:meth:`__matmul__` instead"""
        return self + eqn * (-self[term]/eqn[term])
    def __matmul__(self, eqn:"Eqn") -> "Eqn":
        """Convenience method that does the same thing as :meth:`join`.
Example::

    s = eqn.System(\"\"\"a + b -> c + d
    c + 2e -> f\"\"\")
    s.a.c @ s.c.f # returns the equation "a + b + 2e -> d + f"

Preference order of which term to join:

1) If term is on producer side of ``self``, and consumer side of ``eqn``
2) If term is on consumer side of ``self``, and producer side of ``eqn``
3) Other cases"""
        sharedTerms = self.sharedTerms(eqn)
        def sortF(term):
            if self[term] > 0 and eqn[term] < 0: return 0
            if self[term] < 0 and eqn[term] > 0: return 1
            return 2
        sharedTerms = sorted(sharedTerms, key=sortF)
        if len(sharedTerms) == 0: return None
        return self.join(eqn, sharedTerms[0])
    def round(self, term:str, amount:float=10) -> "Eqn":
        """Rounds the equation off, so that the term's value
is the specified amount. For aesthetic purposes mainly. Example::

    s = eqn.System("a + b -> 2c")
    s.a.c.round("c", 5) # returns the equation "2.5a + 2.5b -> 5c"'"""
        if term not in self: raise AttributeError(term)
        return self * amount / self[term]
    def __round__(self, term:str=None) -> "Eqn":
        """Like :meth:`round`, but more Pythonic?"""
        if term is None: term = list(self.terms.keys())[-1]
        return self.round(term, 1)
class Eqns:
    def __init__(self, system:"System", eqns:_List[Eqn], focusTerm:str=None):
        """Creates a new list of equations. Not expected to be instantiated
by the end user.

:param system: injected :class:`System`
:param eqns: list of equations
:param focusTerm: if the list of equations are from the result of focusing
    in a single term, then use this parameter to prioritize certain search
    parameters.
"""
        self.system = system; self.eqns = eqns; self.terms = set()
        for eqn in eqns: self.terms.update(eqn.terms.keys())
        self.focusTerm = focusTerm
    def __getitem__(self, idx:_Union[int, str]) -> _Optional[Eqn]:
        """If int, return the equation with that index. Not really helpful
for exploring the system of equations, but good for automated scripts

If string, then effectively the same as :meth:`__getattr__`
"""
        return self.eqns[idx] if isinstance(idx, int) else getattr(self, idx)
    def __getattr__(self, term:str) -> _Optional[Eqn]:
        """Picks out a specific :class:`Eqn` that has the specified term.
Prefer shorter equations, and the returned :class:`Eqn` always have the
term on the products side. Meaning::

    eqns = eqn.System("a + 2b -> c").b # gets an Eqns object with that single equation
    eqns.a # gets the equation "c -> a + 2b" instead

This is a convenience way to search for equations. If you need more
granularity, use :meth:`pick` instead"""
        chosenEqns = []
        for eqn in self.eqns:
            if term in eqn:
                chosenEqns.append(eqn if eqn[term] > 0 else -eqn)
        chosenEqns = sorted(chosenEqns, key=lambda eqn: len(eqn))
        return None if len(chosenEqns) == 0 else chosenEqns[0]
    def pick(self, *terms:_List[str]) -> _Optional[Eqn]:
        """Like the quick method (:meth:`__getattr__`), but here, picks
equations more carefully, with selection for multiple terms. Example::

    s = eqn.System(\"\"\"a + 2b -> c
    b + c -> d
    a -> 3d
    a + b + c -> 2d\"\"\")
    s.a.pick("b", "d") # returns last equation
    
As you can see, it's impossible to pick out the last equation using
:meth:`__getattr__` alone, as they will all prefer the shorter equations,
so this is where :meth:`pick` can be useful."""
        chosenEqns = []; t = self.focusTerm or terms[0]
        for eqn in self.eqns:
            if all((term in eqn for term in terms)):
                chosenEqns.append(eqn if eqn[t] > 0 else -eqn)
        chosenEqns = sorted(chosenEqns, key=lambda eqn: len(eqn))
        return None if len(chosenEqns) == 0 else chosenEqns[0]
    def __dir__(self):
        """Returns the list of terms in every equation here. Useful for
tab completion."""
        return list(self.terms)
    def __repr__(self):
        end = """Can...
- eqns[i]: to get the 'i'th equation
- eqns.C: to pick out the first equation that has term 'C'"""
        if self.focusTerm == None:
            eqns = "\n".join([f"{i}. {eqn.__repr__(printExtras=False)}" for i, eqn in enumerate(self.eqns)])
            return f"""Equations:\n{eqns}\n\n{end}"""
        else:
            consumingEqns = []; producingEqns = []
            for eqn in self.eqns:
                if eqn[self.focusTerm] < 0:
                    consumingEqns.append(f"{eqn.__repr__(printExtras=False)}")
                else: producingEqns.append(f"{eqn.__repr__(printExtras=False)}")
            consumingEqns = "\n".join([f"{i}. {eqn}" for i, eqn in enumerate(consumingEqns)])
            producingEqns = "\n".join([f"{i}. {eqn}" for i, eqn in enumerate(producingEqns)])
            return f"""Consumers:\n{consumingEqns}\n\nProducers:\n{producingEqns}\n\n{end}"""
class System:
    def __init__(self, strToParse:str=None):
        """Creates a new system of equations.
        
:param strToParse: if specified, then it gets feed into :meth:`parse`"""
        self.terms = set()
        self.eqns = []
        if strToParse is not None: self.parse(strToParse)
    def parse(self, lines:str) -> "System":
        """Parses extra equations and saves them to this :class:`System`"""
        lines = (line for line in lines.split("\n") if line != "" and not line.startswith("#"))
        self.eqns += [Eqn(self).parse(line) for line in lines if not line.startswith("#")]
        self.eqns = list(set(self.eqns))
        return self
    def spellCheck(self):
        """Runs a spell check to find out terms that are pretty similar to
each other"""
        print("Similar terms:"); terms = list(self.terms)
        for i, iTerm in enumerate(terms):
            for j, jTerm in enumerate(terms[i+1:]):
                if iTerm[:-1] == jTerm[:-1]: continue
                if abs(len(iTerm) - len(jTerm)) > 2: continue
                r = _difflib.SequenceMatcher(None, iTerm, jTerm).ratio()
                if r < 0.9: continue
                print(f"- {round(r*100)}% similar: {iTerm}, {jTerm}")
    def __len__(self): return len(self.eqns)
    def __getitem__(self, idx:int) -> Eqn:
        """Picks out the i'th equation from the list of equations. Useful
for automated scripts"""
        return self.eqns[idx]
    def __getattr__(self, term:str) -> Eqns:
        """Picks out equations that has the term"""
        return Eqns(self, [eqn for i, eqn in enumerate(self.eqns) if term in eqn], focusTerm=term)
    def __dir__(self):
        """Returns the list of terms in every equation here. Useful for
tab completion."""
        return list(self.terms)
    def __repr__(self):
        return f"""System of {len(self)} equations:\n{Eqns(self, self.eqns)}\n
Can...
- s[i]: to get a specific equation
- s.C: to get all equations that involve a specific substance "C"
- s.spellCheck(): to check if there are terms that are close to each other
"""