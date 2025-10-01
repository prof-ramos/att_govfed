"""CLI helper to run the data processing pipeline locally."""
from app.processing import process_data


def main() -> None:
    result = process_data()
    # When the processing function returns a message, show it to the user.
    if result:
        print(result)


if __name__ == "__main__":
    main()
