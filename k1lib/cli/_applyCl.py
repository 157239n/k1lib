# AUTOGENERATED FILE! PLEASE DON'T EDIT HERE. EDIT THE SOURCE NOTEBOOKS INSTEAD
__all__ = ["dummy"]
def dummy():                                                                     # dummy
    """Does nothing. Only here for you to checkout the source code"""            # dummy
    pass                                                                         # dummy
from k1lib.imports import *; import hashlib                                      # dummy
def hashF(msg:str) -> str: m = hashlib.sha256(); m.update(f"{msg}".encode()); return k1.encode(m.digest()) # hashF
def cpuHash() -> str: return None | cmd("lscpu") | head() | join("\n") | aS(hashF) # cpuHash
loadTestFn = "~/.k1lib/applyCl_loadTest.pth"                                     # cpuHash
def load_loadTest(): return cat(loadTestFn, False) | aS(dill.loads) if os.path.exists(os.path.expanduser(loadTestFn)) else dict() # load_loadTest
def good_loadTest(): # whether the underlying architecture has been load-tested before # good_loadTest
    obj = load_loadTest(); return None | applyCl.aS(lambda: cpuHash()) | cut(1) | ~inSet(obj) | shape(0) == 0 # good_loadTest
def loadTestS(nodeId, cpus, hash_):                                              # loadTestS
    with k1.timer() as t1:                                                       # loadTestS
        [nodeId]*cpus*4 | insertIdColumn(begin=False) | applyCl(lambda x: range(300_000_000) | toSum(), pre=True) | deref() # loadTestS
    with k1.timer() as t2:                                                       # loadTestS
        [nodeId]*cpus*4 | insertIdColumn(begin=False) | applyCl(lambda x: range(30_000_000) | apply(op()+2) | toSum(), pre=True) | deref() # loadTestS
    return [nodeId, cpus, hash_, t1(), t2()]                                     # loadTestS
def loadTest():                                                                  # loadTest
    data = None | applyCl.aS(lambda: [os.cpu_count(), cpuHash()] | deref()) | ~apply(lambda x,y: [x,*y]) | deref() # loadTest
    a = data | ~applyTh(loadTestS, timeout=3600) | deref()                       # loadTest
    alpha1, alpha2 = a | cut(1, 3, 4) | ~apply(lambda x,y,z: [y, z]) | transpose() | toMax().all() | deref() # loadTest
    obj = a | ~apply(lambda idx,cpu,h,t1,t2: [h, (alpha1/(t1), alpha2/(t2)) | toMean()]) | toDict() | deref() # loadTest
    obj | aS(dill.dumps) | file(loadTestFn)                                      # loadTest
def loadTestGuard(guard=True, rounded=True): # returns Dict[nodeId, cpus]        # loadTestGuard
    if guard and not good_loadTest():                                            # loadTestGuard
        ans = input("""applyCl has not load-tested your system yet, so running
the requested operation might be unbalanced on the cluster (some
nodes finish before others, wasting computational time). Would you
like to perform a load test now? Should take 1-2 minutes. Y/n: """)              # loadTestGuard
        if ans.lower()[0] == "y": loadTest()                                     # loadTestGuard
    data = None | applyCl.aS(lambda: [cpuHash(), os.cpu_count()]) | apply(wrapList(), 0) | joinStreams().all() | deref() # List[nodeId, cpu hash, #cpus] # loadTestGuard
    obj = {**data | cut(1, 2) | apply("1", 1) | toDict(), **load_loadTest()}     # loadTestGuard
    return data | lookup(obj, 1) | ~apply(lambda nodeId,mul,cpu: [nodeId, mul*cpu | (aS(round) if rounded else iden())]) | toDict() # loadTestGuard
