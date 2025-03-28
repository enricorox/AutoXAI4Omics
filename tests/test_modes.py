# Copyright 2024 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import pytest
from os.path import exists
import sys
import yaml
import pandas as pd
import json
import glob

sys.path.append("../AutoXAI4Omics/")


# Test to check if all scripts run to completion without raising errors for non-omic data
@pytest.mark.synthetic
@pytest.mark.modes
@pytest.mark.container
@pytest.mark.parametrize(
    "mode",
    [
        pytest.param("train", marks=pytest.mark.training),
        pytest.param("test", marks=pytest.mark.holdout),
        pytest.param("plotting", marks=pytest.mark.plotting),
        pytest.param("predict", marks=pytest.mark.prediction),
        pytest.param("feature", marks=pytest.mark.feature),
    ],
)
@pytest.mark.parametrize(
    "problem_create",
    [
        (
            pytest.param(
                ["binary", True],
                marks=[
                    pytest.mark.classification,
                    pytest.mark.binary,
                    pytest.mark.ready,
                ],
            )
        ),
        (
            pytest.param(
                ["binary", False],
                marks=[pytest.mark.classification, pytest.mark.binary, pytest.mark.raw],
            )
        ),
        (
            pytest.param(
                ["multi", True],
                marks=[
                    pytest.mark.classification,
                    pytest.mark.multi,
                    pytest.mark.ready,
                ],
            )
        ),
        (
            pytest.param(
                ["multi", False],
                marks=[pytest.mark.classification, pytest.mark.multi, pytest.mark.raw],
            )
        ),
        (
            pytest.param(
                ["reg", True], marks=[pytest.mark.regression, pytest.mark.ready]
            )
        ),
        (pytest.param(["reg", False], marks=[pytest.mark.regression, pytest.mark.raw])),
    ],
    indirect=True,
)
def test_modes(mode, problem_create, container):
    assert container
    fname = problem_create.split("/")[1]
    sp = subprocess.call(["./autoxai4omics.sh", "-m", mode, "-c", fname])
    assert sp == 0

    with open(f"configs/{fname}", "r") as infile:
        config = json.load(infile)
    log_filepath = (
        config["data"]["save_path"][1:]
        + f'results/{config["data"]["name"]}/AutoXAI4OmicsLog_*'
    )
    log_filepath = sorted(glob.glob(log_filepath), reverse=True)[-1]
    with open(log_filepath, "r") as F:
        last_line = F.readlines()[-2:]
    assert "INFO : Process completed." in last_line[0] or last_line[1]


# Test to check if the outputs are the same as expected outcomes
@pytest.mark.output
@pytest.mark.synthetic
@pytest.mark.parametrize(
    "problem",
    [
        pytest.param(
            "classification",
            marks=[
                pytest.mark.classification,
                pytest.mark.binary,
                pytest.mark.skipif(
                    not (
                        exists(
                            "experiments/results/generated_test_classification_run1_1/best_model/"
                        )
                    ),
                    reason="Best model folder was not created",
                ),
            ],
        ),
        pytest.param(
            "multi",
            marks=[
                pytest.mark.classification,
                pytest.mark.multi,
                pytest.mark.skipif(
                    not (
                        exists(
                            "experiments/results/generated_test_classification_multi_run1_1/best_model/"
                        )
                    ),
                    reason="Best model folder was not created",
                ),
            ],
        ),
        pytest.param(
            "regression",
            marks=[
                pytest.mark.regression,
                pytest.mark.skipif(
                    not (
                        exists(
                            "experiments/results/generated_test_regression_run1_1/best_model/"
                        )
                    ),
                    reason="Best model folder was not created",
                ),
            ],
        ),
    ],
)
def test_model_outputs(problem):
    with open("tests/result_sets/best_model_names.yml") as file:
        best_model_names = yaml.safe_load(file)

    if problem != "multi":
        assert exists(
            f"experiments/results/generated_test_{problem}_run1_1/best_model/{best_model_names[problem]}_best.pkl"
        )

        df_run = pd.read_csv(
            f"experiments/results/generated_test_{problem}_run1_1/results/scores__performance_results_testset.csv"
        ).set_index("model")
        df_stored = pd.read_csv(f"tests/result_sets/{problem}_results.csv").set_index(
            "model"
        )

        assert (df_run == df_stored).all().all()

    else:
        assert exists(
            f"experiments/results/generated_test_classification_{problem}_run1_1/best_model/{best_model_names[problem]}_best.pkl"
        )

        df_run = pd.read_csv(
            f"experiments/results/generated_test_classification_{problem}_run1_1/results/scores__performance_results_testset.csv"
        ).set_index("model")
        df_stored = pd.read_csv(f"tests/result_sets/{problem}_results.csv").set_index(
            "model"
        )

        assert (df_run == df_stored).all().all()


# Test to check if all scripts run to completion without raising errors for omic data
@pytest.mark.omics
@pytest.mark.container
@pytest.mark.skipif(
    not (exists("configs/OmicsTestSets/configs")),
    reason="OmicsTestSets (configs) not present",
)
@pytest.mark.skipif(
    not (exists("data/OmicsTestSets/data")), reason="OmicsTestSets (data) not present"
)
@pytest.mark.parametrize(
    "mode",
    [
        pytest.param("train", marks=pytest.mark.training),
        pytest.param("test", marks=pytest.mark.holdout),
        pytest.param("plotting", marks=pytest.mark.plotting),
        pytest.param("predict", marks=pytest.mark.prediction),
        pytest.param("feature", marks=pytest.mark.feature),
    ],
)
@pytest.mark.parametrize(
    "omic",
    [
        pytest.param("geneExp", marks=pytest.mark.gene),
        pytest.param("metabolomic", marks=pytest.mark.metabolomic),
        pytest.param("microbiome", marks=pytest.mark.microbiome),
        pytest.param("tabular", marks=pytest.mark.tabular),
    ],
)
@pytest.mark.parametrize(
    "problem",
    [
        pytest.param("binary", marks=[pytest.mark.classification, pytest.mark.binary]),
        pytest.param("multi", marks=[pytest.mark.classification, pytest.mark.multi]),
        pytest.param("reg", marks=pytest.mark.regression),
    ],
)
def test_omic_datasets(mode, omic, problem, container):
    assert container
    fname = f"OmicsTestSets/configs/test_{omic}_{problem}.json"
    sp = subprocess.call(["./autoxai4omics.sh", "-m", mode, "-c", fname])
    assert sp == 0

    with open(f"configs/{fname}", "r") as infile:
        config = json.load(infile)
    log_filepath = (
        config["data"]["save_path"][1:]
        + f'results/{config["data"]["name"]}/AutoXAI4OmicsLog_*'
    )
    log_filepath = sorted(glob.glob(log_filepath), reverse=True)[-1]
    with open(log_filepath, "r") as F:
        last_line = F.readlines()[-2:]
    assert "INFO : Process completed." in last_line[0] or last_line[1]
