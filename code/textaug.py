import sys
import random
import string

def shift_one_letter(word):
    if len(word) < 2:
        return word
    i = random.randint(0, len(word) - 2)
    return word[:i] + word[i+1] + word[i] + word[i+2:]

def shift_two_letters(word):
    if len(word) < 3:
        return word
    i = random.randint(0, len(word) - 3)
    return word[:i] + word[i+1] + word[i+2] + word[i] + word[i+3:]

def exchange_two_letters(word):
    if len(word) < 2:
        return word
    i, j = random.sample(range(len(word)), 2)
    word_list = list(word)
    word_list[i], word_list[j] = word_list[j], word_list[i]
    return ''.join(word_list)

def exchange_one_letter(word):
    if not word:
        return word
    i = random.randint(0, len(word) - 1)
    new_letter = random.choice(string.ascii_lowercase)
    return word[:i] + new_letter + word[i+1:]

def double_letter(word):
    if not word:
        return word
    i = random.randint(0, len(word) - 1)
    return word[:i] + word[i] * 2 + word[i+1:]

def remove_letter(word):
    if len(word) < 2:
        return word
    i = random.randint(0, len(word) - 1)
    return word[:i] + word[i+1:]

def augment_word(word):
    augmentations = [
        shift_one_letter,
        shift_two_letters,
        exchange_two_letters,
        exchange_one_letter,
        double_letter,
        remove_letter
    ]
    return random.choice(augmentations)(word.lower())

def main(input_file, output_file, num_augmentations):
    with open(input_file, 'r') as f:
        words = f.read().splitlines()

    augmented_words = []
    for word in words:
        augmented_words.append(word)  # Keep the original word
        for _ in range(num_augmentations):
            augmented_words.append(augment_word(word))

    with open(output_file, 'w') as f:
        for word in augmented_words:
            f.write(word + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python program.py <input .txt file> <output .txt file> <number of augmented words for each word>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    num_augmentations = int(sys.argv[3])

    main(input_file, output_file, num_augmentations)