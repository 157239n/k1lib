# AUTOGENERATED FILE! PLEASE DON'T EDIT HERE. EDIT THE SOURCE NOTEBOOKS INSTEAD
"""
I have several machine learning tools running on my own cluster that's hosted
on https://mlexps.com/#kapi, and this module contains functions, classes and
clis that will contact that service. This is so that if I want to use a language
model in multiple notebooks, I'd have to load the model into my GPU for each
notebook, which would waste a lot of resources. I can't run a lot of notebooks
at the same time as I'd just run out of VRAM. So, by having dedicated services/demos,
I can really focus on serving things well and make it performant. For example::

    "some text"           | kapi.embed()    # returns embedding numpy array
    "What is Python? "    | kapi.complete() # returns string, completes the sentence
    "image.png" | toImg() | kapi.ocr()      # returns `Ocr` object, with bounding boxes and text content of all possible texts
    "cute anime girl"     | kapi.txt2im()   # generates an image from some description
    "image.png" | toImg() | caption()       # generates a caption of an image


"""
__all__ = ["status", "segment", "demo", "embed", "embeds", "complete",
           "ocr", "Ocr", "OcrBox", "tess",
           "txt2im", "caption", "speech", "summarize", "post"]
from k1lib.cli.init import BaseCli; import k1lib.cli.init as init
import k1lib.cli as cli, k1lib, base64, html, json
requests = k1lib.dep.requests; k1 = k1lib
settings = k1lib.settings.cli
s = k1lib.Settings(); settings.add("kapi", s, "cli.kapi settings")
s.add("local", False, "whether to use local url instead of remote url. This only has relevance to me though, as the services are running on localhost")
def get(idx:str, json):                                                          # get
    """Sends a request to any service/demo on https://mlexps.com.
Example::

    # returns "13.0"
    kapi.get("demos/1-arith", {"a": 1, "b": 3, "c": True, "d": 2.5, "e": 10})

:param idx: index of the service, like "kapi/1-embed" """                        # get
    url = "http://localhost:9000" if s.local else "https://local.mlexps.com"     # get
    res = requests.post(f"{url}/routeServer/{idx.replace('/', '_')}", json=json) # get
    if not res.ok: raise Exception(f"{res.status_code} - {res.reason}")          # get
    res = res.json()                                                             # get
    if not res["success"]: raise Exception(res["reason"])                        # get
    return res["data"]                                                           # get
def jsF_get(idx, dataIdx):                                                       # jsF_get
    url = "https://local.mlexps.com"                                             # jsF_get
    return f"""await (await fetch("{url}/routeServer/{idx.replace('/', '_')}", {{method: "POST", headers: {{ "Content-Type": "application/json" }}, body: JSON.stringify({dataIdx})}})).json()""" # jsF_get
def status():                                                                    # status
    """Displays a table of whether the services are online and available or not""" # status
    ["kapi/1-embed", "kapi/2-complete", "kapi/3-ocr", "kapi/4-txt2im", "kapi/5-caption", "kapi/6-speech"] | cli.apply(lambda x: [x, requests.get(f"https://local.mlexps.com/routeServer/{x.replace(*'/_')}/healthCheck").text == "ok"]) | cli.insert(["Service", "Online"]) | cli.display(None) # status
class segment(BaseCli):                                                          # segment
    def __init__(self, limit:int=2000):                                          # segment
        """Segments the input string by sentences, such that each segment's length is lower than the specified limit.
Example::

    # returns ['some. Really', 'Long. String', 'Just. Monika']
    "some. Really. Long. String. Just. Monika" | segment(15)

So, this will split the input string by ". ", then incrementally joins the strings together into segments.
This is useful in breaking up text so that it fits within language model's context size""" # segment
        self.limit = limit                                                       # segment
    def __ror__(self, text):                                                     # segment
        if not isinstance(text, str): raise Exception("Input is not a string!")  # segment
        data = [[]]; c = 0; limit = self.limit                                   # segment
        for line in text.split(". "):                                            # segment
            if c + len(line) > limit and c > 0: # if even a single sentence is too big, then just have a segment as that sentence, and don't push it to the next one # segment
                data.append([]); c = 0                                           # segment
            data[-1].append(line); c += len(line)+2                              # segment
        return data | cli.join(". ").all() | cli.deref()                         # segment
