"""Aplikasi 2: Presensi Kelas - kehadiran dan rekap per mahasiswa."""
from fplib import (
    avg, count_by, filter_list, find_first, flatten, format_table, group_by,
    map_list, partition, percent, pipe, pluck, rank_by, reduce_list,
    sort_by, update_where,
)

MAHASISWA = [
    {"nim": "001", "nama": "Ayu"},
    {"nim": "002", "nama": "Budi"},
    {"nim": "003", "nama": "Citra"},
    {"nim": "004", "nama": "Dimas"},
]

# Satu list per pertemuan; isi: (nim, status) H=Hadir I=Izin S=Sakit A=Alfa
PERTEMUAN = [
    [("001", "H"), ("002", "H"), ("003", "H"), ("004", "A")],
    [("001", "H"), ("002", "S"), ("003", "H"), ("004", "H")],
    [("001", "H"), ("002", "H"), ("003", "A"), ("004", "A")],
    [("001", "H"), ("002", "H"), ("003", "H"), ("004", "I")],
]


def buat_catatan(pertemuan):
    return flatten(map_list(
        lambda p: map_list(lambda t: {"pertemuan": p[0] + 1, "nim": t[0], "status": t[1]}, p[1]),
        enumerate(pertemuan)))


def koreksi(catatan, nim, pertemuan, status_baru):
    return update_where(
        lambda r: r["nim"] == nim and r["pertemuan"] == pertemuan,
        lambda r: {**r, "status": status_baru}, catatan)


def rekap_mhs(catatan, m):
    milik = filter_list(lambda r: r["nim"] == m["nim"], catatan)
    hadir = reduce_list(lambda acc, r: acc + (r["status"] == "H"), milik, 0)
    return {"nim": m["nim"], "nama": m["nama"], "hadir": hadir,
            "total": len(milik), "persen": percent(hadir, len(milik))}


def main():
    catatan = pipe(PERTEMUAN, buat_catatan, lambda c: koreksi(c, "004", 4, "H"))
    rekap = map_list(lambda m: rekap_mhs(catatan, m), MAHASISWA)
    ranked = rank_by(lambda r: r["persen"], rekap)
    print("=== PRESENSI KELAS ===")
    print(format_table(["Peringkat", "Nama", "Hadir", "Persen"],
                       [[r["peringkat"], r["nama"], f"{r['hadir']}/{r['total']}", f"{r['persen']}%"]
                        for r in ranked]))
    lolos, tidak = partition(lambda r: r["persen"] >= 75, rekap)
    print("\nMemenuhi syarat 75%:", ", ".join(pluck("nama", lolos)) or "-")
    print("Tidak memenuhi     :", ", ".join(pluck("nama", tidak)) or "-")
    print("Rata-rata kehadiran:", round(avg(pluck("persen", rekap)), 1), "%")
    print("Rekap status       :", count_by(lambda r: r["status"], catatan))
    per_pert = group_by(lambda r: r["pertemuan"], catatan)
    for p, rs in sort_by(lambda kv: kv[0], per_pert.items()):
        print(f"  Pertemuan {p}: hadir {len(filter_list(lambda r: r['status'] == 'H', rs))}/{len(rs)}")
    budi = find_first(lambda m: m["nama"] == "Budi", MAHASISWA)
    print("Detail Budi        :", rekap_mhs(catatan, budi))


if __name__ == "__main__":
    main()
