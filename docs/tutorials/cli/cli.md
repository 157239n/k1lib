# k1lib.bioinfo.cli module

This tutorial is for the basics of the `k1lib.bioinfo.cli` module (docs at https://k1lib.github.io/latest/bioinfo/cli.html). As a quick reminder, this module allows you to use common cli tools from the linux cli inside of Python. The idea for this module came across while I was reading over the [Biostar Handbook](https://www.biostarhandbook.com/). They used a lot of cli tools, but all of them are sort of weird, unintuitive, not powerful, and just painful to work with. That's why I made this module to move everything to regular Python.

We're going to go over the multilanguage names dataset from a [PyTorch RNN tutorial](https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial.html). The data folder is at [../cli_name_languages](../cli_name_languages) btw. My advice is to read this along with the docs page, and see the sources of functions that you're interested in.


```python
from k1lib.imports import *
from k1lib.bioinfo.cli import *
import unicodedata, string
```


<style>div.jp-OutputArea-output pre {white-space: pre;}</style>



<style>div.output_area pre {white-space: pre;}</style>



```python
namesFolder = "cli_name_languages/names"
nameFiles = glob.glob(f"{namesFolder}/*.txt")
withBareNames = insertColumn(*(nameFiles | split("/", -1) | split(".", 0))) | display(None)
nameFiles[:3], len(nameFiles)
```




    (['cli_name_languages/names/Korean.txt',
      'cli_name_languages/names/Spanish.txt',
      'cli_name_languages/names/Greek.txt'],
     18)



So, we have 18 files in total. Let's look over a few of them:


```python
cat(nameFiles[0]) | headOut(3)
```

    Ahn
    Baik
    Bang


You can also pipe the file name in btw, like this:


```python
nameFiles[0] | cat() | headOut(3)
```

    Ahn
    Baik
    Bang


Let's convert all unicode chars to regular ascii (taken from the PyTorch doc):


```python
letters = string.ascii_letters + ".,;'"
def unicodeToAscii(s, notIn=False):
    if notIn: # debug case
        return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn" and c not in letters)
    else: # "right" case
        return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn" and c in letters)
```

How many names in total across files?


```python
nameFiles | cats() | joinStreams() | shape(0)
```




    20074



How many names with weird unicode characters?


```python
def unicodes(): return nameFiles | cats() | joinStreams() | apply(partial(unicodeToAscii, notIn=True))
unicodes() | count() | display(None)
```

    19962          99%   
    47             0%    
    3              0%    
    21      -      0%    
    2       --     0%    
    1              0%    
    23             0%    
    1       /      0%    
    3       1      0%    
    9       ß      0%    
    1       ł      0%    
    1       :      0%    


See over https://k1lib.github.io/latest/bioinfo/streams for more info about how stuff like `cats()` and `joinStreams()` work. Also, `partial` is a pretty awesome function I might add, look over it at [Python functools docs](https://docs.python.org/3/library/functools.html#functools.partial). There're lots of empty names here, so let's get rid of them


```python
unicodes() | strip() | ~isValue("") | count() | display()
```

    21   -    55%   
    2    --   5%    
    1    /    3%    
    3    1    8%    
    9    ß    24%   
    1    ł    3%    
    1    :    3%    


Here, we're just stripping white spaces at both ends of each name (`strip()`) and filters them out (`~isValue("")`). The tilde `~` sign common in front of every filter functions effectively inverts the filter's condition. How many duplicate names are there in a file?


```python
nameFiles | cats() | (count() | ~isValue("1", 0) | shape(0)).all() | tableFromList() | withBareNames
```

    Korean       94     
    Spanish      296    
    Greek        193    
    Irish        226    
    Scottish     100    
    Portuguese   74     
    Russian      9342   
    Czech        503    
    French       273    
    German       706    
    Japanese     990    
    Polish       138    
    Arabic       108    
    English      3668   
    Chinese      246    
    Dutch        286    
    Italian      701    
    Vietnamese   71     


Okay yeah there's a lot. Let's see how many unique names (of each file) that appear in other files:


```python
nameFiles | cats() | toSet().all() | joinStreams() | (identity() & toSet()) | shape(0).all() | dereference()
```




    [18015, 17458]



Let's see what are the actual Korean names that appear in other files:


```python
nameFiles | AA_(0) | ((cat() | infinite()) + cats()) | joinColumns() | intersection().all() | withBareNames
```

    Korean                                                                                                                                  
    Spanish                                                                                                                                 
    Greek                                                                                                                                   
    Irish                                                                                                                                   
    Scottish                                                                                                                                
    Portuguese   Han    Li                                                                                                                  
    Russian                                                                                                                                 
    Czech                                                                                                                                   
    French       Wang                                                                                                                       
    German       Jo     Seo    Ko                                                                                                           
    Japanese                                                                                                                                
    Polish                                                                                                                                  
    Arabic       Moon   Yang   Wang    Lee   Chong   Chung                                                                                  
    English      Yun    Koo    Chang   Sun   Yang    Chin    Wang   Chou   Woo   Han   Yim   Chi   Chong   Hong   Kang   Song   You   Chu   
    Chinese                                                                                                                                 
    Dutch                                                                                                                                   
    Italian      Ha     Kim    Han     Ma    Chung   Chu     Ho                                                                             
    Vietnamese                                                                                                                              


`cat() | infinite()`'s branch essentially creates `Iterator[File]`, and each `File` is actually just `Iterator[str]`. Result of `cats()` is also `Iterator[File]`. We want to place these 2 lists' elements on each row, so we can actually operate on them. `joinColumns()` will output `Iterator[(File, File)]`. First file is the Korean one, second file is every other file. `intersection()` will find the common names between the 2 files, and `insertColumn()` just to have some nice formatting.

How about we do this for every file and record how many names in that that is in other files:


```python
analyze2Files = intersection() | shape(0) # takes 2 files, and squish them into 1 value
analyze1Combo = ((cat() | infinite()) + cats()) | joinColumns() | analyze2Files.all() | toSum() # summing all common values
nameFiles | AA_(None) | analyze1Combo.all() | tableFromList() | withBareNames
```

    Korean       37    
    Spanish      104   
    Greek        1     
    Irish        78    
    Scottish     115   
    Portuguese   57    
    Russian      74    
    Czech        41    
    French       102   
    German       148   
    Japanese     9     
    Polish       24    
    Arabic       5     
    English      381   
    Chinese      52    
    Dutch        58    
    Italian      54    
    Vietnamese   20    


Nice. Anyway, hope you are as thrilled as I am about this. Really complicated loops and whatnot can be explored quite quickly without actually writing any loops, and that helps with bringing down iteration time.


```python

```