metas = {} # Dict[prefix -> demo meta]                                           # segment
class demo(BaseCli):                                                             # demo
    def __init__(self, prefix:str="demos_1-arith"):                              # demo
        """Sends a request to one of mlexps.com demos.
Example::

    # returns 21.0
    {"a": 3} | kapi.demo("demos/1-arith")
    # builds js interface that displays 21.0
    {"a": 3} | (toJsFunc() | kapi.demo("demos/1-arith")) | op().interface("jsone")
    # same as above, but the dictionary is formed in JS instead of Python
    3 | (toJsFunc() | aS("{'a': x}") | demo("demos/1-arith")) | op().interface("jsone")

You don't have to specify all params, just the ones you want to deviate from the defaults""" # demo
        prefix = prefix.replace(*"/_"); self.prefix = prefix                     # demo
        res = requests.get(f"https://mlexps.com/{prefix.replace(*'_/')}/demo_meta.json") # demo
        if not res.ok: raise Exception(f"Demo {prefix.replace(*'_/')} not found!") # demo
        if prefix not in metas: metas[prefix] = json.loads(res.text)             # demo
    def __ror__(self, d):                                                        # demo
        prefix = self.prefix; meta = metas[prefix]; kw = {}                      # demo
        for arg in meta["args"]:                                                 # demo
            a = meta["defaults"][arg]; anno = meta["annos"][arg]                 # demo
            if anno in ("checkbox", "bytes", "image", "serialized"): a = a       # demo
            elif anno == "dropdown": a = a[1][a[0]]                              # demo
            elif anno == "apiKey": a = k1lib.apiKey if hasattr(k1lib, "apiKey") else a[0] # demo
            else: a = a[0]                                                       # demo
            kw[arg] = k1lib.serve.webToPy(a, anno)                               # demo
        for k, v in d.items(): kw[k] = v                                         # demo
        for k, v in kw.items(): kw[k] = k1lib.serve.pyToWeb(v, meta["annos"][k]) # demo
        url = "http://localhost:9003" if k1lib.settings.cli.kapi.local else "https://local.mlexps.com" # demo
        res = requests.post(f"{url}/routeServer/{prefix}", json=kw)              # demo
        if not res.ok: raise Exception(res.reason)                               # demo
        res = res.json()                                                         # demo
        if res["success"]: return k1lib.serve.webToPy(res["data"], meta["annos"]["return"]) # demo
        else: raise Exception(res["reason"])                                     # demo
    def __repr__(self): return f"<demo prefix='{self.prefix}'>"                  # demo
    def _repr_html_(self): s = html.escape(f"{self}"); return f"{s}{metas[self.prefix]['mainDoc']}" # demo
    def _jsF(self, meta):                                                        # demo
        fIdx = init._jsFAuto(); dataIdx = init._jsDAuto(); prefix = self.prefix; prefixSlash = prefix.replace(*"_/") # demo
        try: apiKey = k1lib.apiKey                                               # demo
        except: apiKey = ''                                                      # demo
        return f"""\
{fIdx} = async ({dataIdx}) => {{
    const meta = await (await fetch("https://mlexps.com/{prefixSlash}/demo_meta.json")).json();
    const kw = {{}};
    for (const arg of meta.args) {{
        let a = meta.defaults[arg]; anno = meta.annos[arg];
        if (["checkbox", "bytes", "image", "serialized"].includes(anno)) a = a;
        else if (anno === "dropdown") a = a[1][a[0]];
        else if (anno === "apiKey") a = "{apiKey}";
        else a = a[0];
        kw[arg] = a
    }}
    for (const [k,v] of Object.entries({dataIdx})) {{ kw[k] = v; }}
    let res = await (await fetch("https://local.mlexps.com/routeServer/{prefix}", {{ method: "POST", headers: {{ "Content-Type": "application/json" }}, "body": JSON.stringify(kw) }})).text();
    try {{ res = JSON.parse(res); }} catch (e) {{ throw new Error(`Can't decode json of '${{res}}'`); }}
    if (!res.success) throw new Error(`Request failed: '${{res.reason}}'`);
    let data = res.data;
    if (meta.annos.return === "html") return atob(data);
    if (meta.annos.return === "image") return `<img src="data:image;base64,${{data}}">`
    return data;
}}""", fIdx                                                                      # demo
class embed(BaseCli):                                                            # embed
    def __init__(self):                                                          # embed
        """Gets an embedding vector for every sentence piped into this using `all-MiniLM-L6-v2`.
Example::

    # returns (384,)
    "abc" | kapi.embed() | shape()
    # returns (2, 384)
    ["abc", "def"] | kapi.embed().all() | shape()

- VRAM: 440MB
- Throughput: 512/s

See also: :class:`~k1lib.cli.models.embed`"""                                    # embed
        pass                                                                     # embed
    def __ror__(self, it): return self._all_opt([it]) | cli.item()               # embed
    def _all_opt(self, it:"list[str]"):                                          # embed
        for b in it | cli.batched(1024, True):                                   # embed
            yield from get("kapi/1-embed", {"lines": k1lib.encode(b)}) | cli.aS(k1lib.decode) # embed