def balancedNodeIds(): a = loadTestGuard().items(); return a | ~apply(lambda x,y: [x]*y) | joinStreams() | randomize(None) | repeatFrom() | randomize(a | cut(1) | toSum() | op()*2) # balancedNodeIds
from k1lib.imports import *                                                      # balancedNodeIds
getFolderSize = ls() | filt(os.path.isdir).split() | apply(lambda x: x | (tryout(0) | getFolderSize)) + apply(os.path.getsize) | toSum().all() | toSum() | deref() # balancedNodeIds
getFilesInFolder = aS(os.path.expanduser) | aS(os.walk) | cut(0, 2) | ungroup() | join(os.sep).all() # balancedNodeIds
def getIr(base): return None | applyCl.aS(lambda: ls(base) | iden() & apply(lambda x: x | (tryout(0) | (aS(os.path.getsize) if os.path.isfile(x) else getFolderSize))) | transpose() | deref()) | ungroup(False) | insertIdColumn(True) | deref() # getIr
_normF1 = cut(1) | toSum()                                                       # getIr
def normalize(d):                                                                # normalize
    s = 0                                                                        # normalize
    for a,b in d: s+=b                                                           # normalize
    return [[a,b/s] for a,b in d]                                                # normalize
    return d | apply(op()/s, 1) | deref()                                        # normalize
@lru_cache                                                                       # normalize
def statsCpu(nodeIds):                                                           # statsCpu
    cpu = loadTestGuard(False).items() | inSet(nodeIds, 0) | sort(0, False) | deref() # statsCpu
    cpuF = loadTestGuard(False).items() | inSet(nodeIds, 0) | sort(0, False) | deref() | aS(normalize); cpuF # "cpuF" = cpu fraction. List[nodeId, cpu fraction] # statsCpu
    return [cpu, cpuF]                                                           # statsCpu
@lru_cache                                                                       # statsCpu
def statsNodeId(): return applyCl.nodeIds()                                      # statsNodeId
_statsS1 = statsNodeId() | apply(wrapList() | insert(0, False)) | toDict()       # statsNodeId
def stats(inter, nodeIds): # inter for cached data                               # stats
    sizeF = normalize(inter["sizes"].items()) # size fraction. List[nodeId, size fraction] # stats
    return *statsCpu(nodeIds), sizeF                                             # stats
_scoresF = cut(1).all() | transpose() | ~apply(lambda c,s: s-c) | deref()        # stats
def scores(inter, nodeIds): # 0 for best situation, negative means more compute than size, positive means more size than compute # scores
    cpu, cpuF, sizeF = stats(inter, nodeIds)                                     # scores
    return [cpuF, sizeF] | _scoresF # negpos                                     # scores
scoreF = apply(lambda x: abs(x)**2) | toSum()                                    # scores
def getIrp(ir, nodeIds): # "processed ir". Dict[nodeId -> Dict[idx -> Tuple[url, size]]]. This will mutate across optimizations and is intended to be fast # getIrp
    return [nodeIds | apply("[x, {}]"), ir | groupBy(1, True) | apply(~apply(lambda idx,url,size: [idx,[url,size]]) | toDict(), 1)] | joinStreams() | sort(0, False) | toDict() # getIrp
def getSizes(irp): return irp.items() | apply(op().values() | cut(1) | toSum(), 1) | toDict() # Dict[nodeId -> int] for total size of a node # getSizes
def move(ir, nA:str, nB:str, idx:int, inter=None): # mutates ir                  # move
    ir1 = ir; ir1[idx][1] = nB                                                   # move
    if inter is not None:                                                        # move
        irp = inter["irp"]; irp[nB][idx] = elem = irp[nA][idx]; del irp[nA][idx] # move
        sizes = inter["sizes"]; sizes[nB] += elem[1]; sizes[nA] -= elem[1]       # move
    return ir1                                                                   # move
