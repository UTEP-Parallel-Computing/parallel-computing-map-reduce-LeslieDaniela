import pymp
import re

# Importing Timer
import timeit

# Start Timer
start = timeit.default_timer()

# shake_file holds files
shake_files = ["shakespeare1.txt", "shakespeare2.txt", "shakespeare3.txt", "shakespeare4.txt",
               "shakespeare5.txt", "shakespeare6.txt", "shakespeare7.txt", "shakespeare8.txt"]

# word_list holds words of interest
word_list = ["hate", "love", "death", "night", "sleep",
             "time", "henry", "hamlet", "you", "my",
             "blood", "poison", "macbeth", "king",
             "heart", "honest"]


def read_shake(shake_files):
    with open(shake_files) as file:
        combined_files = file.read().lower()
    return combined_files


def count_words(word_list, combined_files):
    for word in word_list:
        locate = re.findall(word, combined_files)
        word_list[word] += len(locate)


def main():

    with pymp.Parallel(8) as p:

        combined_files = pymp.shared.dict()
        word_list = pymp.shared.dict()

        for word in word_list:
            word_list[word] = 0

            for files in combined_files:
                combined_files[files] = read_shake(files)

            sum_lock = p.lock

            for files in p.iterate(combined_files):
                sum_lock.aquire()
                word_list = count_words(word_list, combined_files[files])
                sum_lock.release()


# Ending Timer
stop = timeit.default_timer()
print('Time: ', stop - start)
print(word_list)

if __name__ == "__main__":
    main()
