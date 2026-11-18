# Satu Library, Lima Aplikasi (Pemrograman Fungsional)

`fplib.py` adalah satu file library berisi fungsi umum bergaya fungsional
(pure function, tanpa efek samping, tanpa mutasi data). Library ini dipakai
oleh lima aplikasi; **setiap fungsi dipakai oleh minimal 3 dari 5 aplikasi.**

## Struktur

| File | Keterangan |
|------|------------|
| `fplib.py` | Library fungsi umum |
| `test_fplib.py` | Unit test (pytest) |
| `kasir_kantin.py` | Aplikasi 1: menu, keranjang, total belanja |
| `presensi_kelas.py` | Aplikasi 2: kehadiran dan rekap per mahasiswa |
| `perpustakaan_mini.py` | Aplikasi 3: katalog, peminjaman, denda |
| `keuangan_pribadi.py` | Aplikasi 4: pemasukan, pengeluaran, kategori |
| `nilai_mahasiswa.py` | Aplikasi 5: komponen nilai, nilai akhir, peringkat |

## Cara pakai

Butuh Python 3.8+ dan pytest (`pip install pytest`).

```bash
python kasir_kantin.py
python presensi_kelas.py
python perpustakaan_mini.py
python keuangan_pribadi.py
python nilai_mahasiswa.py
pytest -v
```

## Daftar fungsi `fplib.py`

**Komposisi**
- `compose(*fns)`: gabung fungsi, dieksekusi kanan ke kiri
- `pipe(value, *fns)`: alirkan nilai lewat fungsi, kiri ke kanan

**Transformasi koleksi**
- `map_list(f, xs)`, `filter_list(pred, xs)`, `reduce_list(f, xs, init)`
- `flatten(xss)`: ratakan list of list
- `partition(pred, xs)`: pisah jadi (memenuhi, tidak memenuhi)
- `pluck(key, xs)`: ambil satu field dari tiap dict
- `take(n, xs)`: n elemen pertama

**Pencarian dan pembaruan immutable**
- `find_first(pred, xs, default=None)`
- `add_item(xs, item)`, `update_where(pred, f, xs)`, `remove_where(pred, xs)`

**Agregasi**
- `sum_by(key, xs)`, `avg(xs)`, `percent(part, whole)`
- `group_by(key, xs)`, `count_by(key, xs)`, `max_by(key, xs)`

**Pengurutan dan peringkat**
- `sort_by(key, xs, reverse=False)`
- `rank_by(key, xs)`: urut menurun + field `peringkat` (nilai sama, peringkat sama)

**Format tampilan**
- `format_rupiah(n)`: `12500` menjadi `Rp 12.500`
- `format_table(headers, rows)`: tabel teks
