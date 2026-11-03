import pytest
from credit_card_rewards import reward_points, late_payment_fee, card_status

# Test cases written so that every decision in credit_card_rewards.py
# evaluates to both True and False, including boundary values and
# each part of the compound (and / or) conditions.


# ---------- reward_points ----------

# card_tier not in POINTS_PER_100 -> True / False
def test_unknown_card_tier_raises():
    with pytest.raises(ValueError, match="unknown card tier"):
        reward_points("silver", 1000, "grocery", False)


def test_valid_tier_classic():
    assert reward_points("classic", 1000, "grocery", False) == 10


# amount <= 0 -> True (zero and negative) / False
def test_zero_amount_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("gold", 0, "grocery", False)


def test_negative_amount_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("gold", -100, "grocery", False)


def test_smallest_valid_amount():
    # 1 // 100 = 0 points
    assert reward_points("gold", 1, "grocery", False) == 0


# category == "fuel" -> True / False
def test_fuel_gives_zero_points():
    assert reward_points("platinum", 5000, "fuel", True) == 0


# category == "dining" or category == "travel"
def test_dining_doubles_points():
    assert reward_points("classic", 1000, "dining", False) == 20


def test_travel_doubles_points():
    assert reward_points("classic", 1000, "travel", False) == 20


def test_other_category_not_doubled():
    assert reward_points("classic", 1000, "shopping", False) == 10


# is_weekend and card_tier != "classic"
def test_weekend_gold_gets_bonus():
    assert reward_points("gold", 1000, "grocery", True) == 70


def test_weekend_platinum_travel_gets_bonus():
    # 1000 // 100 * 4 = 40, doubled = 80, +50 = 130
    assert reward_points("platinum", 1000, "travel", True) == 130


def test_weekend_classic_no_bonus():
    assert reward_points("classic", 1000, "grocery", True) == 10


def test_weekday_gold_no_bonus():
    assert reward_points("gold", 1000, "grocery", False) == 20


def test_amount_not_multiple_of_100():
    # 250 // 100 = 2 -> 2 * 4 = 8
    assert reward_points("platinum", 250, "grocery", False) == 8


# ---------- late_payment_fee ----------

# days_late <= 0 or outstanding <= 0
def test_paid_on_time():
    assert late_payment_fee(5000, 0) == 0


def test_negative_days_late():
    assert late_payment_fee(5000, -2) == 0


def test_zero_outstanding():
    assert late_payment_fee(0, 10) == 0


def test_negative_outstanding():
    assert late_payment_fee(-500, 10) == 0


# outstanding <= 1000 / <= 10000 / else, with boundaries
def test_small_outstanding_fee():
    assert late_payment_fee(500, 5) == 100


def test_outstanding_exactly_1000():
    assert late_payment_fee(1000, 5) == 100


def test_outstanding_just_above_1000():
    assert late_payment_fee(1001, 5) == 500


def test_outstanding_exactly_10000():
    assert late_payment_fee(10000, 5) == 500


def test_outstanding_just_above_10000():
    assert late_payment_fee(10001, 5) == 1000


# days_late > 30 -> True / False, with boundaries
def test_exactly_30_days_late_no_extra():
    assert late_payment_fee(20000, 30) == 1000


def test_31_days_late_extra_fee():
    assert late_payment_fee(20000, 31) == 1750


def test_small_outstanding_very_late():
    assert late_payment_fee(500, 45) == 850


def test_medium_outstanding_very_late():
    assert late_payment_fee(5000, 60) == 1250


def test_one_day_late_one_rupee():
    assert late_payment_fee(1, 1) == 100


# ---------- card_status ----------

# is_frozen -> True / False (frozen wins over everything else)
def test_frozen_card():
    assert card_status(50, 0, True) == "frozen"


def test_frozen_overrides_blocked():
    assert card_status(95, 5, True) == "frozen"


# missed_payments >= 3, with boundary
def test_blocked_card():
    assert card_status(50, 3, False) == "blocked"


def test_blocked_overrides_over_limit():
    assert card_status(95, 4, False) == "blocked"


def test_two_missed_payments_not_blocked():
    assert card_status(10, 2, False) == "watch"


# utilisation_percent > 90, with boundary
def test_over_limit_risk():
    assert card_status(95, 0, False) == "over limit risk"


def test_utilisation_exactly_90_is_watch():
    assert card_status(90, 0, False) == "watch"


def test_utilisation_91_over_limit():
    assert card_status(91, 0, False) == "over limit risk"


# utilisation_percent > 30 or missed_payments > 0
def test_watch_high_utilisation():
    assert card_status(50, 0, False) == "watch"


def test_watch_due_to_missed_payment_only():
    assert card_status(10, 1, False) == "watch"


def test_utilisation_exactly_30_is_good():
    assert card_status(30, 0, False) == "good"


def test_utilisation_31_is_watch():
    assert card_status(31, 0, False) == "watch"


def test_good_status():
    assert card_status(10, 0, False) == "good"


def test_zero_utilisation_good():
    assert card_status(0, 0, False) == "good"
