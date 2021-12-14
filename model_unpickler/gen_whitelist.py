import json
import inspect
import pkgutil
import sys
from pathlib import Path

try:
    import sklearn
except:
    pass


def gen_pickle_whitelist():
    """ Generate dict and dump to `pk_whitelist.json`.
    """
    rval = {
        'SK_NAMES': [],
        'SKR_NAMES': [],
        'XGB_NAMES': [],
        'IMBLEARN_NAMES': [],
        'MLXTEND_NAMES': [],
        'SKOPT_NAMES': [],
        'NUMPY_NAMES': [],
        'KERAS_NAMES': [],
        'TORCH_NAMES': [],
        'GALAXY-ML_NAMES': [],
        'GENERAL_NAMES': []
    }

    sk_submodule_excludes = (
        'exceptions', 'externals', 'clone', 'get_config',
        'set_config', 'config_context', 'show_versions',
        'datasets')
    for submodule in (set(sklearn.__all__ + ['_loss'])
                      - set(sk_submodule_excludes)):
        rval['SK_NAMES'].extend(
            find_members('sklearn.' + submodule))
    rval['SK_NAMES'] = sorted(rval['SK_NAMES'])

    rval['SKR_NAMES'].extend(find_members('skrebate'))

    for xgb_submodules in ('callback', 'compat', 'core',
                           'sklearn', 'training'):
        rval['XGB_NAMES'].extend(
            find_members('xgboost.' + xgb_submodules))

    rval['IMBLEARN_NAMES'].extend(find_members('imblearn'))

    for mlx_submodules in ('_base', 'classifier', 'regressor',
                           'frequent_patterns', 'cluster',
                           'feature_selection',
                           'feature_extraction',
                           'preprocessing'):
        rval['MLXTEND_NAMES'].extend(
            find_members('mlxtend.' + mlx_submodules))

    rval['SKOPT_NAMES'].extend(find_members('skopt.searchcv'))
    rval['NUMPY_NAMES'].extend([
        "numpy.core.multiarray._reconstruct",
        "numpy.core.multiarray.scalar",
        "numpy.dtype",
        "numpy.float64",
        "numpy.int64",
        "numpy.ma.core._mareconstruct",
        "numpy.ma.core.MaskedArray",
        "numpy.mean",
        "numpy.ndarray",
        "numpy.random.__RandomState_ctor",
        "numpy.random._pickle.__randomstate_ctor"])

    rval['KERAS_NAMES'].extend([
        "keras.engine.sequential.Sequential",
        "keras.engine.sequential.Functional",
        "keras.engine.sequential.Model"
    ])

    rval['GENERAL_NAMES'].extend([
        "_codecs.encode",
        "builtins.object",
        "builtins.bytearray",
        "collections.OrderedDict",
        "copyreg._reconstructor"
    ])

    rval['TORCH_NAMES'].extend([
        "torch._utils._rebuild_tensor_v2",
        "torch.FloatStorage"
    ])

    for gx_ml_submodules in ('keras_galaxy_models', 'feature_selectors',
                             'preprocessors', 'iraps_classifier',
                             'model_validations', 'binarize_target',
                             'metrics'):
        rval['GALAXY-ML_NAMES'].extend(
            find_members('galaxy_ml.' + gx_ml_submodules))

    with open('whitelist_new.json', 'w') as fh:
        json.dump(rval, fh, indent=4)

    return rval


def find_members(module: str, enforce_import: bool = True):
    """ get class and function members, including those from submodules.
    """
    rval = []

    if module not in sys.modules and enforce_import:
        exec(f"import {module}")
    mod = sys.modules[module]

    members = inspect.getmembers(
        mod,
        lambda x: ((inspect.isclass(x) or inspect.isfunction(x))
                   and x.__module__ == module)
    )
    for mem in members:
        rval.append(module + '.' + mem[0])

    if hasattr(mod, '__path__'):
        for submodule in pkgutil.iter_modules(mod.__path__):
            if submodule.name.lower() in ('tests', 'utils'):
                continue
            rval.extend(find_members(module + '.' + submodule.name,
                                     enforce_import=enforce_import))

    return sorted(rval)
