import requests
import os
import pandas as pd 
import string
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup


POSITIVE_SCORE = []
NEGATIVE_SCORE = []
POLARITY_SCORE = []
SUBJECTIVITY_SCORE = []
AVG_SENTENCE_LENGTH = []
PERCENTAGE_OF_COMPLEX_WORDS = []
FOG_INDEX = []
AVG_NUMBER_OF_WORDS_PER_SENTENCE = []
COMPLEX_WORD_COUNT = []
WORD_COUNT = []
SYLLABLE_PER_WORD = []
PERSONAL_PRONOUNS = []
AVG_WORD_LENGTH = []


def extract():
    df = pd.read_csv('Input.csv')

    for index, row in df.iterrows():
        url = row["URL"]
        url_id = row["URL_ID"]

        # GETTING RESPONSE FROM URL
        try:
            response = requests.get(url)
            print(f"got response of {url_id}:{response.status_code}")
        except Exception as e:
            print(f"Error occured when getting response of {url_id}\n{e}")

        #GETTING SOUP CONTENT 
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error occured when prasing data of {url_id}\n{e}")

        # GETIING TITLE OF URL
        try:
            title = soup.find('h1')
            if title:
                title = title.get_text()
        except Exception as e:
            print(f"Error occured when getting title of {url_id}\n{e}")

        # GETTING CONTENT OF URL
        all_content = ""
        try:
            text = soup.get_text().replace('\n','').split('.')[3:-8]
            filters = '.'.join(text)
            all_content += filters
        except Exception as e:
            print(f"Error occured when finding content of {url_id}\n{e}")

        # WRITE TITLE AND CONTENT IN FILE
        directory = 'articles_text'
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = f"{directory}/{url_id}.txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(f"{title}\n{all_content}")

extract()

