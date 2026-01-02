import glob
import os

from dotenv import load_dotenv

from app.db import get_cursor


def main() -> None:
    load_dotenv()

    here = os.path.dirname(__file__)
    migrations_dir = os.path.join(here, "..", "app", "migrations")
    paths = sorted(glob.glob(os.path.join(migrations_dir, "*.sql")))

    with get_cursor() as cur:
        for path in paths:
            with open(path, "r", encoding="utf-8") as f:
                sql = f.read()
            cur.execute(sql)
            print(f"Applied {os.path.basename(path)}")


if __name__ == "__main__":
    main()

