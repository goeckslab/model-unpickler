import _compat_pickle
import json
import logging
import pickle
import os
import sys
from pathlib import Path


log = logging.getLogger(__name__)

# handle pickle white list file
WL_FILE = os.environ.get('PK_WHITELIST_PATH') or \
    str(Path(__file__).parent.joinpath(
        'pk_whitelist.json').absolute())


class SafeUnpickler(pickle.Unpickler, object):
    """
    Used to safely deserialize scikit-learn model objects
    Usage:
        eg.: SafeUnpickler.load(pickled_file_object)
    """
    def __init__(self, file, **kwargs):
        super(SafeUnpickler, self).__init__(file, **kwargs)
        # load global white list
        with open(WL_FILE, 'r') as f:
            pk_whitelist = json.load(f)

        self.whitelist = pk_whitelist['SK_NAMES'] + \
            pk_whitelist['SKR_NAMES'] + \
            pk_whitelist['XGB_NAMES'] + \
            pk_whitelist['NUMPY_NAMES'] + \
            pk_whitelist['IMBLEARN_NAMES'] + \
            pk_whitelist['MLXTEND_NAMES'] + \
            pk_whitelist['SKOPT_NAMES'] + \
            pk_whitelist['KERAS_NAMES'] + \
            pk_whitelist['GENERAL_NAMES'] + \
            pk_whitelist['TORCH_NAMES'] + \
            pk_whitelist['GALAXY-ML_NAMES']

        self.bad_names = (
            'and', 'as', 'assert', 'break', 'class', 'continue',
            'def', 'del', 'elif', 'else', 'except', 'exec',
            'finally', 'for', 'from', 'global', 'if', 'import',
            'in', 'is', 'lambda', 'not', 'or', 'pass', 'print',
            'raise', 'return', 'try', 'system', 'while', 'with',
            'True', 'False', 'None', 'eval', 'execfile', '__import__',
            '__package__', '__subclasses__', '__bases__', '__globals__',
            '__code__', '__closure__', '__func__', '__self__', '__module__',
            '__dict__', '__class__', '__call__', '__get__',
            '__getattribute__', '__subclasshook__', '__new__',
            '__init__', 'func_globals', 'func_code', 'func_closure',
            'im_class', 'im_func', 'im_self', 'gi_code', 'gi_frame',
            '__asteval__', 'f_locals', '__mro__')

        # custom module in Galaxy-ML
        self.custom_modules = [
            'keras_galaxy_models',
            'feature_selectors', 'preprocessors',
            'iraps_classifier', 'model_validations']

    # override
    def find_class(self, module, name):
        # balack list first
        if name in self.bad_names:
            raise pickle.UnpicklingError("Global '%s.%s' is forbidden"
                                         % (module, name))

        if (module, name) in _compat_pickle.NAME_MAPPING:
            module, name = _compat_pickle.NAME_MAPPING[(module, name)]
        elif module in _compat_pickle.IMPORT_MAPPING:
            module = _compat_pickle.IMPORT_MAPPING[module]

        fullname = module + '.' + name

        if fullname not in self.whitelist:
            # raise pickle.UnpicklingError
            raise pickle.UnpicklingError("Global '%s' is forbidden"
                                         % fullname)

        __import__(module, level=0)
        new_global = getattr(sys.modules[module], name)

        assert new_global.__module__ == module
        log.debug(f"SafeUnpickler loaded global: `{fullname}`.")
        return new_global


def safe_load_model(file):
    """Load pickled object with `SafeUnpickler`
    """
    return SafeUnpickler(file).load()
