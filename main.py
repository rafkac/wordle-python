import re

# load word list as global variable
with open("shortlist.txt") as f:
    words = [line.strip().lower() for line in f if line.strip()]

def main():
    # game loop
    solved = False
    must_have = set("")
    must_not_have = set("")
    feedback = ""
    regex = list(".....") # 5 spots initially all unknown


    while (not solved):
        print_possibilities(must_have, must_not_have, regex)

        guess = input("Guess: ")
        feedback = input("Feedback: ")

        if (feedback == "22222"):
            print("\nSolved! Good game.")
            solved = True
        else:
            for i, letter in enumerate(feedback):
                match letter:
                    # green
                    case "2":
                        regex[i] = guess[i]
                        must_have.add(guess[i])
                    # yellow
                    case "1":
                        if spot_not_taken(regex[i]):
                            regex[i] = exclude_letter(regex[i], guess[i])
                        must_have.add(guess[i])
                    # grey
                    case _:
                        must_not_have.add(guess[i])
        
        # handle single-occurring letters
        common_set = must_have & must_not_have
        must_not_have -= common_set
        for x in common_set:
            for i, spot in enumerate(regex):
                if spot_not_taken(spot):
                    regex[i] = exclude_letter(regex[i], x)              



# helper functions 

# exclude letter from a regex spot
def exclude_letter(old_str, letter):
    if old_str.startswith("[^") and old_str.endswith("]"):
        return "[^" + letter + old_str[2:]
    else:
        return f"[^{letter}]"

# check if spot is not yet taken by a confirmed letter
def spot_not_taken(s):
    return s.startswith((".", "[^]"))

# print possible words based on current constraints
def print_possibilities(include, exclude, pattern, word_list=words):
    filtered = [
        w for w in word_list
        if include.issubset(set(w)) and not (set(w) & exclude)
    ]
    pattern = re.compile("".join(pattern))
    patterned = [w for w in filtered if pattern.match(w)]

    print(", ".join(patterned))
    print(f"there are {len(patterned)} possibilities")
    

if __name__ == "__main__":
    main()