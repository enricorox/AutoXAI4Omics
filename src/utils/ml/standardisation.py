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

from sklearn.preprocessing import QuantileTransformer
import logging
import scipy.sparse

omicLogger = logging.getLogger("OmicLogger")


def standardize_data(data):
    """
    Standardize the input X using Standard Scaler
    """
    omicLogger.debug("Applying Standard scaling to given data...")

    if scipy.sparse.issparse(data):
        data = data.todense()
    else:
        data = data

    SS = QuantileTransformer(
        n_quantiles=max(20, data.shape[0] // 20), output_distribution="normal"
    )
    data = SS.fit_transform(data)
    return data, SS
