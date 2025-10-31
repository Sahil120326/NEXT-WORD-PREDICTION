"""Download additional massive corpus to reach 25M+ words"""
import urllib.request
import os

# Add more massive books
urls = [
    ('https://www.gutenberg.org/files/1399/1399-0.txt', 'brothers_karamazov.txt'),
    ('https://www.gutenberg.org/files/1952/1952-0.txt', 'metamorphosis.txt'),
    ('https://www.gutenberg.org/files/205/205-0.txt', 'walden.txt'),
    ('https://www.gutenberg.org/files/1322/1322-0.txt', 'leaves_grass.txt'),
    ('https://www.gutenberg.org/files/158/158-0.txt', 'emma.txt'),
    ('https://www.gutenberg.org/files/161/161-0.txt', 'sense_sensibility.txt'),
    ('https://www.gutenberg.org/files/100/100-0.txt', 'complete_shakespeare.txt'),  # MASSIVE!
    ('https://www.gutenberg.org/files/1727/1727-0.txt', 'odyssey.txt'),
    ('https://www.gutenberg.org/files/4280/4280-0.txt', 'brothers_grimm.txt'),
    ('https://www.gutenberg.org/files/1998/1998-0.txt', 'dante_inferno.txt'),
    ('https://www.gutenberg.org/files/244/244-0.txt', 'study_scarlet.txt'),
    ('https://www.gutenberg.org/files/730/730-0.txt', 'oliver_twist.txt'),
    ('https://www.gutenberg.org/files/766/766-0.txt', 'david_copperfield.txt'),
    ('https://www.gutenberg.org/files/580/580-0.txt', 'around_world_80_days.txt'),
    ('https://www.gutenberg.org/files/1952/1952-0.txt', 'yellow_wallpaper.txt'),
    ('https://www.gutenberg.org/files/120/120-0.txt', 'treasure_island.txt'),
    ('https://www.gutenberg.org/files/1250/1250-0.txt', 'anthem_rand.txt'),
    ('https://www.gutenberg.org/files/16/16-0.txt', 'peter_pan.txt'),
    ('https://www.gutenberg.org/files/209/209-0.txt', 'vanity_fair.txt'),
    ('https://www.gutenberg.org/files/3296/3296-0.txt', 'rome_and_juliet.txt'),
]

os.makedirs('data', exist_ok=True)

# Read existing corpus
existing_text = ""
corpus_path = 'data/corpus.txt'
if os.path.exists(corpus_path):
    with open(corpus_path, 'r', encoding='utf-8') as f:
        existing_text = f.read()
    existing_words = len(existing_text.split())
    print(f"Existing corpus: {existing_words:,} words")
else:
    existing_words = 0

print("Downloading MORE books to reach 25M+ words...")
print("=" * 60)

all_text = [existing_text] if existing_text else []
total_words = existing_words

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
        print(f"✓ ({words:,} words) | Total: {total_words:,}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

# Write combined corpus
print("=" * 60)
print(f"Writing MEGA corpus to {corpus_path}...")
with open(corpus_path, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(all_text))

print(f"✓ Done! Total words: {total_words:,}")
print(f"✓ Corpus saved to: {corpus_path}")
print("\nNow restart the Flask app for much better predictions!")