# LOADING TEXT_FILE AND PERFORMING TEXTUAL ANALYSIS
folder = "articles_text"
files = os.listdir(folder)
for file_name in files:
    try:
        # file_path = os.path.join(folder, file_name)
        file_path = f"{folder}/{file_name}"
        with open(file_path, 'r',errors='ignore') as text_file:
            text = text_file.read()
            lower_text = text.lower()
    except Exception as e:
        print(f"Error occured while getting file {file_name}\n{e}")

    # REMOVING PUNCTUATION
    cleaned_text = lower_text.translate(str.maketrans('','',string.punctuation))

    # TOKENIZED WORD
    tokenizes_words = word_tokenize(cleaned_text)

    # STOPWORDS AND FILTER
    def filtered_text():
        filtered_text = []
        temp = []
        directory = 'stopword_dict'
        for file in os.listdir(directory):
            file_path = f"{directory}/{file}"
            with open(file_path, 'r',errors='ignore') as  file:
                stop_word_file = file.read().lower()

                if file_path == "stopword_dict/StopWords_Auditor.txt":
                    for word in tokenizes_words:
                        if word not in stop_word_file:
                            temp.append(word)
                            filtered_text = temp.copy()
                    temp.clear()

                else:
                    for word in filtered_text:
                        if word not in stop_word_file:
                            temp.append(word)
                            filtered_text = temp.copy()
                    temp.clear()
        return filtered_text
    
    filtered = filtered_text()
    
    # POSITIVE SCORE
    def positive():
        positive_file = "MasterDictionary\positive-words.txt"
        positive_word = []
        with open(positive_file, 'r', errors='ignore') as file:
            positive_text = file.read().lower()

            for word in filtered:
                if word in positive_text:
                    positive_word.append(word)
        return  len(positive_word)
    
    positive_score = positive()
    POSITIVE_SCORE.append(positive_score)
    
    # GETTING NEGATIVE SCORE
    def negative():
        negative_file = "MasterDictionary/negative-words.txt"
        negative_word = []
        with open(negative_file, 'r',errors='ignore') as file:
            negative_text = file.read().lower()

            for word in filtered:
                if word in negative_text:
                    negative_word.append(word)
        return len(negative_word)
    
    negative_score = negative()
    NEGATIVE_SCORE.append(negative_score)
    
    # POLARTITY SCORE
    def polarity():
        return (positive_score - negative_score) / ((positive_score + negative_score )+ 0.000001)
    polarity_score = polarity()
    POLARITY_SCORE.append(polarity_score)

    # SUBJECTIVITY SCORE
    def subjective():
        return (positive_score + negative_score)/ (len(filtered) + 0.000001)
    subjective_score = subjective()
    SUBJECTIVITY_SCORE.append(subjective_score)

    # COUNTING NUMBERS OF COMPLEX WORDS
    def complex():
        complex_words = []
        for word in filtered:
            vowels = 'aeiou'
            syllable_count_word = sum(1 for letter in word if letter.lower() in vowels)
            if syllable_count_word > 2: 
                complex_words.append(word)
        return len(complex_words)
    
    complex_words = complex()
    COMPLEX_WORD_COUNT.append(complex_words)

    # SYLLABLE WORD COUNT
    def syllable():
        syllable_count = 0
        syllable_words =[]
        for word in filtered:
            if word.endswith('es'):
                word = word[:-2]
            elif word.endswith('ed'):
                word = word[:-2]
                vowels = 'aeiou'
                syllable_count_word = sum( 1 for letter in word if letter.lower() in vowels)
                if syllable_count_word >= 1:
                    syllable_words.append(word)
                    syllable_count += syllable_count_word
        return syllable_count, syllable_words

    syllable_list = list(syllable())
    syllable_count = syllable_list[0]
    syllable_words = syllable_list[1]

    # AVERAGE WORD LENGHT 
    def avg_word_length():
        char_count = 0
        for word in filtered:
            for char in word:
                char_count += 1
        average_word_length = char_count / len(filtered)
        return average_word_length
    
    average_word_length = avg_word_length()
    AVG_WORD_LENGTH.append(average_word_length)
    AVG_NUMBER_OF_WORDS_PER_SENTENCE.append(average_word_length)
    
    # PERSONAL PRONOUN COUNT
    import regex as re
    def personal_noun():
        personal_pronuous = ["I", "we", "my", "ours", "us"]
        pp_count = 0
        for pronoun in personal_pronuous:
            pp_count += len(re.findall(r"\b" + pronoun + r"\b", lower_text))
        return str(pp_count)
    
    personal_pronuous = personal_noun()
    PERSONAL_PRONOUNS.append(personal_pronuous)

    # WORD COUNT

    num_words = len(filtered)
    WORD_COUNT.append(len(filtered))

    sentences = text.split('.')
    num_sentences = len(sentences)

    # AVERAGE SENTENCE LENGTH
    average_sentence_length = num_words / num_sentences
    AVG_SENTENCE_LENGTH.append(average_sentence_length)

    # SYLLABLE PER WORD
    try:
        if syllable_count != 0 and len(syllable_words) != 0:
            average_sllyable_count = syllable_count / len(syllable_words)
            SYLLABLE_PER_WORD.append(average_sllyable_count)
        else:
            average_sllyable_count = 0
            SYLLABLE_PER_WORD.append(average_sllyable_count)
    except ZeroDivisionError:
        average_sllyable_count = 0
        
    #  PERCENTAGE OF COMPLEX WORDS
    percent_complex_words = complex_words / num_words
    PERCENTAGE_OF_COMPLEX_WORDS.append(percent_complex_words)

    # FOG INDEX
    fog_index = 0.4 * (average_sentence_length + percent_complex_words)
    FOG_INDEX.append(fog_index)

# STORED ALL URL'S DATA IN DICT
variables = {'POSITIVE SCORE': POSITIVE_SCORE,
             'NEGATIVE SCORE': NEGATIVE_SCORE,
             'POLARITY SCORE': POLARITY_SCORE, 
             'SUBJECTIVITY SCORE': SUBJECTIVITY_SCORE,
             'AVG SENTENCE LENGTH': AVG_SENTENCE_LENGTH,
             'PERCENTAGE OF COMPLEX WORDS': PERCENTAGE_OF_COMPLEX_WORDS,
             'FOG INDEX': FOG_INDEX,
             'AVG NUMBER OF WORDS PER SENTENCE': AVG_NUMBER_OF_WORDS_PER_SENTENCE,
             'COMPLEX WORD COUNT': COMPLEX_WORD_COUNT,
             'WORD COUNT': WORD_COUNT,
             'SYLLABLE PER WORD': SYLLABLE_PER_WORD,
             'PERSONAL PRONOUNS': PERSONAL_PRONOUNS,
             'AVG WORD LENGTH': AVG_WORD_LENGTH
        }
 
#  REMOVE NULL COLUMNS
df = pd.read_csv('Input.csv')
df.dropna(axis='columns',inplace=True)
df1 = pd.DataFrame.from_dict(variables)

# SAVING THE DATA IN FOLDER
df3=df.join(df1, lsuffix="_left", rsuffix="_right", how='left')
df3.to_csv("Output Data.csv")