class embeds(BaseCli):                                                           # embeds
    def __init__(self):                                                          # embeds
        """Breaks up some text and grab the embedding vectors of each segment.
Example::

    "sone long text" | kapi.embeds() # returns list of (segment, numpy vector)

This is just a convenience cli. Internally, this splits the text up using :class:`segment`
and then embeds each segment using :class:`embed`
"""                                                                              # embeds
        pass                                                                     # embeds
    def __ror__(self, it): return self._all_opt([it]) | cli.item()               # embeds
    def _all_opt(self, it:"list[str]"): return it | cli.apply(segment(700) | cli.iden() & embed().all() | cli.transpose()) | cli.deref() # embeds
class complete(BaseCli):                                                         # complete
    def __init__(self, prompt:str=None, maxTokens:int=200):                      # complete
        """Generates text from predefined prompts using `Llama 2`.
Example::

    # returns string completion
    "What is Python?" | kapi.complete()
    # returns list of string completions
    ["What is Python?", "What is C++?"] | kapi.complete().all()
    # returns list of string completions. The prompts sent to the server are ["<paragraph 1>\\n\\n\\nPlease summarize the above paragraph", ...]
    ["<paragraph 1>", "<paragraph 2>"] | kapi.complete("Please summarize the above paragraph").all()

- VRAM: 22GB
- Throughput: 8/s

:param max_tokens: maximum amount of tokens

See :class:`~k1lib.cli.models.complete`. That one is an older version using Google Flan T5 instead of llama 2""" # complete
        self.prompt = prompt; self.maxTokens = maxTokens                         # complete
    def __ror__(self, it): return self._all_opt([it]) | cli.item()               # complete
    def _all_opt(self, it:"list[str]"):                                          # complete
        if self.prompt: it = it | cli.apply(lambda x: f"{x}\n\n\n{self.prompt}: ") | cli.deref() # complete
        if not (isinstance(it, (list, tuple)) and isinstance(it[0], str)):       # complete
            raise Exception("You might have forgot to use .all(), like ['str1', 'str2'] | kapi.complete().all()") # complete
        it = it | cli.apply(lambda x: [x, self.maxTokens]) | cli.deref()         # complete
        return get("kapi/2-complete", {"prompts": json.dumps(it)}) | cli.aS(json.loads) # complete
    def _jsF(self, meta):                                                        # complete
        fIdx = cli.init._jsFAuto(); dataIdx = cli.init._jsDAuto()                # complete
        body = f"{{ prompts: JSON.stringify([{dataIdx}].map((x) => [`${{x}}\\n\\n\\n{self.prompt or ''}`, {cli.kjs.v(self.maxTokens)}])) }}" # complete
        return f"""
{fIdx} = async ({dataIdx}) => {{
    const res = {jsF_get('kapi/2-complete', body)}
    return res[0]
}}""", fIdx                                                                      # complete
tf = k1.dep("torchvision.transforms")                                            # complete
class ocr(BaseCli):                                                              # ocr
    def __init__(self, paragraph:bool=False, resize=True, bs:int=10):            # ocr
        """Do OCR (optical character recognition) on some image.
Example::

    o = "some_image.png" | toImg() | kapi.ocr() # loads image and do OCR on them
    o     # run this in a separate notebook cell for an overview of where the boxes are
    o.res # see raw results received from the OCR service

That returns something like this::

    [[[771, 5, 813, 17], 'round', 0.7996242908503107],
     [[58, 10, 100, 34], '150', 0.883547306060791],
     [[166, 8, 234, 34], '51,340', 0.9991665158446097],
     [[782, 14, 814, 38], '83', 0.9999995785315409],
     [[879, 13, 963, 33], 'UPGRADes', 0.7625563055298393],
     [[881, 53, 963, 69], 'Monkey Ace', 0.9171751588707685],
     [[933, 133, 971, 149], '5350', 0.9001984000205994],
     [[873, 203, 911, 219], '5325', 0.481669545173645],
     [[931, 203, 971, 219], '5500', 0.7656491994857788],
     [[869, 271, 913, 291], 'G800', 0.31933730840682983],
     [[925, 271, 977, 291], '64600', 0.14578145924474253],
     [[871, 341, 911, 361], '5750', 0.5966295003890991],
     [[929, 341, 971, 361], '5850', 0.9974847435951233]]

First column is the bounding box (x1, y1, x2, y2), second column is the text,
and third column is the confidence, from 0 to 1.

Internally, this uses EasyOCR for the recognition. However, from my experience,
this doesn't always get it right. It's particularly bad at symbols like dollar
signs (it thinks it's "S", or "5" instead), periods or commads. So, you can refine
each of the bounding boxes like this::

    ocr = someImg | kapi.ocr()
    ocr[4] | toImg() | kapi.tess() # returns string, uses tesseract OCR instead of EasyOCR for more accuracy for a less complex scene

See also: :class:`Ocr`

- VRAM: 1GB
- Throughput: depends heavily on image resolution, but for 1000x750 images, should be 3-4 images/s

:param paragraph: whether to try to combine boxes together or not
:param resize: whether to resize the images to a reasonable size before sending it over or not. Runs faster if true
:param bs: how many images should this group together and send to the server at once?""" # ocr
        self.paragraph = paragraph; self.resize = resize; self.bs = bs           # ocr
    def __ror__(self, it): return self._all_opt([it]) | cli.item()               # ocr
    def _all_opt(self, it:"list[PIL.Image.Image]"):                              # ocr
        def resize(it): # resizing if they're too big                            # ocr
            for img in it:                                                       # ocr
                w, h = img | cli.shape()                                         # ocr
                if w > h:                                                        # ocr
                    if w > 1000: frac = 1000/w; img = img | tf.Resize([int(h*frac), int(w*frac)]) # ocr
                else:                                                            # ocr
                    if h > 1000: frac = 1000/h; img = img | tf.Resize([int(h*frac), int(w*frac)]) # ocr
                yield img, self.paragraph                                        # ocr
        return (resize(it) if self.resize else it | cli.apply(lambda img: [img, self.paragraph])) | cli.batched(self.bs, True)\
            | cli.apply(lambda imgParas: [imgParas, get("kapi/3-ocr", {"data": k1.encode(imgParas | cli.apply(cli.toBytes(), 0) | cli.deref())}) | cli.aS(k1.decode)] | cli.transpose()) | cli.joinSt() | ~cli.apply(Ocr) # ocr
