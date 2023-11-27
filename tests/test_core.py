from template.core import addInt
import pytest

@pytest.mark.parametrize("x,y,z", [(1,2,3), (2,3,5), (5,8,13)])
def test_addInt(x, y, z):
    print(f"{x} + {y} = {addInt(x, y)}")
    assert z == addInt(x, y)