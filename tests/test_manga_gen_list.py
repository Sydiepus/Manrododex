import pytest

import tests
from manrododex.manga import _gen_list

gen = tests.gen
ex_gen = tests.ex_gen
param = [(u, v) for u, v in zip(gen, ex_gen)]


@pytest.mark.parametrize("genf,ex_genf", param)
def test__gen_list(genf, ex_genf):
    res = _gen_list(genf)
    assert res == ex_genf