class Ocr:                                                                       # Ocr
    def __init__(self, imgPara, res):                                            # Ocr
        """Ocr result object. Stores raw results from model in ``.res`` field and has many
more functionalities. Not intended to be instantiated by the end user. Example::

    ocr = someImg | kapi.ocr() # ocr is an object of type Ocr
    ocrBox = ocr[3] # grabs the 3rd detected bounding box

    ocrBox.coords     # grabs coordinates
    ocrBox.text       # grabs recognized text
    ocrBox.confidence # grabs confidence

    ocrBox | toImg()               # grabs image cutout
    ocrBox | toNdArray()           # grabs numpy array cutout
    ocrBox | toImg() | kapi.tess() # returns string, pass the image through tesseract OCR, to get more reliable results

See also: :class:`OcrBox`"""                                                     # Ocr
        self.img, self.para = imgPara; self._npImg = None; self.res = res | cli.apply(~cli.aS(lambda x1,x2,y1,y2: [x1,y1,x2,y2]), 0) | cli.deref() # Ocr
    def npImg(self):                                                             # Ocr
        """Grabs the numpy array of the image, shape (C, H, W)"""                # Ocr
        if self._npImg is None: self._npImg = self.img | cli.toNdArray()         # Ocr
        return self._npImg                                                       # Ocr
    def __repr__(self): return f"<Ocr shape={self.img | cli.shape()}>"           # Ocr
    def _overlay(self) -> "PIL":                                                 # Ocr
        img = self.img; res = self.res; p5 = k1.p5; w, h = img | cli.shape(); p5.newSketch(*img | cli.shape()); p5.background(255); p5.fill(255, 0) # Ocr
        res | cli.cut(0) | ~cli.apply(lambda x1,y1,x2,y2: [x1,h-y2,x2-x1,y2-y1]) | ~cli.apply(p5.rect) | cli.deref() # Ocr
        res | cli.cut(0, 1) | ~cli.apply(lambda x1,y1,x2,y2: [min(x1,x2), h-max(y1,y2)], 0) | ~cli.apply(lambda xy,s: [s,*xy]) | ~cli.apply(p5.text) | cli.deref() # Ocr
        im2 = p5.img(); alpha = 0.3; return [img, im2] | cli.apply(cli.toTensor() | cli.op()[:3]) | ~cli.aS(lambda x,y: x*alpha+y*(1-alpha)) | cli.op().to(int) | cli.op().permute(1, 2, 0) | cli.toImg() # Ocr
    def _repr_html_(self): s = html.escape(f"{self}"); return f"<pre>{s}</pre><img src='data:image/jpeg;base64, {base64.b64encode(self._overlay() | cli.toBytes()).decode()}' />" # Ocr
    def __getitem__(self, s):                                                    # Ocr
        if isinstance(s, slice): return [OcrBox(self, i) for i in range(len(self.res))[s]] # Ocr
        return OcrBox(self, s)                                                   # Ocr
    def __len__(self): return len(self.res)                                      # Ocr
    def __getstate__(self): d = {**self.__dict__}; d["img"] = self.img | cli.toBytes(); d["_npImg"] = None; return d # better compression due to converting to jpg # Ocr
    def __setstate__(self, d): self.__dict__.update(d); self.img = self.img | cli.toImg(); self._npImg = None # Ocr
