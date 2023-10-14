# SPDX-FileCopyrightText: 2023 Geoffrey Lentner
# SPDX-License-Identifier: MIT

"""Unit tests for ListSchema."""


# external libs
import pytest

# internal libs
from schema_check import ListSchema, SchemaError, Size


@pytest.mark.unit
class TestListSchema:
    """Unit tests for ListSchema."""

    @staticmethod
    def test_any() -> None:
        schema = ListSchema.any()
        assert schema.ensure([1, 2, 3, 'apple']) == [1, 2, 3, 'apple']
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure(42)
        response, = exc_info.value.args
        assert response == 'Expected list, found int(42)'

    @staticmethod
    def test_any_sized() -> None:
        schema = ListSchema.any(size=4)
        assert schema.ensure([1, 2, 3, 'apple']) == [1, 2, 3, 'apple']
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure([1, 2, 3, 4, 5])
        response, = exc_info.value.args
        assert response == 'Expected length 4, found length 5'

    @staticmethod
    def test_int_sized() -> None:
        schema = ListSchema.of(int, size=5)
        assert schema.ensure([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure([1, 2, 3, 4, 'apple'])
        response, = exc_info.value.args
        assert response == 'Expected all members to be type int, found str(\'apple\') at position 4'
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure([1, 2, 3, 4, 5, 6])
        response, = exc_info.value.args
        assert response == 'Expected length 5, found length 6'

    @staticmethod
    def test_nested() -> None:
        schema = ListSchema.of(ListSchema.of(float, size=3), size=3)
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        assert schema.ensure(data) == data

    @staticmethod
    def test_nested_raises_on_wrong_member_type() -> None:
        schema = ListSchema.of(ListSchema.of(float, size=3), size=3)
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure([1, 2, 3])
        response, = exc_info.value.args
        assert response == 'Expected list, found int(1), for member at position 0'

    @staticmethod
    def test_nested_raises_on_wrong_member_type2() -> None:
        schema = ListSchema.of(ListSchema.of(float, size=3), size=3)
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure([['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']])
        response, = exc_info.value.args
        assert response == ('Expected all members to be type float, found str(\'a\') at position 0, ' 
                            'for member at position 0')

    @staticmethod
    def test_nested_raises_on_wrong_member_size() -> None:
        schema = ListSchema.of(ListSchema.of(float, size=3), size=3)
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure([[1, 2, 3], [4, 5, 6], [7, 8]])
        response, = exc_info.value.args
        assert response == 'Expected length 3, found length 2, for member at position 2'

    @staticmethod
    def test_nested_raises_on_wrong_size() -> None:
        schema = ListSchema.of(ListSchema.of(float, size=3), size=3)
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
        response, = exc_info.value.args
        assert response == 'Expected length 3, found length 4'

    @staticmethod
    def test_nested_equal_member_size() -> None:
        """Use Size.ALL_EQUAL within member to require all are the same length."""
        schema = ListSchema.of(ListSchema.of(float, size=Size.ALL_EQUAL))
        data = [[1, 2, 3], [4, 5, 6]]
        assert schema.ensure(data) == data
        with pytest.raises(SchemaError) as exc_info:
            schema.ensure([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, ]])
        response, = exc_info.value.args
        assert response == 'Expected members of equal size, found size=1 at position 3 but size=3 at position 0'
