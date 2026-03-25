import argparse
import zxcvbn
import itertools

def analyze_password(password):
    print("\n--- Password Strength Analysis ---")
    results = zxcvbn.zxcvbn(password)
    score = results['score']
    crack_time = results['crack_times_display']['offline_fast_hashing_1e10_per_second']
    
    print(f"Target Password: {password}")
    print(f"Strength Score (0-4): {score}")
    print(f"Estimated time to crack (Offline GPU): {crack_time}")
    
    if results['feedback']['warning']:
        print(f"Warning: {results['feedback']['warning']}")
    if results['feedback']['suggestions']:
        print("Suggestions:")
        for sug in results['feedback']['suggestions']:
            print(f" - {sug}")
    print("----------------------------------\n")

def generate_wordlist(name, pet, year, output_file):
    print("--- Generating Custom Wordlist ---")
    base_words = [name.lower(), pet.lower(), year]
    
    # 1. Capitalization Variations
    capitalized = [w.capitalize() for w in base_words if isinstance(w, str)]
    upper = [w.upper() for w in base_words if isinstance(w, str)]
    
    # 2. Leetspeak Substitutions
    leet_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    leetspeak = []
    for word in base_words:
        if isinstance(word, str):
            leet_word = "".join(leet_map.get(c, c) for c in word)
            leetspeak.append(leet_word)
            
    # Combine core words
    core_words = list(set(base_words + capitalized + upper + leetspeak))
    
    # 3. Mangling: Append/Prepend years and symbols
    symbols = ['!', '@', '#', '123']
    years = [year, "2023", "2024"]
    
    final_wordlist = set()
    
    # Generate Permutations
    for word in core_words:
        final_wordlist.add(str(word))
        for y in years:
            final_wordlist.add(f"{word}{y}")
            for sym in symbols:
                final_wordlist.add(f"{word}{y}{sym}")
                final_wordlist.add(f"{word}{sym}{y}")
                
    # Export to file
    with open(output_file, "w") as f:
        for pwd in final_wordlist:
            f.write(f"{pwd}\n")
            
    print(f"[*] Success! {len(final_wordlist)} custom passwords written to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Password Security Toolkit")
    
    # Mode 1: Analysis
    parser.add_argument("--analyze", help="Analyze a specific password's strength", type=str)
    
    # Mode 2: Wordlist Generation
    parser.add_argument("--name", help="Target's first or last name", type=str)
    parser.add_argument("--pet", help="Target's pet name", type=str)
    parser.add_argument("--year", help="Significant year (e.g., DOB, Anniversary)", type=str)
    parser.add_argument("--output", help="Output file for wordlist (default: wordlist.txt)", default="wordlist.txt", type=str)

    args = parser.parse_args()

    if args.analyze:
        analyze_password(args.analyze)
        
    elif args.name and args.pet and args.year:
        generate_wordlist(args.name, args.pet, args.year, args.output)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()