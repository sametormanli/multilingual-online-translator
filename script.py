import requests
from bs4 import BeautifulSoup
import sys


languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish', 'portuguese',
             'romanian', 'russian', 'turkish', 'all']
headers = {'user-agent': 'Mozilla/5.0'}
one_lang = True
s = requests.Session()


def main():
    print("Hello, you're welcome to the translator. Translator supports:\n"
          "1. Arabic\n"
          "2. German\n"
          "3. English\n"
          "4. Spanish\n"
          "5. French\n"
          "6. Hebrew\n"
          "7. Japanese\n"
          "8. Dutch\n"
          "9. Polish\n"
          "10. Portuguese\n"
          "11. Romanian\n"
          "12. Russian\n"
          "13. Turkish\n")
    user_lang = languages[int(input('Type the number of your language: ')) - 1]
    trans_lang = int(input('Type the number of a language you want to translate or "0" for all: '))
    if trans_lang != 0:
        trans_lang = languages[trans_lang - 1]
        one_lang = True
    else:
        word = input('Type the word you want to translate: ')
        translate_all(user_lang, word)
        one_lang = False
    if one_lang:
        word = input('Type the word you want to translate: ')
        url = f'https://context.reverso.net/translation/{user_lang}-{trans_lang}/{word}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        words = [word.text.strip() for word in soup.find_all(['a', 'div'], class_='dict')]

        example_content = soup.find('section', id='examples-content')
        examples = [ex.text.strip() for ex in example_content.find_all(class_='ltr')]

        print(f'\n{trans_lang.capitalize()} Translations:')
        print(*words[:5], sep='\n')
        print(f'\n{trans_lang.capitalize()} Examples:')
        for i in range(0, 10, 2):
            print(examples[i] + ':')
            print(examples[i + 1])
            print()


def translate_all(lang, word):
    for language in languages:
        if lang != language:
            url = f'https://context.reverso.net/translation/{lang}-{language}/{word}'
            response = s.get(url, headers=headers)
            if response.status_code == 404:
                print('Sorry, unable to find', sys.argv[3])
                exit()
            if response.status_code != 200:
                print('Something wrong with your internet connection')
                exit()
            soup = BeautifulSoup(response.content, 'html.parser')
            try:
                result = soup.find(['a', 'div'], class_='dict').text.strip()
            except:
                pass
            example_content = soup.find('section', id='examples-content')
            example_1, example_2 = [ex.text.strip() for ex in example_content.find_all(class_=['ltr', 'rtl'])[:2]]

            with open(f'{word}.txt', 'a', encoding='utf-8') as f:
                f.write(language.capitalize() + ' Translations:\n')
                f.write(result + '\n\n')
                f.write(f'{language.capitalize()} examples:\n')
                f.write(example_1 + ':\n')
                f.write(example_2 + '\n\n')
    with open(f'{word}.txt', encoding='utf-8') as f:
        print(f.read())

if len(sys.argv) == 4:
    if sys.argv[1] not in languages:
        print("Sorry, the program doesn't support", sys.argv[1])
        exit()
    if sys.argv[2] not in languages:
        print("Sorry, the program doesn't support", sys.argv[2])
        exit()
    if sys.argv[2] != 'all':
        url = f'https://context.reverso.net/translation/{sys.argv[1]}-{sys.argv[2]}/{sys.argv[3]}'
        response = s.get(url, headers=headers)
        if response.status_code == 404:
            print('Sorry, unable to find', sys.argv[3])
            exit()
        if response.status_code != 200:
            print('Something wrong with your internet connection')
            exit()
        soup = BeautifulSoup(response.content, 'html.parser')
        words = [word.text.strip() for word in soup.find_all(['a', 'div'], class_='dict')]
        example_content = soup.find('section', id='examples-content')
        examples = [ex.text.strip() for ex in example_content.find_all(class_='ltr')]

        print()
        print(f'{sys.argv[2].capitalize()} Translations:')
        print(*words[:5], sep='\n')
        print()
        print(f'{sys.argv[2].capitalize()} Examples:')
        for i in range(0, 10, 2):
            print(examples[i] + ':')
            print(examples[i + 1])
            print()
    else:
        translate_all(sys.argv[1], sys.argv[3])
else:
    main()