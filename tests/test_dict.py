# SPDX-FileCopyrightText: 2023 Geoffrey Lentner
# SPDX-License-Identifier: MIT

"""Unit tests for DictSchema."""


# external libs
import pytest

# internal libs
from schema_check import DictSchema, SchemaError, Size


@pytest.mark.unit
class TestDictSchema:
    """Unit tests for DictSchema."""

    @staticmethod
    def test_any() -> None:
        schema = DictSchema.any()
        assert schema.ensure({'a': 1, 'b': True}) == {'a': 1, 'b': True}

    @staticmethod
    def test_any_raises_on_non_str_keys() -> None:
        schema = DictSchema.any()
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure({1: 'a', 2: 'b'})  # noqa: wrong type
        response, = exc_info.value.args
        assert response == 'Expected all keys to be type str, found int(1) at position 0'

    @staticmethod
    def test_any_raises_on_non_dict() -> None:
        schema = DictSchema.any()
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure(['a', 'b', 'c'])
        response, = exc_info.value.args
        assert response == 'Expected DictSchema.any(), found list([\'a\', \'b\', \'c\'])'

    @staticmethod
    def test_any_raises_on_wrong_size() -> None:
        schema = DictSchema.any(size=3)
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure({'a': 1, 'b': 2})
        response, = exc_info.value.args
        assert response == 'Expected length 3, found length 2'

    @staticmethod
    def test_member_type() -> None:
        schema = DictSchema.of(float)
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure({'a': 1, 'b': 'banana'})
        response, = exc_info.value.args
        assert response == ('Expected all members to be type float, found str(\'banana\') '
                            'at position 1 for member \'b\'')

    @staticmethod
    def test_explicit_keys_missing() -> None:
        schema = DictSchema.of(float, keys=['a', 'b', 'c'])
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure({'a': 1, 'b': 2})
        response, = exc_info.value.args
        assert response == 'Missing key \'c\''

    @staticmethod
    def test_explicit_keys_unexpected() -> None:
        schema = DictSchema.of(float, keys=['a', 'b', 'c'])
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure({'a': 1, 'b': 2, 'c': 3, 'd': 4})
        response, = exc_info.value.args
        assert response == 'Unexpected key \'d\''

    @staticmethod
    def test_explicit_keys_with_types() -> None:
        schema = DictSchema.of({'a': float, 'b': str})
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure({'a': 1, 'b': 2})
        response, = exc_info.value.args
        assert response == 'Expected type str for member \'b\', found int(2) at position 1'
