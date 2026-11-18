"""Aplikasi 1: Kasir Kantin - menu, keranjang, total belanja."""
from fplib import (
    add_item, compose, filter_list, find_first, format_rupiah, format_table,
    group_by, map_list, pipe, pluck, remove_where, sort_by, sum_by,
)

MENU = [
    {"id": 1, "nama": "Nasi Goreng", "harga": 15000, "kategori": "makanan"},
    {"id": 2, "nama": "Mie Ayam", "harga": 13000, "kategori": "makanan"},
    {"id": 3, "nama": "Es Teh", "harga": 4000, "kategori": "minuman"},
    {"id": 4, "nama": "Jus Jeruk", "harga": 8000, "kategori": "minuman"},
    {"id": 5, "nama": "Gorengan", "harga": 2000, "kategori": "snack"},
]


def tambah(keranjang, id_menu, qty):
    return add_item(keranjang, {"id": id_menu, "qty": qty})


def batalkan(keranjang, id_menu):
    return remove_where(lambda k: k["id"] == id_menu, keranjang)


def detail(keranjang):
    def ke_baris(k):
        m = find_first(lambda x: x["id"] == k["id"], MENU)
        return {"nama": m["nama"], "kategori": m["kategori"], "qty": k["qty"],
                "subtotal": m["harga"] * k["qty"]}
    return map_list(ke_baris, keranjang)


def diskon(total):
    """Diskon 10% untuk belanja >= Rp 50.000."""
    return total * 0.9 if total >= 50000 else total


hitung_total = compose(round, diskon, lambda rows: sum_by(lambda r: r["subtotal"], rows))


def main():
    keranjang = pipe(
        [],
        lambda k: tambah(k, 1, 2),
        lambda k: tambah(k, 3, 2),
        lambda k: tambah(k, 5, 5),
        lambda k: tambah(k, 2, 1),
        lambda k: tambah(k, 4, 1),
        lambda k: batalkan(k, 4),
    )
    rows = sort_by(lambda r: r["subtotal"], detail(keranjang), reverse=True)
    print("=== KASIR KANTIN ===")
    print(format_table(["Item", "Qty", "Subtotal"],
                       [[r["nama"], r["qty"], format_rupiah(r["subtotal"])] for r in rows]))
    print("\nPer kategori:")
    for kat, items in group_by(lambda r: r["kategori"], rows).items():
        print(f"  {kat:<8}: {format_rupiah(sum_by(lambda r: r['subtotal'], items))}")
    makanan = filter_list(lambda r: r["kategori"] == "makanan", rows)
    print("Makanan dipesan:", ", ".join(pluck("nama", makanan)))
    print("TOTAL (setelah diskon):", format_rupiah(hitung_total(rows)))


if __name__ == "__main__":
    main()
