import pytest
from fplib import (
    add_item, avg, compose, count_by, filter_list, find_first, flatten,
    format_rupiah, format_table, group_by, map_list, max_by, partition,
    percent, pipe, pluck, rank_by, reduce_list, remove_where, sort_by,
    sum_by, take, update_where,
)


def test_compose_kanan_ke_kiri():
    assert compose(lambda x: x + 1, lambda x: x * 2)(5) == 11


def test_pipe_kiri_ke_kanan():
    assert pipe(5, lambda x: x * 2, lambda x: x + 1) == 11


def test_map_filter_reduce():
    assert map_list(lambda x: x * 2, [1, 2, 3]) == [2, 4, 6]
    assert filter_list(lambda x: x > 1, [1, 2, 3]) == [2, 3]
    assert reduce_list(lambda a, x: a + x, [1, 2, 3], 10) == 16


def test_flatten_partition_pluck_take():
    assert flatten([[1], [2, 3], []]) == [1, 2, 3]
    assert partition(lambda x: x % 2 == 0, [1, 2, 3, 4]) == ([2, 4], [1, 3])
    assert pluck("a", [{"a": 1}, {"a": 2}]) == [1, 2]
    assert take(2, [1, 2, 3]) == [1, 2]
    assert take(5, [1]) == [1]


def test_find_first():
    assert find_first(lambda x: x > 1, [1, 2, 3]) == 2
    assert find_first(lambda x: x > 9, [1, 2], default="none") == "none"


def test_add_update_remove_tidak_mutasi():
    asli = [{"id": 1, "v": 1}, {"id": 2, "v": 2}]
    baru = add_item(asli, {"id": 3, "v": 3})
    assert len(asli) == 2 and len(baru) == 3
    upd = update_where(lambda d: d["id"] == 1, lambda d: {**d, "v": 99}, asli)
    assert upd[0]["v"] == 99 and asli[0]["v"] == 1
    assert remove_where(lambda d: d["id"] == 1, asli) == [{"id": 2, "v": 2}]
    assert len(asli) == 2


def test_sum_avg_percent():
    assert sum_by(lambda x: x["n"], [{"n": 2}, {"n": 3}]) == 5
    assert sum_by(lambda x: x, []) == 0
    assert avg([2, 4]) == 3 and avg([]) == 0
    assert percent(1, 3) == 33.3 and percent(1, 0) == 0.0


def test_group_count_max():
    xs = ["a", "bb", "cc", "d"]
    assert group_by(len, xs) == {1: ["a", "d"], 2: ["bb", "cc"]}
    assert count_by(len, xs) == {1: 2, 2: 2}
    assert max_by(len, xs) == "bb"
    assert max_by(len, [], default=None) is None


def test_sort_by_tidak_mutasi():
    xs = [3, 1, 2]
    assert sort_by(lambda x: x, xs) == [1, 2, 3]
    assert sort_by(lambda x: x, xs, reverse=True) == [3, 2, 1]
    assert xs == [3, 1, 2]


def test_rank_by_dengan_seri():
    data = [{"n": "a", "s": 90}, {"n": "b", "s": 80}, {"n": "c", "s": 80}, {"n": "d", "s": 70}]
    hasil = rank_by(lambda x: x["s"], data)
    assert [r["peringkat"] for r in hasil] == [1, 2, 2, 4]
    assert "peringkat" not in data[0]


def test_format_rupiah():
    assert format_rupiah(12500) == "Rp 12.500"
    assert format_rupiah(1000000) == "Rp 1.000.000"
    assert format_rupiah(0) == "Rp 0"


def test_format_table():
    out = format_table(["A", "Bb"], [[1, "x"], [22, "yyy"]])
    baris = out.split("\n")
    assert len(baris) == 4
    assert baris[0].startswith("A ")
    assert "yyy" in baris[3]
    assert format_table(["A"], []).split("\n")[0] == "A"
