"""Download a large text corpus for training"""
import urllib.request
import os

# Download a large book corpus from Project Gutenberg
# This will download multiple books to create a large training set

urls = [
    # Massive collection of classic literature from Project Gutenberg
    # This will give us 25+ million words
    ('https://www.gutenberg.org/files/2701/2701-0.txt', 'moby_dick.txt'),
    ('https://www.gutenberg.org/files/1342/1342-0.txt', 'pride_prejudice.txt'),
    ('https://www.gutenberg.org/files/84/84-0.txt', 'frankenstein.txt'),
    ('https://www.gutenberg.org/files/1661/1661-0.txt', 'sherlock.txt'),
    ('https://www.gutenberg.org/files/98/98-0.txt', 'tale_two_cities.txt'),
    ('https://www.gutenberg.org/files/11/11-0.txt', 'alice_wonderland.txt'),
    ('https://www.gutenberg.org/files/1184/1184-0.txt', 'count_monte_cristo.txt'),
    ('https://www.gutenberg.org/files/345/345-0.txt', 'dracula.txt'),
    ('https://www.gutenberg.org/files/174/174-0.txt', 'dorian_gray.txt'),
    ('https://www.gutenberg.org/files/1400/1400-0.txt', 'great_expectations.txt'),
    ('https://www.gutenberg.org/files/1399/1399-0.txt', 'anna_karenina.txt'),
    ('https://www.gutenberg.org/files/2600/2600-0.txt', 'war_and_peace.txt'),  # HUGE!
    ('https://www.gutenberg.org/files/4300/4300-0.txt', 'ulysses.txt'),  # Very large
    ('https://www.gutenberg.org/files/1952/1952-0.txt', 'yellow_wallpaper.txt'),
    ('https://www.gutenberg.org/files/64317/64317-0.txt', 'great_gatsby.txt'),
    ('https://www.gutenberg.org/files/1260/1260-0.txt', 'jane_eyre.txt'),
    ('https://www.gutenberg.org/files/76/76-0.txt', 'huckleberry_finn.txt'),
    ('https://www.gutenberg.org/files/46/46-0.txt', 'christmas_carol.txt'),
    ('https://www.gutenberg.org/files/1232/1232-0.txt', 'prince.txt'),
    ('https://www.gutenberg.org/files/1497/1497-0.txt', 'republic.txt'),
    ('https://www.gutenberg.org/files/135/135-0.txt', 'les_miserables.txt'),  # MASSIVE!
    ('https://www.gutenberg.org/files/2814/2814-0.txt', 'dubliners.txt'),
    ('https://www.gutenberg.org/files/1080/1080-0.txt', 'modest_proposal.txt'),
    ('https://www.gutenberg.org/files/219/219-0.txt', 'heart_of_darkness.txt'),
    ('https://www.gutenberg.org/files/2097/2097-0.txt', 'sun_also_rises.txt'),
    ('https://www.gutenberg.org/files/996/996-0.txt', 'don_quixote.txt'),  # Very large
    ('https://www.gutenberg.org/files/16389/16389-0.txt', 'persuasion.txt'),
    ('https://www.gutenberg.org/files/1250/1250-0.txt', 'anthem.txt'),
    ('https://www.gutenberg.org/files/43/43-0.txt', 'dr_jekyll.txt'),
    ('https://www.gutenberg.org/files/74/74-0.txt', 'tom_sawyer.txt'),
]

os.makedirs('data', exist_ok=True)
corpus_path = 'data/corpus.txt'

print("Downloading large text corpus...")
print("This will download ~10+ books from Project Gutenberg")
print("=" * 60)

all_text = []
total_words = 0

for url, filename in urls:
    try:
        print(f"Downloading {filename}...", end=' ')
        response = urllib.request.urlopen(url, timeout=30)
        text = response.read().decode('utf-8', errors='ignore')
        
        # Remove Project Gutenberg header/footer
        start_markers = ['*** START OF', '***START OF']
        end_markers = ['*** END OF', '***END OF']
        
        for marker in start_markers:
            if marker in text:
                text = text.split(marker, 1)[1]
                break
        
        for marker in end_markers:
            if marker in text:
                text = text.split(marker, 1)[0]
                break
        
        words = len(text.split())
        total_words += words
        all_text.append(text)
        print(f"✓ ({words:,} words)")
        
    except Exception as e:
        print(f"✗ Error: {e}")

# Write combined corpus
print("=" * 60)
print(f"Writing combined corpus to {corpus_path}...")
with open(corpus_path, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(all_text))

print(f"✓ Done! Total words: {total_words:,}")
print(f"✓ Corpus saved to: {corpus_path}")
print("\nNow restart the Flask app to use the new corpus!")