fileSizesF = apply(lambda arr: np.array([e[1] for e in arr[1].values()]))        # move
def optimize(ir, nodeIds, inter=None): # inter for intermediary data, to speed things up. Has "irp", "sizes" # optimize
    hasInter = inter is not None; inter = inter or {}                            # optimize
    irp = inter["irp"] if hasInter else getIrp(ir, nodeIds)                      # optimize
    sizes = inter["sizes"] if hasInter else getSizes(irp)                        # optimize
    cpu, cpuF = statsCpu(nodeIds); inter = {**inter, "irp": irp, "sizes": sizes} # optimize
    scs = inter["scs"] if hasInter else scores(inter, nodeIds)                   # optimize
    a = np.argmax(scs); b = np.argmin(scs)                                       # optimize
    files = list(irp.items()); fA = files[a]; fB = files[b] # files A. Tuple[nodeId, Dict[idx -> Tuple[url, size]]]. Previously Tuple[nodeId, List[idx, url, size]] # optimize
    nA = nodeIds[a]; nB = nodeIds[b] # A node id, str                            # optimize
    sA, sB = [fA, fB] | fileSizesF # file sizes in A, List[int]                  # optimize
    # print(f"sA: {sA} {sB}")                                                    # optimize
    spA = sA.sum() - sA; spB = sB.sum() + sA # sum prime A, array[files]         # optimize
    sp = spA + spB; sfA = spA/sp; sfB = spB/sp                                   # optimize
    cA = cpu[a][1]; cB = cpu[b][1] # cpu A                                       # optimize
    c = cA + cB; cfA = cA/c; cfB = cB/c # cpu fraction A                         # optimize
    # print(f"sfA: {sfA}, cfA: {cfA}")                                           # optimize
    exp = 5 # intuition says that exp should be even. But that doesn't work. Odd values work tho, but I have no idea why # optimize
    i = ((sfA-cfA)**exp + (sfB-cfB)**exp).argmin()                               # optimize
    idx = fA[1].keys() | rItem(i)                                                # optimize
    ir2 = move(ir, nA, nB, idx, inter)                                           # optimize
    scs = scores(inter, nodeIds); inter["scs"] = scs                             # optimize
    return ir2, [nA, nB, idx, scs | scoreF], inter                               # optimize
def traj(ir, maxSteps=20, nodeIds=None):                                         # traj
    nodeIds = nodeIds | sort(None, False) | deref() | aS(tuple); irp = getIrp(ir, nodeIds); sizes = getSizes(irp) # traj
    sc = scores({"irp": irp, "sizes": sizes}, nodeIds) | scoreF; aux = None; inter = None; auxs = []; irs = [] # traj
    maxSteps = maxSteps if maxSteps is not None else int(1e10)                   # traj
    for i in range(maxSteps):                                                    # traj
        print(f"\rVirtually moving files and folders around. Step {i} of total max steps ({maxSteps})...", end="") # traj
        ir, aux, inter = optimize(ir, nodeIds, inter)                            # traj
        if aux[3] > sc: break                                                    # traj
        irs.append(ir); auxs.append(aux); sc = aux[3]                            # traj
    print(); return irs, auxs                                                    # traj
def collapse(it):                                                                # collapse
    a, b = it | rows(0, -1); c = [a[0], b[1], a[2], b[3]]                        # collapse
    return [] if c[0] == c[1] else [c]                                           # collapse
def traj2(ir, traj): # just looks up the file names really, no processing involved # traj2
    idx2FileName = ir | apply(lambda arr: [arr[0], arr[2]]) | toDict()           # traj2
    a = traj | groupBy(2) | filt(lambda x: len(x) > 1).split() | (apply(collapse)) + iden() | joinStreams(2) | deref() # traj2
    return a | lookup(idx2FileName, 2) | deref()                                 # traj2
