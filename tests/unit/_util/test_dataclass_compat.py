import dataclasses as dataclasses_real
import pytest
import typing as t

import ansible_sdk._util.dataclass_compat as dataclasses


@pytest.mark.skipif(getattr(dataclasses_real, 'KW_ONLY', None), reason='builtin dataclass supports kw_only')
class TestKWOnlyPolyfill:
    def test_basics(self):
        @dataclasses.dataclass(kw_only=True, frozen=True)  # pass a "real" dataclass arg as well to make sure we propagate it
        class TestFrozenDC:
            required_str: str
            optional_int: t.Optional[int] = None

        kwargs = dict(required_str='strvalue', optional_int=42)

        dc = TestFrozenDC(**kwargs)

        assert dataclasses.asdict(dc) == kwargs, 'missing values'

        with pytest.raises(dataclasses.FrozenInstanceError):
            dc.required_str = "can't set if frozen passed through"

        with pytest.raises(TypeError, match='TestFrozenDC only supports construction with keyword arguments'):
            dc = TestFrozenDC("positional arg", 42)

    @pytest.mark.xfail(reason='figure out a way to skip the order check')
    def test_inheritance(self):
        # ensure that inherited children sort properly
        @dataclasses.dataclass(kw_only=True)
        class BaseDC:
            required_str: str
            optional_int: t.Optional[int] = None

        @dataclasses.dataclass(kw_only=True)
        class DerivedDC(BaseDC):
            derived_required_str: str
            derived_optional_str: t.Optional[str] = None

        dc = DerivedDC(required_str='x', derived_required_str='y')

    def test_with_callable_decorator(self):
        @dataclasses.dataclass
        class CallableDecoratorDC:
            required_str: str

        dc = CallableDecoratorDC(required_str='hi mom')
        assert dc.required_str == 'hi mom'