class OcrBox:                                                                    # OcrBox
    def __init__(self, ocr, i):                                                  # OcrBox
        """1 bounding box of the ocr-ed image. Not intended to be instantiated by the end user.
Example::

    ocr = someImg | kapi.ocr()
    ocrBox = ocr[3] # grabs the 3rd detected bounding box

See also: :class:`Ocr`"""                                                        # OcrBox
        self.ocr = ocr; self.i = i                                               # OcrBox
    @property                                                                    # OcrBox
    def coords(self): return self.ocr.res[self.i][0]                             # OcrBox
    @property                                                                    # OcrBox
    def text(self): return self.ocr.res[self.i][1]                               # OcrBox
    @property                                                                    # OcrBox
    def confidence(self): return self.ocr.res[self.i][2]                         # OcrBox
    def _toNdArray(self):                                                        # OcrBox
        x1,y1,x2,y2 = self.ocr.res[self.i][0]                                    # OcrBox
        return self.ocr.npImg()[:,y1:y2,x1:x2]                                   # OcrBox
    def _toImg(self, **kwargs): return self._toNdArray().transpose((1, 2, 0)) | cli.toImg() # OcrBox
    def __repr__(self): return f"<OcrBox i={self.i} coords={self.coords} confidence={round(self.confidence, 3)} text='{self.text}' />" # OcrBox
    def _repr_html_(self): s = html.escape(f"{self}"); return f"<pre>{s}</pre><img src='data:image/jpeg;base64, {base64.b64encode(self | cli.toImg() | cli.toBytes()).decode()}' />" # OcrBox
init.addAtomic(Ocr); init.addAtomic(OcrBox)                                      # OcrBox
class tess(BaseCli):                                                             # tess
    def __init__(self):                                                          # tess
        """Do OCR using tesseract, instead of easyocr. This is meant for simple images only,
preferably sections cut off from :class:`ocr`. For complex bounding box detection, still
use :class:`ocr`. Example::

    # returns "some text"
    image | kapi.tess()

For small texts, can reach throughput up to 75/s"""                              # tess
        pass                                                                     # tess
    def __ror__(self, it): return self._all_opt([it]) | cli.item()               # tess
    def _all_opt(self, it:"list[str]"):                                          # tess
        for b in it | cli.batched(75, True):                                     # tess
            yield from get("kapi/12-tess", {"imgs": k1lib.encode(b)})            # tess
class txt2im(BaseCli):                                                           # txt2im
    def __init__(self, num_inference_steps=10):                                  # txt2im
        """Generates images from text descriptions, using stable diffusion v2.
Example::

    "a bowl of apples" | kapi.txt2im() # returns PIL image

- VRAM: 5.42GB
- Throughput: 1/s
"""                                                                              # txt2im
        self.num_inference_steps = num_inference_steps                           # txt2im
    def __ror__(self, it): return get("kapi/4-txt2im", {"prompt": it, "num_inference_steps": self.num_inference_steps}) | cli.aS(base64.b64decode) | cli.toImg() # txt2im
