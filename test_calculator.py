import pytest
from calculator import calculate_commission


class TestCalculateCommission:

    @pytest.mark.parametrize("amount, expected", [
        (100, 50.0),
        (500, 50.0),
        (1000, 50.0),
        (1001, 100.0),
        (10000, 100.0),
        (20000, 100.0),
        (20001, 400.01),
        (30000, 500.0),
        (40000, 600.0),
        (40001, 500.0),
        (45000, 500.0),
        (50000, 500.0),
    ])
    def test_commission_calculation_valid(self, amount, expected):
        assert calculate_commission(amount) == expected

    @pytest.mark.parametrize("amount, expected", [
        (100, 50.0),
        (1000, 50.0),
        (1001, 100.0),
        (20000, 100.0),
        (20001, 400.01),
        (40000, 600.0),
        (40001, 500.0),
        (50000, 500.0),
    ])
    def test_commission_boundary_values(self, amount, expected):
        assert calculate_commission(amount) == expected

    @pytest.mark.parametrize("invalid_amount", [
        99,
        0,
        -1,
        -100,
        50001,
        100000,
    ])
    def test_commission_invalid_amount_raises_value_error(self, invalid_amount):
        with pytest.raises(ValueError):
            calculate_commission(invalid_amount)

    @pytest.mark.parametrize("invalid_type", [
        "abc",
        "100",
        None,
        [100],
        {"amount": 100},
    ])
    def test_commission_invalid_type_raises_type_error(self, invalid_type):
        with pytest.raises(TypeError):
            calculate_commission(invalid_type)

    @pytest.mark.parametrize("amount", [
        40001,
        41000,
        42500,
        49999,
        50000,
    ])
    def test_fixed_commission_for_high_amounts(self, amount):
        assert calculate_commission(amount) == 500.0

    def test_new_rule_boundary_40000(self):
        assert calculate_commission(40000) == 600.0
        assert calculate_commission(40001) == 500.0

    def test_commission_is_monotonic_up_to_40000(self):
        amounts = [20001, 25000, 30000, 35000, 40000]
        commissions = [calculate_commission(a) for a in amounts]
        for i in range(len(commissions) - 1):
            assert commissions[i] < commissions[i + 1]

    def test_commission_returns_float(self):
        for amount in [100, 1001, 20001, 40001, 50000]:
            assert isinstance(calculate_commission(amount), float)

    def test_commission_for_max_amount(self):
        assert calculate_commission(50000) == 500.0

    def test_commission_for_min_amount(self):
        assert calculate_commission(100) == 50.0