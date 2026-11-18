"""Aplikasi 4: Keuangan Pribadi - pemasukan, pengeluaran, kategori."""
from fplib import (
    add_item, avg, count_by, filter_list, flatten, format_rupiah, format_table,
    group_by, map_list, max_by, partition, percent, pipe, pluck, reduce_list,
    remove_where, sort_by, sum_by, take,
)

# Transaksi dikelompokkan per minggu
MINGGU = [
    [{"jenis": "masuk", "kategori": "gaji", "jumlah": 3000000},
     {"jenis": "keluar", "kategori": "makan", "jumlah": 150000},
     {"jenis": "keluar", "kategori": "transport", "jumlah": 50000}],
    [{"jenis": "keluar", "kategori": "makan", "jumlah": 200000},
     {"jenis": "keluar", "kategori": "hiburan", "jumlah": 120000},
     {"jenis": "keluar", "kategori": "makan", "jumlah": 0}],   # salah input
    [{"jenis": "masuk", "kategori": "freelance", "jumlah": 500000},
     {"jenis": "keluar", "kategori": "transport", "jumlah": 80000},
     {"jenis": "keluar", "kategori": "tagihan", "jumlah": 300000}],
]


def saldo_berjalan(transaksi):
    def step(acc, t):
        delta = t["jumlah"] if t["jenis"] == "masuk" else -t["jumlah"]
        return add_item(acc, (acc[-1] if acc else 0) + delta)
    return reduce_list(step, transaksi, [])


def main():
    semua = pipe(flatten(MINGGU), lambda ts: remove_where(lambda t: t["jumlah"] <= 0, ts))
    masuk, keluar = partition(lambda t: t["jenis"] == "masuk", semua)
    total_masuk = sum_by(lambda t: t["jumlah"], masuk)
    total_keluar = sum_by(lambda t: t["jumlah"], keluar)

    print("=== KEUANGAN PRIBADI ===")
    print("Pemasukan  :", format_rupiah(total_masuk))
    print("Pengeluaran:", format_rupiah(total_keluar))
    print("Saldo akhir:", format_rupiah(saldo_berjalan(semua)[-1]))

    per_kat = map_list(
        lambda kv: {"kategori": kv[0], "total": sum_by(lambda t: t["jumlah"], kv[1])},
        group_by(lambda t: t["kategori"], keluar).items())
    urut = sort_by(lambda r: r["total"], per_kat, reverse=True)
    print("\nPengeluaran per kategori:")
    print(format_table(["Kategori", "Total", "Porsi"],
                       [[r["kategori"], format_rupiah(r["total"]),
                         f"{percent(r['total'], total_keluar)}%"] for r in urut]))
    print("3 terbesar        :", ", ".join(pluck("kategori", take(3, urut))))
    print("Transaksi terbesar:", max_by(lambda t: t["jumlah"], keluar)["kategori"])
    print("Rata-rata keluar  :", format_rupiah(round(avg(pluck("jumlah", keluar)))))
    print("Frekuensi         :", count_by(lambda t: t["kategori"], keluar))
    besar = filter_list(lambda t: t["jumlah"] >= 200000, keluar)
    print("Pengeluaran >= 200rb:", len(besar), "transaksi")


if __name__ == "__main__":
    main()
