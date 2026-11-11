import json
import os

FILE_DATA = "pocketbudget_data.json"

def muat_data():
    if os.path.exists(FILE_DATA):
        with open(FILE_DATA, "r") as file:
            return json.load(file)
    return {"saldo": 0, "transaksi": []}

def simpan_data(data):
    with open(FILE_DATA, "w") as file:
        json.dump(data, file, indent=4)


SALDO_MINIMAL_URGENT = 100000  # Batas dana darurat (Rp 100.000)

def tambah_transaksi(data, jenis):
    try:
        jumlah = float(input("Masukkan jumlah (Rp): "))
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0!")
            return

        if jenis == "pemasukan":
            data["saldo"] += jumlah
            data["riwayat"].append({"jenis": "Pemasukan", "jumlah": jumlah})
            print(f"Pemasukan sebesar Rp {jumlah:,.0f} berhasil ditambahkan.")

        elif jenis == "pengeluaran":
            saldo_setelah_pengeluaran = data["saldo"] - jumlah

            # 1. CEK JIKA PENGELUARAN MEMBUAT SALDO DI BAWAH BATAS URGENT
            if saldo_setelah_pengeluaran < SALDO_MINIMAL_URGENT:
                print(f"\n❌ Transaksi Ditolak!")
                print(f"Sisa saldo Anda akan menjadi Rp {saldo_setelah_pengeluaran:,.0f}.")
                print(f"Minimal saldo Rp {SALDO_MINIMAL_URGENT:,.0f} harus disisa untuk kebutuhan URGENT!")
            
            # 2. CEK JIKA SALDO PAS MENYENTUH BATAS URGENT
            elif saldo_setelah_pengeluaran == SALDO_MINIMAL_URGENT:
                print(f"\n⚠️  NOTIFIKASI PERINGATAN:")
                print(f"Saldo Anda saat ini pas Rp {SALDO_MINIMAL_URGENT:,.0f} (Batas Dana Urgent)!")
                print(f"Anda tidak bisa melakukan pengeluaran lagi sampai ada pemasukan baru.")

            data["saldo"] = saldo_setelah_pengeluaran
            data["riwayat"].append({"jenis": "Pengeluaran", "jumlah": jumlah})
            print(f"Pengeluaran sebesar Rp {jumlah:,.0f} berhasil dicatat.")

        simpan_data(data)
    except ValueError:
        print("Input tidak valid! Harap masukkan angka.")

def tampilkan_riwayat(data):
    print("\n" + "="*40)
    print(f" SALDO SAAT INI: Rp{data['saldo']:,.2f}")
    print("="*40)
    print("RIWAYAT TRANSAKSI:")
    if not data["transaksi"]:
        print("Belum ada transaksi.")
    else:
        for i, t in enumerate(data["transaksi"], start=1):
            print(f"{i}. [{t['jenis']}] {t['keterangan']} - Rp{t['jumlah']:,.2f}")
    print("="*40)

def main():
    # --- FUNGSI UTAMA DAN NAVIGASI MENU ---
    data = muat_data()
    while True:
        print("\n=== APLIKASI POCKETBUDGET ===")
        print("1. Tambah Pemasukan")
        print("2. Tambah Pengeluaran")
        print("3. Lihat Saldo & Riwayat")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1-4): ")

        if pilihan == "1":
            tambah_transaksi(data, "pemasukan")
        elif pilihan == "2":
            tambah_transaksi(data, "pengeluaran")
        elif pilihan == "3":
            tampilkan_riwayat(data)
        elif pilihan == "4":
            print("Terima kasih telah menggunakan PocketBudget!")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()