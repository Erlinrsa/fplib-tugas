"""Aplikasi 3: Perpustakaan Mini - katalog, peminjaman, denda."""
from fplib import (
    add_item, compose, filter_list, find_first, flatten, format_rupiah,
    format_table, group_by, map_list, max_by, rank_by, remove_where,
    sort_by, sum_by, take, update_where, count_by, pluck,
)

RAK = [
    [{"id": 1, "judul": "Struktur Data", "stok": 2},
     {"id": 2, "judul": "Basis Data", "stok": 1}],
    [{"id": 3, "judul": "Pemrograman Fungsional", "stok": 3},
     {"id": 4, "judul": "Jaringan Komputer", "stok": 0}],
]
KATALOG = flatten(RAK)

BATAS_HARI = 7
DENDA_PER_HARI = 1000


def _ubah_stok(katalog, id_buku, delta):
    return update_where(lambda b: b["id"] == id_buku,
                        lambda b: {**b, "stok": b["stok"] + delta}, katalog)


def pinjam(katalog, peminjaman, id_buku, nama, lama):
    buku = find_first(lambda b: b["id"] == id_buku, katalog)
    if buku is None or buku["stok"] == 0:
        return katalog, peminjaman
    return (_ubah_stok(katalog, id_buku, -1),
            add_item(peminjaman, {"id_buku": id_buku, "peminjam": nama, "lama": lama}))


def kembalikan(katalog, peminjaman, id_buku, nama):
    sisa = remove_where(lambda p: p["id_buku"] == id_buku and p["peminjam"] == nama, peminjaman)
    return _ubah_stok(katalog, id_buku, +1), sisa


def denda(p):
    return max(0, p["lama"] - BATAS_HARI) * DENDA_PER_HARI


total_denda_rupiah = compose(format_rupiah, lambda ps: sum_by(denda, ps))


def main():
    katalog, pjm = KATALOG, []
    transaksi = [(1, "Ayu", 5), (2, "Ayu", 10), (3, "Budi", 12), (1, "Citra", 3),
                 (3, "Citra", 9), (4, "Budi", 2)]  # buku 4 stok 0 -> ditolak
    for id_buku, nama, lama in transaksi:
        katalog, pjm = pinjam(katalog, pjm, id_buku, nama, lama)
    katalog, pjm = kembalikan(katalog, pjm, 1, "Citra")

    print("=== PERPUSTAKAAN MINI ===")
    print(format_table(["ID", "Judul", "Stok"],
                       [[b["id"], b["judul"], b["stok"]] for b in sort_by(lambda b: b["id"], katalog)]))
    telat = filter_list(lambda p: denda(p) > 0, pjm)
    print("\nPeminjaman aktif:", len(pjm), "| terlambat:", len(telat))
    per_orang = group_by(lambda p: p["peminjam"], pjm)
    rekap = map_list(lambda kv: {"peminjam": kv[0], "buku": len(kv[1]),
                                 "denda": sum_by(denda, kv[1])}, per_orang.items())
    ranked = rank_by(lambda r: r["denda"], rekap)
    print(format_table(["Peringkat", "Peminjam", "Buku", "Denda"],
                       [[r["peringkat"], r["peminjam"], r["buku"], format_rupiah(r["denda"])] for r in ranked]))
    print("Denda 2 teratas :", ", ".join(pluck("peminjam", take(2, ranked))))
    populer = max_by(lambda kv: kv[1], count_by(lambda p: p["id_buku"], pjm).items())
    print("Buku terpopuler : ID", populer[0], f"({populer[1]}x dipinjam)")
    print("Total denda     :", total_denda_rupiah(pjm))


if __name__ == "__main__":
    main()
