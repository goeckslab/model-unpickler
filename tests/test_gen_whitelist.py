from model_unpickler.gen_whitelist import find_members


def test_find_members():
    got = find_members('galaxy_ml.metrics')
    expect = [
        'galaxy_ml.metrics._regression.spearman_correlation_score'
    ]
    assert got == expect, got

    got = find_members('imblearn.over_sampling')
    expect = [
        "imblearn.over_sampling._adasyn.ADASYN",
        "imblearn.over_sampling._random_over_sampler.RandomOverSampler",
        "imblearn.over_sampling._smote.base.BaseSMOTE",
        "imblearn.over_sampling._smote.base.SMOTE",
        "imblearn.over_sampling._smote.base.SMOTEN",
        "imblearn.over_sampling._smote.base.SMOTENC",
        "imblearn.over_sampling._smote.cluster.KMeansSMOTE",
        "imblearn.over_sampling._smote.filter.BorderlineSMOTE",
        "imblearn.over_sampling._smote.filter.SVMSMOTE",
        "imblearn.over_sampling.base.BaseOverSampler"
    ]
    assert got == expect, got