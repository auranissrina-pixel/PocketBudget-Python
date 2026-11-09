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

def tambah_transaksi(data, jenis):
    try:
        keterangan = input("Masukkan keterangan: ")
        jumlah = float(input("Masukkan jumlah (Rp): "))
        if jumlah <= 0:
            print("Jumlah harus lebih dari 0!")
            return

        if jenis == "pengeluaran" and jumlah > data["saldo"]:
            print("Saldo tidak mencukupi!")
            return

        if jenis == "pemasukan":
            data["saldo"] += jumlah
        else:
            data["saldo"] -= jumlah

        transaksi = {
            "jenis": jenis.capitalize(),
            "keterangan": keterangan,
            "jumlah": jumlah
        }
        data["transaksi"].append(transaksi)
        simpan_data(data)
        print(f"\n[+] Berhasil menambahkan {jenis}: Rp{jumlah:,.2f}")
    except ValueError:
        print("Input jumlah harus berupa angka!")

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