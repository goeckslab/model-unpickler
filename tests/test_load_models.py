import os
import re
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier

from model_unpickler import SafeUnpickler
from model_unpickler import safe_load_model


test_folder = Path(__file__).parent.joinpath('test-data')


def test_safe_load_model():
    model = test_folder.joinpath('RandomForestRegressor01.zip')
    with open(model, 'rb') as fh:
        safe_unpickler = SafeUnpickler(fh)

    assert RandomForestClassifier == \
        safe_unpickler.find_class('sklearn.ensemble._forest',
                                  'RandomForestClassifier')

    for name in os.listdir(test_folder):
        model_path = os.path.join(test_folder, name)
        print(model_path)
        if model_path.endswith('.zip'):
            with open(model_path, 'rb') as fh:
                safe_load_model(fh)
