# AUTOGENERATED FILE! PLEASE DON'T EDIT
__all__ = ["grep", "grepToTable", "grepTemplate"]
import re
from k1lib.cli.init import BaseCli, Table, Row
import k1lib.cli as cli
from collections import deque
from typing import Iterator
class grep(BaseCli):
    def __init__(self, pattern:str, before:int=0, after:int=0):
        """Find lines that has the specified pattern. Example::

    # returns ['c', 'd', '2', 'd']
    "abcde12d34" | grep("d", 1) | deref()
    # returns ['d', 'e', 'd', '3', '4']
    "abcde12d34" | grep("d", 0, 3).till("e") | deref()

:param pattern: regex pattern to search for in a line
:param before: lines before the hit. Outputs independent lines
:param after: lines after the hit. Outputs independent lines"""
        super().__init__()
        self.pattern = re.compile(pattern)
        self.before = before; self.after = after
        self.tillPattern = None
    def till(self, pattern:str):
        """Greps until some other pattern appear. Before lines will be honored,
but after lines will be set to inf. Inclusive."""
        self.tillPattern = re.compile(pattern); self.after = 1e9; return self
    def __ror__(self, it:Iterator[str]) -> Iterator[str]:
        super().__ror__(it); self.sectionIdx = 0
        queue = deque(); counter = 0 # remaining lines after to display
        for line in it:
            queue.append(line) # saves recent past lines
            if len(queue) > self.before + 1: queue.popleft()
            a = self.pattern.search(line) is not None # new hit!
            b = counter > 0 # still got sth to print out
            c = False if self.tillPattern is None else self.tillPattern.search(line) # new hit of "till"
            if a or b: # if detected, or still printing the "after" section
                if a:
                    self.sectionIdx += 1 # notifies to other utils that a new section has been created
                    counter = self.after + 1 # resets "after" section
                elif c:
                    self.sectionIdx += 1; counter = 0
                # prints current line and everything before
                yield from queue; queue.clear(); counter -= 1
class grepToTable(BaseCli):
    def __init__(self, pattern:str, before:int=0, after:int=0):
        """Searches for a pattern. If found, then put all the before and after
lines in different columns. Example::

    # returns [['2', 'b'], ['5', 'b']]
    "1a\\n 2b\\n 3c\\n 4d\\n 5b\\n 6c\\n f" | grepToTable("b", 1) | deref()"""
        super().__init__()
        self.pattern = pattern; self.before = before; self.after = after
    def __ror__(self, it:Iterator[str]) -> Table[str]:
        super().__ror__(it)
        gr = grep(self.pattern, self.before, self.after)
        elems = []; idx = 0
        for line in (it | gr):
            if gr.sectionIdx > idx: # outputs whatever remaining
                idx = gr.sectionIdx;
                if len(elems) > 0: yield Row(elems)
                elems = []
            elems.append(line)
        yield Row(elems)
class grepTemplate(BaseCli):
    def __init__(self, pattern:str, template:str):
        """Searches over all lines, pick out the match, and expands
it to the templateand yields"""
        super().__init__()
        self.pattern = re.compile(pattern); self.template = template
    def __ror__(self, it:Iterator[str]):
        super().__ror__(it)
        for line in it:
            matchObj = self.pattern.search(line)
            if matchObj is None: continue
            yield matchObj.expand(self.template)