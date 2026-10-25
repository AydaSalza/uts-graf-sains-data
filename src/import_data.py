
import os
import sys
import pandas as pd
from tqdm import tqdm
from neo4j import GraphDatabase

# Koneksi ke Neo4j lokal
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "Alzy0806"

# Lokasi dataset dan ukuran tiap batch
CSV_PATH = os.path.join("data", "events.csv")
BATCH_SIZE = 5000



def buat_constraint(session):
    """Mencegah node Visitor dan Item dengan ID yang sama."""

    session.run("""
        CREATE CONSTRAINT visitor_id_unique IF NOT EXISTS
        FOR (v:Visitor)
        REQUIRE v.visitorId IS UNIQUE
    """).consume()

    session.run("""
        CREATE CONSTRAINT item_id_unique IF NOT EXISTS
        FOR (i:Item)
        REQUIRE i.itemId IS UNIQUE
    """).consume()



def impor_batch(tx, batch):
    """Memasukkan satu batch event ke graph Neo4j."""
    query = """
    UNWIND $batch AS row

    MERGE (v:Visitor {visitorId: row.visitorid})
    MERGE (i:Item {itemId: row.itemid})

    FOREACH (_ IN CASE
        WHEN row.event = 'view' THEN [1]
        ELSE []
    END |
        CREATE (v)-[:VIEWED {
            timestamp: row.timestamp
        }]->(i)
    )

    FOREACH (_ IN CASE
        WHEN row.event = 'addtocart' THEN [1]
        ELSE []
    END |
        CREATE (v)-[:ADDED_TO_CART {
            timestamp: row.timestamp
        }]->(i)
    )

    FOREACH (_ IN CASE
        WHEN row.event = 'transaction' THEN [1]
        ELSE []
    END |
        CREATE (v)-[:BOUGHT {
            timestamp: row.timestamp,
            transactionId: row.transactionid
        }]->(i)
    )
    """
    tx.run(query, batch=batch).consume()


def main():
    if PASSWORD == "GANTI_DENGAN_PASSWORD_NEO4J":
        print("Ubah PASSWORD di file import_data.py terlebih dahulu.")
        sys.exit(1)

    if not os.path.exists(CSV_PATH):
        print(f"File tidak ditemukan: {CSV_PATH}")
        print("Pastikan events.csv berada di dalam folder data.")
        sys.exit(1)

    driver = None

    try:
        driver = GraphDatabase.driver(
            URI,
            auth=(USERNAME, PASSWORD)
        )
        driver.verify_connectivity()
        print("Berhasil terhubung ke Neo4j!")

        # Validasi nama kolom
        kolom_wajib = {
            "timestamp", "visitorid", "event",
            "itemid", "transactionid"
        }
        kolom_csv = set(pd.read_csv(CSV_PATH, nrows=0).columns)
        if not kolom_wajib.issubset(kolom_csv):
            raise ValueError(
                f"Kolom CSV tidak sesuai. Kolom ditemukan: {kolom_csv}"
            )

        # Hitung jumlah baris untuk progress bar
        print("Menghitung jumlah baris CSV...")
        with open(CSV_PATH, "r", encoding="utf-8-sig") as file:
            total = sum(1 for _ in file) - 1

        if total <= 0:
            print("CSV kosong.")
            return

        print(f"Jumlah event yang akan diimpor: {total:,}")

        with driver.session() as session:
            buat_constraint(session)

            chunks = pd.read_csv(
                CSV_PATH,
                chunksize=BATCH_SIZE,
                dtype={
                    "timestamp": "int64",
                    "visitorid": "int64",
                    "itemid": "int64"
                }
            )

            with tqdm(
                total=total,
                desc="Impor event",
                unit="baris"
            ) as progress:
                for chunk in chunks:
                    # Mengubah nilai transaksi kosong menjadi None
                    chunk["transactionid"] = (
                        chunk["transactionid"].astype(object)
                    )
                    chunk.loc[
                        chunk["transactionid"].isna(),
                        "transactionid"
                    ] = None

                    records = chunk.to_dict(orient="records")

                    # Menjalankan transaksi batch
                    session.write_transaction(impor_batch, records)
                    progress.update(len(chunk))

        print("\nImpor selesai!")

        # Memeriksa jumlah node dan relasi
        with driver.session() as session:
            node_result = session.run("""
                MATCH (n)
                RETURN labels(n) AS label, count(*) AS jumlah
            """)
            print("\nJumlah node:")
            for record in node_result:
                print(record["label"], record["jumlah"])

            rel_result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) AS jenis, count(*) AS jumlah
                ORDER BY jenis
            """)
            print("\nJumlah relasi:")
            for record in rel_result:
                print(record["jenis"], record["jumlah"])

    except Exception as error:
        print("\nProses gagal:")
        print(error)
        print(
            "\nPeriksa status Neo4j, password, alamat koneksi, "
            "dan lokasi events.csv."
        )
        sys.exit(1)

    finally:
        if driver is not None:
            driver.close()


if __name__ == "__main__":
    main()
