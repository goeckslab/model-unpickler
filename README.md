# model-unpickler
A tool to load machine/deep learning models with security.


_Many machine/deep learning libraries (PyTorch, Scikit-Learn and so on) save trained models solely based on Python pickle, while pickle is well known for its potential to execute malicious code when loading objects from untrusted sources._

_This libary provides a secure tool to load pickled models by overriding the `find_class` method of standard python Unpickler class together with a series of global names -- __whilelist__. Only globals in the whilelist are allowed in loaded model objects, whereas the loading process interrupts when an untrusted global name is found to prevent any potential exploit._


_This libary also provides utils to quickly update the global whilelist in case that the corresponding machine learning libraries are updated._

### Useage

For scikit-learn or other galaxy-ml supported models
```
from model_unpickler import safe_load_model

with open('path_to_model', 'rb') as f:
    safe_load_model(f)
```

For torch models
```
import pickle
from model_unpickler import SafeUnpickler


# Override pickle Unpickler with SafeUnpickler before calling `torch.load`
setattr(pickle, 'Unpickler', SafeUnpickler)

# torch.load('path_to_model')
```

To generate a new whitelist
```
python scripts/gen_whitelist.py
```

To use costom whitelist file, set environment variable `PK_WHITELIST_PATH`
```
# linux
export PK_WHITELIST_PATH='path_to_new_whitelist_file'
```