# def moveFile(fileName:str, sourceNodeId:str, destNodeId:str, timeout=60): # old, slow, corrupted version # traj2
#     """Moves file from the current node to the destination node. Usually executed on other nodes than the driver node""" # traj2
#     fn = os.path.expanduser(fileName); dirname = os.path.dirname(fn)           # traj2
#     applyCl.cmd(f"mkdir -p {dirname}", nodeIds=[destNodeId]); applyCl.cmd(f"rm -f {fn}", nodeIds=[destNodeId]) # traj2
#     for chunk in cat(fn, False, True): [destNodeId] | applyCl.aS(lambda: chunk >> file(fn), timeout=timeout) | deref() # traj2
#     None | cmd(f"rm {fn}") | deref(); return "ok1"                             # traj2
def moveFile(fn:str, sourceN:str, destN:str, timeout=None): # runs on dest node  # moveFile
    fn = os.path.expanduser(fn); dirname = os.path.dirname(fn)                   # moveFile
    applyCl.cmd(f"mkdir -p {dirname}; rm -f {fn}", nodeIds=[destN]);             # moveFile
    windows = [sourceN] | applyCl.aS(lambda: range(os.path.getsize(fn)) | batched(settings.cli.cat.chunkSize, True) | apply("[x.start, x.stop]") | deref(), num_cpus=0.2, timeout=timeout) | cut(1) | item() | deref() # moveFile
    for chunk in [[sourceN]*len(windows), windows] | transpose() | ~applyCl(lambda sB,eB: cat(fn, False, sB=sB, eB=eB), pre=True, prefetch=20, num_cpus=0.2, timeout=timeout) | cut(1): chunk >> file(fn) # moveFile
    applyCl.cmd(f"rm {fn}", nodeIds=[sourceN])                                   # moveFile
def moveFF(ff:str, sourceN:str, destN:str, timeout=None): # runs on dest node    # moveFF
    """Moves file or folder from the current node to the destination node"""     # moveFF
    ff = os.path.expanduser(ff); isfile = [sourceN] | applyCl.aS(lambda: os.path.isfile(ff)) | cut(1) | item() # moveFF
    if isfile: return moveFile(ff, sourceN, destN, timeout)                      # moveFF
    [sourceN] | applyCl.aS(lambda: ff | getFilesInFolder | deref(), timeout=timeout) | cut(1) | item() | apply(aS(moveFile, sourceN, destN, timeout)) | deref() # moveFF
    applyCl.cmd(f"rm -rf {ff}", nodeIds=[sourceN])                               # moveFF
def moveAll(tr, bs=5, timeout=None):                                             # moveAll
    groups = tr | groupBy(1) | deref() # grouping by destination                 # moveAll
    with ray.progress(len(groups), "Moving files around") as rp:                 # moveAll
        def process(idx, arrs): # processing requests for dest node              # moveAll
            arrss = arrs | batched(3, True) | deref()                            # moveAll
            for i, arrs in enumerate(arrss): # moveFF(fn, a, b)                  # moveAll
                arrs | apply(lambda arr: [arr[1], arr]) | ~applyCl(lambda a,b,fn,sc: moveFF(fn, a, b, timeout), pre=True, timeout=timeout) | deref() # move 3 files on dest node # moveAll
                rp.update.remote(idx, (i+1)/len(arrss))                          # moveAll
        groups | insertIdColumn() | ~applyTh(process, timeout=1e9) | deref()     # moveAll
    # tr | apply(lambda arr: [arr[0], arr]) | ~applyCl(lambda a,b,fn,sc: moveFF(fn, b), pre=True, timeout=timeout) | deref() # old version without progress bar # moveAll
def balanceFolder(base, audit=False, maxSteps=1000, timeout=None, bs=5): # currently executing each move step serially, will change in the future if it's too slow # balanceFolder
    loadTestGuard(); applyCl.cmd(f"mkdir -p {base}"); ir = getIr(base)           # balanceFolder
    tr = traj2(ir, traj(ir, maxSteps, tuple(applyCl.nodeIds()))[1]); return tr if audit else moveAll(tr, bs, timeout) # balanceFolder
def decommissionFolderTraj(base:str, nAs:List[str]): # nAs are the ones to decommission # decommissionFolderTraj
    ir = getIr(base); targetNodes = applyCl.nodeIds() | ~inSet(nAs) | repeatFrom(); irs = []; auxs = [] # decommissionFolderTraj
    seis = ir | inSet(nAs, 1) | cut(0, 1) | ~apply(lambda idx, startNode: [startNode, next(targetNodes), idx, 0]) | deref() # List[start, end, index, score] # decommissionFolderTraj
    for sei in seis: ir = move(ir, *sei[:3]); irs.append(ir); auxs.append(sei)   # decommissionFolderTraj
    return irs, auxs                                                             # decommissionFolderTraj