class caption(BaseCli):                                                          # caption
    def __init__(self):                                                          # caption
        """Captions images using model `Salesforce/blip-image-captioning-large`.
Example::

    img = "some_image.png" | toImg() # loads PIL image
    img | kapi.caption()                  # returns string description

- VRAM: 2.5GB
- Throughput: 16/s
"""                                                                              # caption
        pass                                                                     # caption
    def __ror__(self, it): return self._all_opt([it]) | cli.item()               # caption
    def _all_opt(self, it:"list[PIL.Image.Image]"): return it | cli.batched(5, True) | cli.apply(lambda imgs: get("kapi/5-caption", {"images": k1lib.encode(imgs)}) | cli.aS(k1lib.decode)) | cli.joinSt() # caption
class speech(BaseCli):                                                           # speech
    def __init__(self, sep=False):                                               # speech
        """Converts English speech to text using whisper-large-v2.
Example::

    "audio.mp3" | toAudio() | kapi.speech() # returns string transcript

- VRAM: 4GB
- Throughput: 20min video finish transcribing in ~25s, so around 60x faster than real time

If the input audio is too long (>25 minutes), then it will be broken up
into multiple smaller pieces around 20 min each and sent to the server,
so at the bounds, it might go wrong a little bit

:param sep: if True, separate transcripts of each segment (returns List[transcript]),
    if False (default), joins segment's transcripts together into a single string""" # speech
        self.sep = sep                                                           # speech
    def __ror__(self, audio:"conv.Audio"):                                       # speech
        nSplits = int(audio.raw.duration_seconds/60/25)+1                        # speech
        res = audio | cli.splitW(*[1]*nSplits) | cli.apply(lambda piece: get("kapi/6-speech", {"audio": base64.b64encode(piece | cli.toBytes()).decode()})) # speech
        return list(res) if self.sep else res | cli.join(". ")                   # speech
def _summarize(text:str) -> str:                                                 # _summarize
    return text | segment(2000) | complete("<|end of transcript|>\n\nPlease summarize the above transcript using 1-3 sentences: ").all()\
        | cli.op().strip().all() | cli.deref() | cli.join(". ")                  # _summarize
class summarize(BaseCli):                                                        # summarize
    def __init__(self, length=1000):                                             # summarize
        """Summarizes text in multiple stages until it's shorter than ``length`` in
characters or until further compression is not possible. Example::

    url = "https://www.youtube.com/watch?v=NfmSjGbnEWk"
    audio = url   | toAudio()     # downloads audio from youtube
    text  = audio | kapi.speech() # does speech recognition
    text | summarize()            # summarize the text. For a 23 minute video/22k characters text, it should take around 23s to summarize everything

This will return an array of strings::

    [
        "shortened text final stage",
        "shortened text stage 2",
        "shortened text stage 1",
        "original text",
    ]

So in each stage, the original text is split up into multiple pieces, then
each piece is summarized using :class:`complete` and then all summary will
be joined together, creating the "shortened text stage 1". This continues
until it the text's length does not decrease any further, or it's shorter
than the desired length.

:param length: desired summary string length"""                                  # summarize
        self.length = length                                                     # summarize
    def __ror__(self, text:str):                                                 # summarize
        stages = [text]; l = len(text)                                           # summarize
        while True:                                                              # summarize
            if len(text) < self.length: return stages | cli.reverse() | cli.deref() # summarize
            l = len(text); text = _summarize(text); stages.append(text)          # summarize
            if len(text)/l > 0.8: return stages | cli.reverse() | cli.deref() # if length not shrinking, then just return early # summarize
class post(BaseCli):                                                             # post
    def __init__(self, url):                                                     # post
        """Creates a post request from a URL that can be read using :meth:`~k1lib.cli.inp.cat`.
Example::

    # returns str of the results
    {"some": "json data"} | kapi.post("https://some.url/some/path")

Notice how there isn't a get request counterpart, because you can always just cat() them
directly, as get requests don't have a body::

    cat("https://some.url/some/path")
"""                                                                              # post
        self.url = url                                                           # post
    def __ror__(self, d): return requests.post(self.url, json=d).text            # post
    def _jsF(self, meta):                                                        # post
        fIdx = init._jsFAuto(); dataIdx = init._jsDAuto()                        # post
        return f"""\
{fIdx} = async ({dataIdx}) => {{
    const res = await fetch({json.dumps(self.url)}, {{ method: "POST", headers: {{ "Content-Type": "application/json" }}, body: JSON.stringify({dataIdx}) }});
    if (res.ok) return await res.text();
    throw new Error(`Can't send POST request to '{self.url}': ${{res.status}} - ${{res.statusText}}`);
}}""", fIdx                                                                      # post
