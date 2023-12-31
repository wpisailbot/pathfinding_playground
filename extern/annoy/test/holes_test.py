# Copyright (c) 2013 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import random

import numpy

from annoy import AnnoyIndex


def test_random_holes():
    f = 10
    index = AnnoyIndex(f, "angular")
    valid_indices = random.sample(range(2000), 1000)  # leave holes
    for i in valid_indices:
        v = numpy.random.normal(size=(f,))
        index.add_item(i, v)
    index.build(10)
    for i in valid_indices:
        js = index.get_nns_by_item(i, 10000)
        for j in js:
            assert j in valid_indices
    for i in range(1000):
        v = numpy.random.normal(size=(f,))
        js = index.get_nns_by_vector(v, 10000)
        for j in js:
            assert j in valid_indices


def _test_holes_base(n, f=100, base_i=100000):
    annoy = AnnoyIndex(f, "angular")
    for i in range(n):
        annoy.add_item(base_i + i, numpy.random.normal(size=(f,)))
    annoy.build(100)
    res = annoy.get_nns_by_item(base_i, n)
    assert set(res) == set([base_i + i for i in range(n)])


def test_root_one_child():
    # See https://github.com/spotify/annoy/issues/223
    _test_holes_base(1)


def test_root_two_children():
    _test_holes_base(2)


def test_root_some_children():
    # See https://github.com/spotify/annoy/issues/295
    _test_holes_base(10)


def test_root_many_children():
    _test_holes_base(1000)