def decommissionFolder(base:str, nAs:List[str], audit=False, maxSteps=1000, timeout=None, bs=5): # decommissionFolder
    loadTestGuard(); irs, auxs = decommissionFolderTraj(base, nAs)               # decommissionFolder
    nBs=applyCl.nodeIds() | ~inSet(nAs) | aS(tuple)                              # decommissionFolder
    if len(nBs) > 1:                                                             # decommissionFolder
        irs2, auxs2 = traj(irs[-1] if len(irs) > 0 else getIr(base), maxSteps, nBs) # decommissionFolder
        irs = [*irs, *irs2]; auxs = [*auxs, *auxs2]                              # decommissionFolder
    if len(irs) == 0: return                                                     # decommissionFolder
    tr = traj2(irs[-1], auxs)                                                    # decommissionFolder
    if audit: return tr                                                          # decommissionFolder
    moveAll(tr, bs, timeout); nAs | applyCl.aS(lambda: None | cmd(f"rm -rf {base}") | deref()) | deref() # move all files and then deletes the empty folders # decommissionFolder
def a_transfer(fn, nse, nodeB, rpF:callable=iden()):                             # a_transfer
    """Transfers a lot of blocks from a bunch of nodes to nodeB. Does not delete from those node though

nse = List[nodeAId, [sB, eB]]

Runs on driver process, blocks, so better use applyTh outside of this

:param rpF: ray progress function"""                                             # a_transfer
    blockSize = settings.cli.cat.chunkSize                                       # a_transfer
    def inner():                                                                 # a_transfer
        totalBytes = nse | cut(1) | ~apply(lambda x,y:y-x) | toSum(); currentByte = 0 # a_transfer
        for chunk in nse | ~apply(lambda x, y: range(x, y) | batched(blockSize, True) | apply("[x.start, x.stop]"), 1) | ungroup() | deref()\
            | ~applyCl(lambda sB, eB: cat(fn, False, sB=sB, eB=eB), pre=True, timeout=None, prefetch=20) | cut(1): # a_transfer
            chunk >> file(fn); currentByte += len(chunk); rpF(currentByte/totalBytes) # a_transfer
    [nodeB] | applyCl.aS(inner, timeout=None) | item()                           # a_transfer
def decommission(fn:str, nodeAs:List[str], nodeBs:List[str], rS):                # decommission
    """Spreads out a particular file in nodeAs to all nodeBs, to prepare
to decomission nodeAs. The 2 sets should be mutually exclusive

:param rS: instance of refineSeek"""                                             # decommission
    nodeAs, nodeBs = [nodeAs, nodeBs] | deref()                                  # decommission
    if len(nodeAs) == 0: return                                                  # decommission
    if len(nodeBs) == 0: raise Exception("Unsupported configuration! Trying to move data from A+B to C+D. Has to have some shared nodes, like moving data from A+B+C to B+C+D. This is not a fundamental limitation, but just can't be done with the current architecture. Might be fixed in the future.") # decommission
    # some initial metadata                                                      # decommission
    nodeIds = applyCl.nodeIds(); nodeId_cpu = loadTestGuard(False).items() | deref(); nodeId2Cpu = nodeId_cpu | toDict() # decommission
    ws = nodeId_cpu | inSet(nodeBs, 0) | cut(1) | deref() # weights to split files on nodeAs into # decommission
    # splitting file on nodeAs into chunks first, to plan things out             # decommission
    a = nodeAs | applyCl.aS(lambda: fn | splitSeek(ws=ws) | rS | window(2) | deref() | insertColumn(nodeBs) | insert(applyCl.nodeId()).all() | deref()) | cut(1) | joinStreams() | deref() # decommission
    # actually transferring chunks                                               # decommission
    with ray.progress(a | groupBy(1) | shape(0), "Decommissioning") as rp:       # decommission
        c = b = a | groupBy(1, True) | apply(iden() + apply(lambda arr: [arr[0], arr[1:]]) | reverse() | insert(fn)) | deref() # decommission
        enumerate(c) | applyTh(~aS(lambda idx, e: a_transfer(*e, rpF=aS(lambda p: ray.get(rp.update.remote(idx, p))))), timeout=1e9) | deref() # decommission
    # deleting files from nodeAs                                                 # decommission
    nodeAs | applyCl.aS(lambda: None | cmd(f"rm -rf {fn}") | ignore()) | deref() # decommission
