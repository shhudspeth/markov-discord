"""Generate Markov text from text files."""

from random import choice
import sys
import os
import discord

token = os.environ['DISCORD_TOKEN']

def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    Example:
    >>> open_and_read_file("green-eggs.txt")
    'Would you could you in a house?\nWould you could you with a mouse?\n
    Would you could you in a box?\nWould you could you with a fox?\n
    Would you like green eggs and ham?\nWould you like them, Sam I am?\n'
    """

    # your code goes here
    file_ = open(file_path).read()

    return file_


def make_chains(text_string, n_gram):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.
     
    # found the tuple(list) idea from here : https://www.geeksforgeeks.org/python-convert-a-list-into-a-tuple/#:~:text=Itertools.Permutations()-,Python%20%7C%20Convert%20a%20list%20into%20a%20tuple,given%20list%20into%20a%20tuple.&text=Approach%20%231%20%3A%20Using%20tuple(,simply%20using%20tuple(list_name).
     
    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}
    text = text_string.split()
    
    n_gram = int(n_gram)
    # loop over text with indices, stop n-gram away
    for word in range(len(text)-n_gram):
        # set key tuple of n-gram words
        key_tuple = tuple(text[word:word+n_gram])
        # get current next word list
        next_word_list = chains.get(key_tuple,[])
        # append the next word to list
        next_word_list.append(text[word+n_gram]) 
        # set new next word list as the dictionary entry 
        chains[key_tuple] = next_word_list
        
    # set last n-gram as stop phrase           
    key_tuple = tuple(text[word+1:word+n_gram+1])
    chains[key_tuple] = None
            
    # # # print dictionary
    # for tuple_, list_ in chains.items():
    #     print(f"n-gram: {tuple_}, \n options: {list_}")

    return chains


def make_text(chains):
    """Return text from chains."""
    words = []
    not_end_of_list = True
    # your code goes here
    # use random.choice to pick a bigram element from keys
    # make a list of capitalized keys
    # capitalized_ngrams = []
    # for key in chains.keys():
    #     # check if the first tuple in key[0][0]
    #     if key[0][0].isupper():
    #         capitalized_ngrams.append(key)
    # # print(capitalized_ngrams)
    # choice_n = choice(capitalized_ngrams)
    # # add bigram key  to word list
    # words.extend(choice_n)
    # if chains[choice_n]:
    #     choose_third = choice(chains[choice_n])
    #     words.append(choose_third)

    selected_keys = list(chains.keys())
    count = 0
    while not_end_of_list:
        choice_n = choice(selected_keys)
        # print("first key", choice_n)
        if count == 0:
            words.extend(choice_n)
            # print('first gram', choice_n)
            # print(words)
        # add bigram key  to word list
        if chains[choice_n] and count <= 150:
            # print("list of options", chains[choice_n])
            # as long as there is an option, picks a random element from dict list
            choose_next = choice(chains[choice_n])
            # print("new word", choose_next)
            words.append(choose_next)
            # print("new text", words)
            # print('next word choice', choose_next)
            # take last word in tuple
            # first_word_in_key = choice_n[1:]
            
            # print(first_word_in_key)
            # print((choice_n[0].lower(), choice_n[1].lower()), (first_word_in_key.lower(), choose_next.lower()))
            # creates a list of keys whose first item in tuple is item from list
            selected_keys = [x for x in chains.keys() if x == tuple([*choice_n[1:], choose_next])]
            # print("next key", selected_keys)
            if selected_keys:
                # print('new options', selected_keys)
                pass
            else:
                # words.extend(choose_next)
                not_end_of_list = False

            count += 1
            # print('added to text', words)
        else:
            not_end_of_list = False

    return " ".join(words)



# client = discord.Client()

# @client.event
# async def on_ready():
#     print(f'Successfully connected! Logged in as {client.user}.')


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     # TODO: replace this with your code
#     if message.content:
#         print("sending a message")
#         choice_file = choice(['green-eggs.txt', 'gettysburg.txt', 'reading_gaol.txt'])
#         # choice_ngrams = choice([2, 3, 4, 5])
#         choice_ngrams = 2
#         input_text = open_and_read_file(choice_file)
#         # Get a Markov chain
#         chains = make_chains(input_text,choice_ngrams)
#         # Produce random text
#         random_text = make_text(chains)
#         await message.channel.send(random_text[:2000])
       


# client.run(token)



if __name__ == '__main__':
    # python3 markov text.txt no_n_grams
    input_path = sys.argv[1]
    n_grams = sys.argv[2]
    
    # Open the file and turn it into one long string
    input_text = open_and_read_file(input_path)
    # Get a Markov chain
    chains = make_chains(input_text,n_grams)
    # Produce random text
    random_text = make_text(chains)
    print(random_text)
