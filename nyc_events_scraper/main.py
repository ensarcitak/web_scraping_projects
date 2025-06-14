from nyc_events.scraper import get_all_events
from nyc_events.transformer import load_and_transform_events, export_to_excel

def main():
    print("NYC Events Pipeline Started...\n")

    get_all_events()
    df = load_and_transform_events()
    print(f"\nTotal cleaned records: {len(df)}")

    export_to_excel(df)

    print("\nPipeline finished successfully.")

if __name__ == "__main__":
    main()