ranges2Seeks = apply("[x.start, x.stop]") | joinStreams() | aS(set) | sort(None) | deref() # decommission
def spreadOut(fn:str, nAs:List[str], nBs:List[str], rS):                         # spreadOut
    """Spreads out a file from nodes A to B, where B fully contains A (no decomissioning).
A and B should be mutually exclusive. Initial nodes are A, final nodes are A + B""" # spreadOut
    nAs, nBs = [nAs, nBs] | deref(); rS.fn = fn                                  # spreadOut
    if len(nBs) == 0: return # no need to spread out                             # spreadOut
    nBs | applyCl.aS(lambda: None | cmd(f"mkdir -p {os.path.dirname(fn)}") | deref(), timeout=None) | deref() # spreadOut
    nBs | applyCl.aS(lambda: None | cmd(f"rm -rf {fn}") | deref(), timeout=None) | deref() # spreadOut
    # some initial metadata                                                      # spreadOut
    nodeIds = applyCl.nodeIds(); nodeId_cpu = loadTestGuard(False).items() | deref(); nodeId2Cpu = nodeId_cpu | toDict() # spreadOut
    sizes = nAs | applyCl.aS(lambda: os.path.getsize(fn) if os.path.exists(fn) else 0) | deref(); totalSize = sizes | cut(1) | toSum() # spreadOut
    ns = [*nAs, *nBs]; totalCpu = ns | lookup(nodeId2Cpu) | toSum(); bytePerCpu = totalSize/totalCpu; wsB = nBs | lookup(nodeId2Cpu) | deref() # spreadOut
    # prepares segments and metadata, List[nodeId, [sB, eB]], where sB and eB are the ranges of nAs that they're willing to share # spreadOut
    sizePost = sizes | ~apply(lambda idx, size: [idx, nodeId2Cpu[idx]/totalCpu*totalSize/size]) | deref() # size fraction to retain # spreadOut
    invalidNodes = sizePost | ~filt(lambda x: 0 <= x <= 1, 1) | cut(0) | deref() # spreadOut
    if len(invalidNodes) > 0: raise Exception(f"Unsupported configuration! These nodes have too little data to share: {invalidNodes}. This couldn't have happen using applyCl alone. Data is not corrupted, but you'll have to combine data from all files into 1 and spread them back out again.") # spreadOut
    inter = sizePost | ~apply(lambda idx, x: [idx, [x, 1-x]]) | applyCl(lambda ws: fn | splitSeek(ws=ws) | rS | ~head(1), pre=True, timeout=None) | deref() | filt(~aS(lambda x,y: y-x>0), 1) | deref() # filter at the end to eliminate files that don't want to share anything (x == y) # spreadOut
    # actually transferring data to new nodes                                    # spreadOut
    meta = inter | apply(~aS(range) | splitW(*wsB) | ranges2Seeks | apply(lambda x: splitSeek.backward(fn, x)) | deref() | rS | window(2) | deref() | apply(wrapList()) | insertColumn(nBs), 1) | ungroup(False) | groupBy(1, True) | deref() # spreadOut
    with ray.progress(len(meta), "Transferring data to new nodes") as rp:        # spreadOut
        meta | insertIdColumn(True) | applyTh(~aS(lambda idx, nB, nse: a_transfer(fn, nse, nB, rpF=aS(lambda p: ray.get(rp.update.remote(idx, p))))), timeout=24*3600) | deref() # spreadOut
    # truncates the files in nAs nodes                                           # spreadOut
    inter | ~apply(lambda idx,se: [idx,se[0]]) | applyCl(lambda sB: open(fn, 'a').truncate(sB), pre=True, timeout=None) | deref() # spreadOut
