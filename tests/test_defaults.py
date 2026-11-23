from generator.generation import defaults


def test_every_hero_has_winrate_bonus():
    assert set(defaults.HERO_WINRATE_BONUS) == set(defaults.HERO_ARCHETYPE)


def test_winrate_bonuses_are_reasonable_and_centered():
    values = defaults.HERO_WINRATE_BONUS.values()
    assert all(-0.15 <= v <= 0.15 for v in values)
    # центрировано на среднее по мете -> сумма близка к нулю
    assert abs(sum(values)) < 0.1


def test_country_regions_match_mmr_regions():
    assert set(defaults.COUNTRY_WEIGHTS_BY_REGION) == set(defaults.REGION_MMR_MEAN)


def test_country_weights_are_positive():
    for weights in defaults.COUNTRY_WEIGHTS_BY_REGION.values():
        assert weights
        assert all(w > 0 for w in weights.values())
