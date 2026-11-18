"""Aplikasi 5: Nilai Mahasiswa - komponen nilai, nilai akhir, peringkat."""
from fplib import (
    avg, compose, count_by, filter_list, find_first, flatten, format_table,
    group_by, map_list, max_by, partition, percent, pipe, pluck, rank_by,
    reduce_list, take, update_where,
)

MAHASISWA = [
    {"nim": "101", "nama": "Ayu", "tugas": [90, 85, 95], "uts": 80, "uas": 88},
    {"nim": "102", "nama": "Budi", "tugas": [70, 65, 75], "uts": 60, "uas": 45},
    {"nim": "103", "nama": "Citra", "tugas": [85, 90, 80], "uts": 75, "uas": 82},
    {"nim": "104", "nama": "Dimas", "tugas": [60, 70, 65], "uts": 55, "uas": 40},
    {"nim": "105", "nama": "Eka", "tugas": [95, 92, 98], "uts": 90, "uas": 94},
]


def grade(nilai):
    return "A" if nilai >= 85 else "B" if nilai >= 70 else "C" if nilai >= 60 else "D" if nilai >= 50 else "E"


def _tambah_akhir(m):
    return {**m, "akhir": round(0.3 * avg(m["tugas"]) + 0.3 * m["uts"] + 0.4 * m["uas"], 1)}


def _tambah_grade(m):
    return {**m, "grade": grade(m["akhir"])}


# compose bekerja kanan -> kiri: hitung nilai akhir dulu, lalu grade
hitung_nilai = compose(_tambah_grade, _tambah_akhir)


def remedial(mhs, batas=50):
    """UAS di bawah batas diganti nilai remedial = batas."""
    return update_where(lambda m: m["uas"] < batas, lambda m: {**m, "uas": batas}, mhs)


def main():
    print("=== NILAI MAHASISWA ===")
    hasil = map_list(hitung_nilai, MAHASISWA)
    ranked = rank_by(lambda m: m["akhir"], hasil)
    print(format_table(["Rank", "NIM", "Nama", "Akhir", "Grade"],
                       [[m["peringkat"], m["nim"], m["nama"], m["akhir"], m["grade"]] for m in ranked]))
    print("\nTop 3        :", ", ".join(pluck("nama", take(3, ranked))))
    print("Sebaran grade:", count_by(lambda m: m["grade"], hasil))
    lulus, tidak = partition(lambda m: m["akhir"] >= 60, hasil)
    print(f"Kelulusan    : {len(lulus)}/{len(hasil)} ({percent(len(lulus), len(hasil))}%)")
    rata = reduce_list(lambda acc, m: acc + m["akhir"], hasil, 0) / len(hasil)
    print("Rata-rata    :", round(rata, 1))
    print("Rata tugas   :", round(avg(flatten(pluck("tugas", MAHASISWA))), 1))
    terbaik = max_by(lambda m: max(m["tugas"]), hasil)
    print("Tugas tertinggi:", terbaik["nama"], max(terbaik["tugas"]))
    print("Daftar per grade:",
          {g: pluck("nama", ms) for g, ms in group_by(lambda m: m["grade"], hasil).items()})

    # Remedial untuk yang UAS < 50, lalu hitung ulang
    ulang = pipe(MAHASISWA, remedial, lambda ms: map_list(hitung_nilai, ms))
    budi = find_first(lambda m: m["nama"] == "Budi", ulang)
    print("Budi setelah remedial:", budi["akhir"], budi["grade"])
    masih = filter_list(lambda m: m["akhir"] < 60, ulang)
    print("Belum lulus setelah remedial:", ", ".join(pluck("nama", masih)) or "-")


if __name__ == "__main__":
    main()
