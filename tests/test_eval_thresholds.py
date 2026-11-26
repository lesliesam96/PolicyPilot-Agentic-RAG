from policypilot.eval.thresholds import check_thresholds

THRESHOLDS = {"a/mean": 0.8, "b/mean": 0.5}


def test_passes_when_all_metrics_meet_minimums():
    failures, missing = check_thresholds({"a/mean": 0.9, "b/mean": 0.5}, THRESHOLDS)
    assert failures == []
    assert missing == []


def test_fails_when_a_metric_is_below_its_minimum():
    failures, missing = check_thresholds({"a/mean": 0.7, "b/mean": 0.9}, THRESHOLDS)
    assert len(failures) == 1
    assert failures[0].startswith("a/mean")
    assert missing == []


def test_missing_metric_warns_instead_of_failing():
    failures, missing = check_thresholds({"a/mean": 0.9}, THRESHOLDS)
    assert failures == []
    assert missing == ["b/mean"]
