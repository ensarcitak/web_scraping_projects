from nyc_events.scraper import get_all_events

def main():
    print("NYC Events Pipeline Started...\n")

    get_all_events()
    
    print("\nPipeline finished successfully.")

if __name__ == "__main__":
    main()