def balanceFile(fn:str, nAs:List[str]=None, nBs:List[str]=None, rS=None):        # balanceFile
    fn = os.path.expanduser(fn); rS = rS or refineSeek(); rS.injectFn(fn); loadTestGuard() # balanceFile
    if nAs is None: nAs = None | applyCl.aS(lambda: os.path.exists(fn)) | filt(op(), 1) | cut(0) | deref() # balanceFile
    if nBs is None: nBs = applyCl.nodeIds()                                      # balanceFile
    decommission(fn, *nAs | inSet(nBs).split() | reverse(), rS)                  # balanceFile
    spreadOut(fn, *nBs | inSet(nAs).split(), rS)                                 # balanceFile
def diskScan1(base:str) -> List[str]: # like ls(), but returns files and folders that appear at least on 2 nodes. No recursion # diskScan1
    isdir, base = base.split("\ue000")                                           # diskScan1
    if not isdir: return []                                                      # diskScan1
    return None | applyCl.aS(lambda: base | (tryout([]) | ls() | apply(os.path.isdir) & iden() | transpose() | ~apply(lambda x,y: f"{x*1}\ue000{y}")) | deref(), timeout=60) | cut(1) | joinStreams() | count() | filt(op()>1, 0) | cut(1) | deref() # diskScan1
def diskScan2(base:str) -> Tuple[List[str], List[str]]: # returns list of distributed folders and list of distributed files # diskScan2
    dFolders = []; folders, files = diskScan1(base) | op().split("\ue000").all() | toInt(0) | filt(op(), 0).split() | (join("\ue000")).all(2) | deref() # first explore this directory # diskScan2
    # print("2--", folders, files, base)                                         # diskScan2
    for folder in folders: # then recursively explore inside directories         # diskScan2
        fol, fil = diskScan2(folder); dFolders.extend(fol); files.extend(fil)    # diskScan2
        if len(fol) + len(fil) == 0: dFolders.append(folder) # no shared contents, must be a distributed folder # diskScan2
        else: files.extend(fil)                                                  # diskScan2
    # print("3--", [dFolders, files], base)                                      # diskScan2
    return [dFolders, files]                                                     # diskScan2
def getFolderSize2(folder:str):                                                  # getFolderSize2
    folder = os.path.expanduser(folder)                                          # getFolderSize2
    return None | cmd(f"du -s {folder}") | table() | cut(0) | item() | aS(int) | op()*1024 # getFolderSize2
def diskScan3(base:str, accurate=False):                                         # diskScan3
    base = os.path.expanduser(base); folders, files = diskScan2(f"1\ue000{base}") | op().split("\ue000")[1].all(2) | apply(set) | apply(list) | aS(list) # getting rid of all file/folder flags # diskScan3
    getFZ = getFolderSize if accurate else getFolderSize2                        # diskScan3
    folders = [folders, None | applyCl.aS(lambda: folders | apply(lambda x: getFZ(x)           if os.path.exists(x) else 0) | deref(), timeout=300) | cut(1) | transpose()] | transpose() | deref() # diskScan3
    files   = [files,   None | applyCl.aS(lambda: files   | apply(lambda x: os.path.getsize(x) if os.path.exists(x) else 0) | deref(), timeout=300) | cut(1) | transpose()] | transpose() | deref() # diskScan3
    # this section below tries to squeeze out replicatedFolders from a bunch of replicatedFiles. The exact mechanism involved may seem like magic to you, but it seems to work # diskScan3
    balancedFolders = folders; replicatedFiles, balancedFiles = files | filt(filt("x") | aS(set) | shape(0) | (op() == 1), 1).split() | deref() # diskScan3
    f1 = iden() & apply(os.path.dirname) | joinStreams() | aS(set)               # diskScan3
    excludedFolders = balancedFolders | cut(0) | serial(*[f1]*100) | aS(set)     # diskScan3
    f = iden() & apply(os.path.dirname) | joinStreams() | ~inSet(excludedFolders); elims = []; i = 0 # diskScan3
    a = replicatedFiles | cut(0) | apply(os.path.dirname) | serial(*[f]*30) | aS(set) | sort(None, False) | aS(list) # diskScan3
    while i < len(a): # trying to eliminate child directories, so that replicatedFolders work recursively. Doing this weird index loop so that time complexity is O(n*log(n)) instead of O(n^2) # diskScan3
        j = i+1                                                                  # diskScan3
        while j < len(a) and a[j].startswith(a[i]): elims.append(a[j]); j += 1   # diskScan3
        i = j                                                                    # diskScan3
    candidates = a | ~inSet(elims) | deref() # replicatedFolder candidates. Has to reverify that total folder size is the same before declaring it a replicated folder. Yes, this is not the same as each individual files are the same, and I can imagine an edge case that will trip this up, but it's so damn rare and I'm so lazy that I'm sticking with this version # diskScan3
    replicatedFolders = [candidates, None | applyCl.aS(lambda: candidates | apply(lambda x: getFolderSize(x) if os.path.exists(x) else 0) | deref()) | cut(1) | transpose()] | transpose() | apply(filt("x") | aS(set) | shape(0) | aS("x == 1"), 1) | filt("x", 1) | cut(0) | deref() # diskScan3
    replicatedFiles = replicatedFiles | ~filt(lambda fn: replicatedFolders | filt(lambda folder: fn.startswith(f"{folder}/")) | shape(0), 0) | deref() # diskScan3
    replicatedFolders = [replicatedFolders, None | applyCl.aS(lambda: replicatedFolders | apply(lambda x: getFZ(x) if os.path.exists(x) else 0) | deref()) | cut(1) | transpose()] | transpose() | deref() # diskScan3
    return balancedFolders, replicatedFolders, balancedFiles, replicatedFiles    # diskScan3
