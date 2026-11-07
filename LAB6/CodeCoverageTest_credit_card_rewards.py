import pytest
from credit_card_rewards import reward_points, late_payment_fee, card_status

# Test cases written to execute every line (statement) of credit_card_rewards.py


# ---------- reward_points ----------

def test_classic_grocery():
    assert reward_points("classic", 1000, "grocery", False) == 10


def test_unknown_card_tier_raises():
    with pytest.raises(ValueError, match="unknown card tier"):
        reward_points("silver", 1000, "grocery", False)


def test_invalid_amount_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("gold", 0, "grocery", False)


def test_fuel_gives_zero_points():
    assert reward_points("platinum", 5000, "fuel", True) == 0


def test_gold_dining_weekend():
    # 1000 // 100 * 2 = 20, doubled for dining = 40, +50 weekend bonus = 90
    assert reward_points("gold", 1000, "dining", True) == 90


# ---------- late_payment_fee ----------

def test_paid_on_time():
    assert late_payment_fee(5000, 0) == 0


def test_small_outstanding_fee():
    assert late_payment_fee(500, 5) == 100


def test_medium_outstanding_fee():
    assert late_payment_fee(5000, 5) == 500


def test_large_outstanding_very_late_fee():
    # 1000 base fee + 750 for more than 30 days late
    assert late_payment_fee(20000, 40) == 1750


# ---------- card_status ----------

def test_frozen_card():
    assert card_status(50, 0, True) == "frozen"


def test_blocked_card():
    assert card_status(50, 3, False) == "blocked"


def test_over_limit_risk():
    assert card_status(95, 0, False) == "over limit risk"


def test_watch_status():
    assert card_status(50, 0, False) == "watch"


def test_good_status():
    assert card_status(10, 0, False) == "good"
