
from neo4j import GraphDatabase

# Sesuaikan dengan database Neo4j milikmu
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "Alzy0806"


def tambah_teman(tx, nama, nama_teman):
    query = """
    MERGE (a:Person {name: $nama})
    MERGE (b:Person {name: $nama_teman})
    MERGE (a)-[:KNOWS]->(b)
    """
    tx.run(query, nama=nama, nama_teman=nama_teman)


def tampilkan_teman(tx, nama):
    query = """
    MATCH (a:Person)-[:KNOWS]->(b:Person)
    WHERE a.name = $nama
    RETURN b.name AS teman
    ORDER BY teman
    """
    hasil = tx.run(query, nama=nama)
    return [record["teman"] for record in hasil]


def main():
    driver = None

    try:
        driver = GraphDatabase.driver(
            URI,
            auth=(USERNAME, PASSWORD)
        )

        driver.verify_connectivity()
        print("Berhasil terhubung ke Neo4j!")

        with driver.session() as session:
            daftar_teman = [
                ("Arthur", "Guinevere"),
                ("Arthur", "Lancelot"),
                ("Arthur", "Merlin"),
            ]

            for nama, teman in daftar_teman:
                session.write_transaction(
                    tambah_teman, nama, teman
                )

            hasil = session.read_transaction(
                tampilkan_teman, "Arthur"
            )

        print("\nTeman Arthur:")
        for teman in hasil:
            print("-", teman)

        print("\nPraktikum 1.2 berhasil!")

    except Exception as error:
        print("\nKoneksi atau proses gagal.")
        print("Detail error:", error)
        print(
            "\nPeriksa status database, alamat koneksi, "
            "username, dan password Neo4j."
        )

    finally:
        if driver is not None:
            driver.close()


if __name__ == "__main__":
    main()
