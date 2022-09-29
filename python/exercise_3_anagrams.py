def is_anagram(first_word:str, second_word:str) -> bool:
    second_word = second_word.lower().replace(' ','')
    first_word = first_word.lower().replace(' ','')
    for i in {*list(first_word)}:
        if first_word.count(i) != second_word.count(i):
            break
    else:
        return True
    return False

print(is_anagram('Hello','Ellho')) # True
print(is_anagram('Tom Marvolo Riddle','Lord Voldemort')) # False
print(is_anagram('Danya','Nadya')) # True