def diskScan4(base:str, sortSize=True, accurate=False): # fully featured data    # diskScan4
    return diskScan3(base, accurate) | (apply(~sortF(toSum(), 1)) if sortSize else iden()) | deref() # diskScan4
def diskScan5(base:str, sortSize=True, accurate=False, f=iden()): # displays it in a nice format # diskScan5
    d4 = diskScan4(base, sortSize, accurate) | f; lens = d4 | apply(len) | deref(); nodeNames = None | applyCl.aS(lambda: os.cpu_count()) | apply(op()[:5], 0) | apply('f"{x} thr"', 1) | join(", ").all() | deref(); nodeNames # diskScan5
    d5 = d4 | apply(~apply(lambda path, sizes: [path, sizes | toSum() | aS(fmt.size), sizes | apply(fmt.size)]) | insert(["-"*40, "-"*10, ["-"*12]*len(nodeNames)]) | insert(["", "", nodeNames])) | deref(); d5 # diskScan5
    ws = d5 | shape(0).all() | deref()                                           # diskScan5
    d6 = d5 | joinStreams() | cut(0, 1) & (cut(2) | pretty() | wrapList().all()) | transpose() | joinStreams().all() | splitW(*ws) | insert(["Path", "Total size", "Size on each node (node id and thread count)"]).all() | joinStreams() | pretty() | splitW(*ws | apply(op()+1)) | deref() # diskScan5
    explainers = ["\nA distributed folder is a folder that has many files and folders inside, but their names\nare all different from each other. It's managed by applyCl.balanceFolder()", # diskScan5
                  "\nA replicated folder is a folder that has been copied to multiple nodes. Size of all folder\ncopies should be the same. It's managed by applyCl.replicateFolder()", # diskScan5
                  "\nA distributed file is a file that has been split into multiple pieces and sent to other\nnodes. It's managed by applyCl.balanceFile()", # diskScan5
                  "\nA replicated file is a file that has been copied to multiple nodes. Size of all file\ncopies should be the same. It's managed by applyCl.replicateFile()",] # diskScan5
    arr = [d6, ["Distributed folders", "Replicated folders", "Distributed files", "Replicated files"] | (aS(lambda x: [["="*60, x, "="*60] | join(" ")])).all()] | transpose() | permute(1, 0) | (joinStreams() | join("\n")).all() | wrapList() | insert(explainers, False) | transpose() | join("\n").all() | deref() # diskScan5
    [arr, lens] | transpose() | filt(op(), 1) | cut(0) | join("\n"*2) | wrapList() | stdout() # diskScan5