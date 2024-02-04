import typing

import pytest

from .banner_engine import (
    BannerStat, Banner, BannerStorage, EmptyBannerStorageError, EpsilonGreedyBannerEngine
)

TEST_DEFAULT_CTR = 0.1


@pytest.fixture(scope="function")
def test_banners() -> list[Banner]:
    return [
        Banner("b1", cost=1, stat=BannerStat(10, 20)),
        Banner("b2", cost=250, stat=BannerStat(20, 20)),
        Banner("b3", cost=100, stat=BannerStat(0, 20)),
        Banner("b4", cost=100, stat=BannerStat(1, 20)),
    ]


@pytest.mark.parametrize("clicks, shows, expected_ctr", [(1, 1, 1.0), (20, 100, 0.2), (5, 100, 0.05)])
def test_banner_stat_ctr_value(clicks: int, shows: int, expected_ctr: float) -> None:
    assert BannerStat(clicks, shows).compute_ctr(TEST_DEFAULT_CTR) == expected_ctr


def test_empty_stat_compute_ctr_returns_default_ctr() -> None:
    assert BannerStat(0, 0).compute_ctr(TEST_DEFAULT_CTR) == TEST_DEFAULT_CTR


def test_banner_stat_add_show_lowers_ctr() -> None:
    a = BannerStat(1, 1)
    b = BannerStat(1, 1)
    a.add_show()
    assert a.compute_ctr(TEST_DEFAULT_CTR) < b.compute_ctr(TEST_DEFAULT_CTR)


def test_banner_stat_add_click_increases_ctr() -> None:
    a = BannerStat(1, 1)
    b = BannerStat(1, 1)
    a.add_click()
    assert a.compute_ctr(TEST_DEFAULT_CTR) > b.compute_ctr(TEST_DEFAULT_CTR)


def test_get_banner_with_highest_cpc_returns_banner_with_highest_cpc(test_banners: list[Banner]) -> None:
    bs = BannerStorage(test_banners)
    hg = bs.banner_with_highest_cpc()
    x = TEST_DEFAULT_CTR
    for i in test_banners:
        a = i.stat.compute_ctr(TEST_DEFAULT_CTR)
        if a > x:
            x = a
            h = i.banner_id
    assert hg == bs.get_banner(h)


def test_banner_engine_raise_empty_storage_exception_if_constructed_with_empty_storage() -> None:
    bs = BannerStorage([], TEST_DEFAULT_CTR)
    with pytest.raises(EmptyBannerStorageError):
        EpsilonGreedyBannerEngine(bs, 0.0)


def test_engine_send_click_not_fails_on_unknown_banner(test_banners: list[Banner]) -> None:
    eg = EpsilonGreedyBannerEngine(BannerStorage(test_banners, TEST_DEFAULT_CTR), 0.0)
    eg.send_click("228")


def test_engine_with_zero_random_probability_shows_banner_with_highest_cpc(test_banners: list[Banner]) -> None:
    bs = BannerStorage(test_banners, TEST_DEFAULT_CTR)
    eg = EpsilonGreedyBannerEngine(bs, 0.0)
    assert eg.show_banner() == bs.banner_with_highest_cpc().banner_id


@pytest.mark.parametrize("expected_random_banner", ["b1", "b2", "b3", "b4"])
def test_engine_with_1_random_banner_probability_gets_random_banner(
        expected_random_banner: str,
        test_banners: list[Banner],
        monkeypatch: typing.Any
) -> None:
    monkeypatch.setattr("random.choice", lambda x: expected_random_banner)
    eg = EpsilonGreedyBannerEngine(BannerStorage(test_banners, TEST_DEFAULT_CTR), 1.0)
    assert eg.show_banner() == expected_random_banner


def test_total_cost_equals_to_cost_of_clicked_banners(test_banners: list[Banner]) -> None:
    ttl = 0
    eg = EpsilonGreedyBannerEngine(BannerStorage(test_banners, TEST_DEFAULT_CTR), 0.0)
    for i in test_banners:
        ttl += i.cost
        eg.send_click(i.banner_id)
    assert ttl == eg.total_cost


def test_engine_show_increases_banner_show_stat(test_banners: list[Banner]) -> None:
    bs = BannerStorage(test_banners, TEST_DEFAULT_CTR)
    eg = EpsilonGreedyBannerEngine(bs, 0.0)
    pr = bs.banner_with_highest_cpc()
    a = pr.stat.shows
    eg.show_banner()
    assert bs.banner_with_highest_cpc().stat.shows > a


def test_engine_click_increases_banner_click_stat(test_banners: list[Banner]) -> None:
    eg = EpsilonGreedyBannerEngine(BannerStorage(test_banners, TEST_DEFAULT_CTR), 0.0)
    for i in test_banners:
        a = i.stat.clicks
        eg.send_click(i.banner_id)
        assert i.stat.clicks > a
