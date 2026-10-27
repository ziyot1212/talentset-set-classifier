import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_report():
    doc = Document()

    # =========================================================================
    # 1. PENGATURAN KERTAS & MARGIN (Standar Akademik: Kiri 4cm, Lainnya 3cm)
    # =========================================================================
    for section in doc.sections:
        section.page_width = Cm(21.0)   # A4 Width
        section.page_height = Cm(29.7)  # A4 Height
        section.left_margin = Cm(4.0)   # Kiri 4 cm
        section.right_margin = Cm(3.0)  # Kanan 3 cm
        section.top_margin = Cm(3.0)    # Atas 3 cm
        section.bottom_margin = Cm(3.0) # Bawah 3 cm

    # =========================================================================
    # 2. PENGATURAN GAYA TIPOGRAFI KLASIK (Times New Roman)
    # =========================================================================
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(15, 23, 42)
    p_format = style.paragraph_format
    p_format.line_spacing = 1.5
    p_format.space_after = Pt(4)

    # Helper styling background tabel
    def set_cell_background(cell, hex_color):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    # Helper placeholder gambar
    def add_screenshot_box(doc, caption, dimension_hint):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Cm(14.0)
        set_cell_background(cell, "F1F5F9")
        
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p.add_run(f"\n[TEMPAT MENEMPELKAN SCREENSHOT]\n{caption}\n")
        r1.bold = True
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = RGBColor(51, 65, 85)

        r2 = p.add_run(f"Panduan Ukuran: {dimension_hint}\n(Hapus kotak teks ini di Microsoft Word, lalu pilih Insert > Pictures)\n")
        r2.italic = True
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = RGBColor(100, 116, 139)

        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        c_run = cp.add_run(caption)
        c_run.bold = True
        c_run.font.name = 'Times New Roman'
        c_run.font.size = Pt(10)
        c_run.font.color.rgb = RGBColor(30, 41, 59)

    # =========================================================================
    # HALAMAN 1: IDENTITAS, ABSTRAK, & BAB I PENDAHULUAN
    # =========================================================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("LAPORAN PROYEK BERBASIS MASALAH (PJBL-2)\n")
    r_t1.bold = True
    r_t1.font.size = Pt(13)
    r_t2 = p_title.add_run("SISTEM KLASIFIKASI DATA CALON ASISTEN LABORATORIUM BERBASIS TEORI HIMPUNAN DISKRIT (TALENTSET)\n")
    r_t2.bold = True
    r_t2.font.size = Pt(12)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.line_spacing = 1.15
    r_meta = p_meta.add_run(
        "Mata Kuliah: Matematika Diskrit / Struktur Diskrit\n"
        "Disusun Oleh: Kelompok [Isi Nomor Kelompok]\n"
        "1. [Nama Anggota 1] ([NIM 1]) – Project Lead\n"
        "2. [Nama Anggota 2] ([NIM 2]) – Set Engine Engineer\n"
        "3. [Nama Anggota 3] ([NIM 3]) – UI/UX & Visualization\n"
        "4. [Nama Anggota 4] ([NIM 4]) – QA & Tester\n"
        "PROGRAM STUDI INFORMATIKA — FAKULTAS ILMU KOMPUTER\n"
    )
    r_meta.font.size = Pt(10)
    r_meta.italic = True

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.add_run("_______________________________________________________________________\n")

    p_abs = doc.add_paragraph()
    r_absh = p_abs.add_run("RINGKASAN EKSEKUTIF (ABSTRAK)\n")
    r_absh.bold = True
    r_absh.font.size = Pt(11)
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.line_spacing = 1.15
    p_abs.add_run(
        "Rekrutmen asisten laboratorium komputer memerlukan proses evaluasi multi-kriteria yang adil, transparan, "
        "dan terukur. Proyek ini mengembangkan TalentSet, sebuah sistem klasifikasi berbasis web yang mengimplementasikan "
        "konsep aljabar himpunan diskrit untuk menyaring kandidat secara deterministik. Sistem ini memodelkan himpunan semesta (U) "
        "dan tiga kategori kriteria (A, B, C), serta mengeksekusi operasi irisan (∩), gabungan (∪), selisih (−), dan komplemen ('). "
        "Hasil evaluasi divisualisasikan secara simultan melalui tabel beranotasi dan Diagram Venn tiga himpunan. Hasil pengujian membuktikan "
        "bahwa pemodelan aljabar himpunan mampu mengelompokkan profil pendaftar ke dalam penugasan laboratorium secara presisi sesuai formulasi logika formal."
    )

    p_h1 = doc.add_paragraph()
    r_h1 = p_h1.add_run("\nBAB I. PENDAHULUAN")
    r_h1.bold = True
    r_h1.font.size = Pt(12)

    p_sub1 = doc.add_paragraph()
    r_sub1 = p_sub1.add_run("1.1 Latar Belakang Masalah\n")
    r_sub1.bold = True
    p_sub1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_sub1.add_run(
        "Laboratorium Komputer di perguruan tinggi memegang peranan krusial dalam menyelenggarakan praktikum pemrograman, "
        "riset modul, dan operasional harian. Seleksi konvensional sering menggunakan pembobotan rata-rata linier yang rentan mengaburkan "
        "kekuatan spesifik kandidat: pendaftar dengan nilai koding luar biasa belum tentu memiliki keterampilan manajerial kepanitiaan, "
        "dan sebaliknya. Pendekatan Teori Himpunan Diskrit menghadirkan landasan matematis yang tegas (crisp logic) untuk membedah pendaftar "
        "ke dalam klaster kompetensi yang jelas tanpa adanya ambiguitas."
    )

    p_sub2 = doc.add_paragraph()
    r_sub2 = p_sub2.add_run("1.2 Rumusan Masalah & 1.3 Tujuan Proyek\n")
    r_sub2.bold = True
    p_sub2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_sub2.add_run(
        "Masalah yang diselesaikan mencakup: (1) bagaimana memodelkan data pendaftar ke dalam himpunan semesta (U) dan 3 subset kriteria (A, B, C); "
        "(2) bagaimana memformulasikan operasi ∩, ∪, −, dan komplemen untuk penjaringan posisi asisten; dan (3) bagaimana menyajikan Diagram Venn interaktif. "
        "Tujuannya adalah membangun sistem TalentSet berbasis Python/Streamlit yang deterministik dan mudah digunakan oleh Kepala Laboratorium."
    )

    doc.add_page_break()

    # =========================================================================
    # HALAMAN 2: BAB II LANDASAN TEORI & PEMODELAN MATEMATIS
    # =========================================================================
    p_h2 = doc.add_paragraph()
    r_h2 = p_h2.add_run("BAB II. LANDASAN TEORI & PEMODELAN MATEMATIS")
    r_h2.bold = True
    r_h2.font.size = Pt(12)

    p_21 = doc.add_paragraph()
    r_21 = p_21.add_run("2.1 Konsep Himpunan Semesta dan Himpunan Kriteria\n")
    r_21.bold = True
    p_21.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_21.add_run(
        "Himpunan adalah kumpulan objek yang terdefinisi secara jelas (well-defined collection). Objek dalam sistem TalentSet "
        "adalah mahasiswa pendaftar yang diidentifikasi secara unik oleh id_pendaftar.\n"
        "• Himpunan Semesta (U) = { x | x adalah mahasiswa pendaftar asisten laboratorium tahun berjalan }\n"
        "• Himpunan A (Kecakapan Pemrograman) = { x ∈ U | nilai_alpro(x) ≥ 80 }\n"
        "• Himpunan B (Kompetensi Organisasi) = { x ∈ U | pengalaman_organisasi(x) ≥ 2 periode }\n"
        "• Himpunan C (Keunggulan Akademik) = { x ∈ U | ipk(x) ≥ 3.50 }"
    )

    p_22 = doc.add_paragraph()
    r_22 = p_22.add_run("2.2 Formulasi Operasi Aljabar Himpunan pada Rekrutmen\n")
    r_22.bold = True
    p_22.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_22.add_run(
        "Enam skenario penugasan asisten laboratorium dimodelkan menggunakan aljabar himpunan diskrit:\n"
        "1. Koordinator Laboratorium (Irisan 3 Set): A ∩ B ∩ C = { x ∈ U | x ∈ A ∧ x ∈ B ∧ x ∈ C }\n"
        "   Menjaring kandidat serba bisa yang unggul di pemrograman, kepemimpinan, dan prestasi akademik.\n"
        "2. Asisten Modul Lanjut (Irisan 2 Set): A ∩ C = { x ∈ U | x ∈ A ∧ x ∈ C }\n"
        "   Menjaring kandidat dengan daya nalar koding dan akademik tinggi tanpa membatasi pengalaman organisasi.\n"
        "3. Siap Operasional Lab (Gabungan Set): A ∪ B = { x ∈ U | x ∈ A ∨ x ∈ B }\n"
        "   Menjaring seluruh pendaftar yang memiliki kemampuan teknis koding minimal ATAU memiliki jiwa kepemimpinan.\n"
        "4. Asisten Riset / Bank Soal (Selisih Set): (A ∩ C) − B = { x ∈ U | (x ∈ A ∧ x ∈ C) ∧ x ∉ B }\n"
        "   Kandidat unggul teknis dan IPK namun belum pernah aktif berorganisasi formal.\n"
        "5. Programmer Murni (Selisih Majemuk): A − (B ∪ C) = { x ∈ U | x ∈ A ∧ x ∉ B ∧ x ∉ C }\n"
        "   Kandidat yang hanya lolos pada kualifikasi koding saja tanpa menyentuh ambang batas B maupun C.\n"
        "6. Berkas Tidak Memenuhi Syarat (Komplemen Total): U − (A ∪ B ∪ C) = { x ∈ U | x ∉ A ∧ x ∉ B ∧ x ∉ C }\n"
        "   Kandidat yang berada di luar ketiga lingkaran kriteria (berkas gugur tahap awal)."
    )

    p_23 = doc.add_paragraph()
    r_23 = p_23.add_run("2.3 Fungsi Karakteristik Keanggotaan Diskrit\n")
    r_23.bold = True
    p_23.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_23.add_run(
        "Status keanggotaan pendaftar x dipetakan melalui fungsi karakteristik biner χ(x) ∈ {0, 1}. Kombinasi 3 himpunan "
        "kriteria membagi semesta U menjadi 2^3 = 8 wilayah disjoin (7 area irisan di dalam Diagram Venn dan 1 area komplemen luar)."
    )

    doc.add_page_break()

    # =========================================================================
    # HALAMAN 3: BAB III METODOLOGI, DESAIN SISTEM, & STRUKTUR DATASET
    # =========================================================================
    p_h3 = doc.add_paragraph()
    r_h3 = p_h3.add_run("BAB III. METODOLOGI, DESAIN SISTEM, & STRUKTUR DATASET")
    r_h3.bold = True
    r_h3.font.size = Pt(12)

    p_31 = doc.add_paragraph()
    r_31 = p_31.add_run("3.1 Struktur Dataset Awal (15 Record Representatif)\n")
    r_31.bold = True
    p_31.add_run("Data awal disusun dalam format CSV yang mencakup seluruh variasi kombinasi keanggotaan:")

    # Tabel Dataset Awal
    table1 = doc.add_table(rows=16, cols=6)
    table1.style = 'Table Grid'
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER

    headers1 = ["ID", "Nama Mahasiswa", "IPK", "Alpro", "Org", "Keanggotaan Set"]
    for i, h in enumerate(headers1):
        cell = table1.cell(0, i)
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(cell, "E2E8F0")

    data1 = [
        ("P01", "Aditia Nugraha", "3.82", "88", "3", "A ∩ B ∩ C"),
        ("P02", "Bella Safitri", "3.65", "84", "1", "(A ∩ C) - B"),
        ("P03", "Candra Pratama", "3.30", "92", "0", "A - (B ∪ C)"),
        ("P04", "Dian Kusuma", "3.55", "74", "2", "(B ∩ C) - A"),
        ("P05", "Eko Santoso", "3.10", "68", "3", "B - (A ∪ C)"),
        ("P06", "Farhan Ramadhan", "3.78", "70", "0", "C - (A ∪ B)"),
        ("P07", "Gita Ayu", "3.88", "85", "2", "A ∩ B ∩ C"),
        ("P08", "Hendra Wijaya", "3.40", "81", "2", "(A ∩ B) - C"),
        ("P09", "Indah Permata", "3.60", "90", "1", "(A ∩ C) - B"),
        ("P10", "Joko Susilo", "3.25", "65", "1", "U - (A ∪ B ∪ C)"),
        ("P11", "Kartika Sari", "3.52", "82", "2", "A ∩ B ∩ C"),
        ("P12", "Lukman Hakim", "3.70", "62", "2", "(B ∩ C) - A"),
        ("P13", "Maya Puspita", "3.45", "86", "0", "A - (B ∪ C)"),
        ("P14", "Naufal Hidayat", "3.20", "72", "0", "U - (A ∪ B ∪ C)"),
        ("P15", "Olivia Siregar", "3.75", "80", "3", "A ∩ B ∩ C")
    ]

    for row_idx, row_data in enumerate(data1, start=1):
        for col_idx, val in enumerate(row_data):
            cell = table1.cell(row_idx, col_idx)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_paragraph() # Spacing

    p_32 = doc.add_paragraph()
    r_32 = p_32.add_run("3.2 Arsitektur Alur Sistem (System Pipeline)\n")
    r_32.bold = True
    p_32.add_run("Alur sistem berjalan dari: Input CSV → Engine Python Set (Hashing O(1)) → Filter Operasi → Visualisasi Venn & Ekspor CSV.")

    # Kotak Screenshot 1
    add_screenshot_box(doc, "Gambar 3.1: Diagram Alir Arsitektur Pemrosesan Data TalentSet", "Lebar 13–14 cm, Center Align")

    doc.add_page_break()

    # =========================================================================
    # HALAMAN 4: BAB IV IMPLEMENTASI, HASIL PENGUJIAN, & ANALISIS
    # =========================================================================
    p_h4 = doc.add_paragraph()
    r_h4 = p_h4.add_run("BAB IV. IMPLEMENTASI, HASIL PENGUJIAN, & ANALISIS")
    r_h4.bold = True
    r_h4.font.size = Pt(12)

    p_41 = doc.add_paragraph()
    r_41 = p_41.add_run("4.1 Implementasi Antarmuka Pengguna (Slate Dark UI)\n")
    r_41.bold = True
    p_41.add_run(
        "Antarmuka dirancang menggunakan tema Modern Slate Dark untuk kenyamanan visual evaluator. Dashboard memuat 4 kartu metrik kardinalitas "
        "(|U|, |A|, |B|, |C|) serta kontrol slider nilai ambang batas dinamis."
    )

    # Kotak Screenshot 2
    add_screenshot_box(doc, "Gambar 4.1: Tampilan Header dan Kartu Metrik Kardinalitas Sistem", "Lebar 14–15 cm, Center Align")

    p_42 = doc.add_paragraph()
    r_42 = p_42.add_run("4.2 Hasil Evaluasi Operasi dan Diagram Venn\n")
    r_42.bold = True
    p_42.add_run(
        "Pada parameter default (Alpro ≥ 80, Org ≥ 2, IPK ≥ 3.50), semesta terbagi menjadi |A|=9, |B|=8, dan |C|=9. "
        "Operasi Koordinator Lab (A ∩ B ∩ C) menghasilkan 4 kandidat berimbang yang berada tepat di pusat Diagram Venn (P01, P07, P11, P15)."
    )

    # Kotak Screenshot 3
    add_screenshot_box(doc, "Gambar 4.2: Visualisasi Tabel Hasil Penjaringan & Diagram Venn 3 Himpunan", "Lebar 14–15 cm, Center Align")

    p_43 = doc.add_paragraph()
    r_43 = p_43.add_run("4.3 Matriks Validasi Operasi Himpunan (Edge Cases)\n")
    r_43.bold = True

    # Tabel Validasi Operasi
    table2 = doc.add_table(rows=7, cols=5)
    table2.style = 'Table Grid'
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER

    headers2 = ["No", "Kasus Seleksi", "Formulasi Himpunan", "Kardinalitas", "ID Kandidat Terpilih"]
    for i, h in enumerate(headers2):
        cell = table2.cell(0, i)
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(cell, "E2E8F0")

    data2 = [
        ("1", "Koordinator Lab", "A ∩ B ∩ C", "4", "P01, P07, P11, P15"),
        ("2", "Asisten Modul Lanjut", "A ∩ C", "6", "P01, P02, P07, P09, P11, P15"),
        ("3", "Siap Operasional", "A ∪ B", "13", "P01, P02, P03, P04, P05, P07, P08, P09, P11, P12, P13, P15"),
        ("4", "Asisten Riset", "(A ∩ C) - B", "2", "P02, P09"),
        ("5", "Programmer Murni", "A - (B ∪ C)", "2", "P03, P13"),
        ("6", "Berkas Gugur", "U - (A ∪ B ∪ C)", "2", "P10, P14")
    ]

    for row_idx, row_data in enumerate(data2, start=1):
        for col_idx, val in enumerate(row_data):
            cell = table2.cell(row_idx, col_idx)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_page_break()

    # =========================================================================
    # HALAMAN 5: BAB V PEMBAHASAN, PEMBAGIAN TUGAS, & PENUTUP
    # =========================================================================
    p_h5 = doc.add_paragraph()
    r_h5 = p_h5.add_run("BAB V. PEMBAHASAN, PEMBAGIAN TUGAS, & PENUTUP")
    r_h5.bold = True
    r_h5.font.size = Pt(12)

    p_51 = doc.add_paragraph()
    r_51 = p_51.add_run("5.1 Pembahasan Fitur Ekspor & Collapsible Semesta\n")
    r_51.bold = True
    p_51.add_run(
        "Aplikasi menyediakan tombol unduh CSV dinamis yang mengekspor hasil filter secara instan untuk kebutuhan absensi wawancara. "
        "Fitur collapsible expander memungkinkan tim evaluator mengaudit data semesta tanpa menggeser tata letak utama."
    )

    # Kotak Screenshot 4
    add_screenshot_box(doc, "Gambar 5.1: Panel Data Semesta Lengkap dan Fitur Ekspor CSV", "Lebar 13–14 cm, Center Align")

    p_52 = doc.add_paragraph()
    r_52 = p_52.add_run("5.2 Pembagian Tugas Anggota Kelompok\n")
    r_52.bold = True

    # Tabel Pembagian Tugas
    table3 = doc.add_table(rows=5, cols=3)
    table3.style = 'Table Grid'
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER

    headers3 = ["Nama Anggota", "Peran", "Deskripsi Kontribusi & Tanggung Jawab"]
    for i, h in enumerate(headers3):
        cell = table3.cell(0, i)
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9.5)
        set_cell_background(cell, "E2E8F0")

    data3 = [
        ("[Nama Anggota 1]", "Project Lead", "Mengoordinasikan milestone, mengelola repositori GitHub, menyusun dokumen laporan Word."),
        ("[Nama Anggota 2]", "Set Engine Engineer", "Memodelkan aljabar himpunan diskrit, memvalidasi operasi matematika, menulis engine Python."),
        ("[Nama Anggota 3]", "UI/UX & Visualization", "Membangun tampilan Slate Dark Streamlit dan konfigurasi visualisasi Diagram Venn."),
        ("[Nama Anggota 4]", "QA & Video Creator", "Menyusun dataset kasus batas, memverifikasi hasil filter, dan memproduksi video demonstrasi.")
    ]

    for row_idx, row_data in enumerate(data3, start=1):
        for col_idx, val in enumerate(row_data):
            cell = table3.cell(row_idx, col_idx)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)

    doc.add_paragraph()

    p_53 = doc.add_paragraph()
    r_53 = p_53.add_run("5.3 Kesimpulan & 5.4 Saran\n")
    r_53.bold = True
    p_53.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_53.add_run(
        "Kesimpulan: Teori himpunan diskrit terbukti efektif sebagai landasan seleksi asisten laboratorium yang objektif dan bebas bias subjektif. "
        "Saran: Pengembangan lanjutan dapat menambahkan Fuzzy Set Theory untuk mengakomodasi nilai ambang batas mengambang (borderline cases)."
    )

    p_ref = doc.add_paragraph()
    r_ref = p_ref.add_run("DAFTAR PUSTAKA\n")
    r_ref.bold = True
    p_ref.paragraph_format.line_spacing = 1.15
    p_ref.add_run(
        "1. Munir, Rinaldi. (2016). Matematika Diskrit (Edisi Revisi Keenam). Bandung: Penerbit Informatika.\n"
        "2. Rosen, Kenneth H. (2019). Discrete Mathematics and Its Applications (8th Edition). McGraw-Hill Education.\n"
        "3. Streamlit Inc. (2024). Streamlit Documentation. Diakses daring dari https://docs.streamlit.io/.\n"
        "4. Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. Computing in Science & Engineering, 9(3), 90-95."
    )

    # Simpan file dokumen Word
    filename = "Laporan_PJBL2_TalentSet.docx"
    doc.save(filename)
    print(f" Dokumen Word berhasil dibuat: {filename}")

if __name__ == "__main__":
    create_report()