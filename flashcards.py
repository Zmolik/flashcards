import json
import random
import argparse


class Flashcard:

    def __init__(self):
        self.dic_flashcards = {}
        self.log = []

    def add_new_card(self):
        while True:
            term = self.input_and_add_to_log(f'The card:\n> ')
            if term in self.dic_flashcards:
                self.print_and_add_to_log(f'The term "{term}" already exists. Try again:')
            else:
                break
        while True:
            definition = self.input_and_add_to_log('The definition of the card:\n> ')
            if definition in [def_[0] for def_ in self.dic_flashcards.values()]:  
                self.print_and_add_to_log(f'The definition "{definition}" already exists. Try again:')
            else:
                break
        self.dic_flashcards[term] = [definition, 0]
        self.print_and_add_to_log(f'The pair ("{term}":"{definition}") has been added.')

    def find_term_based_on_definition(self, user_definition):
        for term, definition in self.dic_flashcards.items():
            if user_definition == definition[0]:
                return term

    def ask_and_control(self):
        number_of_questions = int(self.input_and_add_to_log('How many times to ask?\n> '))
        for i in range(number_of_questions):
            term, definition = random.choice(list(self.dic_flashcards.items()))
            answer = self.input_and_add_to_log(f'Print the definition of "{term}":\n> ')
            if answer == definition[0]:
                self.print_and_add_to_log('Correct!')
            else:
                self.dic_flashcards[term][1] += 1
                if answer in [def_[0] for def_ in self.dic_flashcards.values()]:
                    term_for_answer = self.find_term_based_on_definition(answer)
                    self.print_and_add_to_log(f'Wrong. The right answer is "{definition[0]}", but your definition is '
                                              f'correct for "{term_for_answer}".')
                else:
                    self.print_and_add_to_log(f'Wrong. The right answer is "{definition[0]}".')

    def remove_card(self):
        card_to_remove = self.input_and_add_to_log('Which card?\n> ')
        if card_to_remove in self.dic_flashcards:
            del self.dic_flashcards[card_to_remove]
            self.print_and_add_to_log('The card has been removed.')
        else:
            self.print_and_add_to_log(f'Can\'t remove "{card_to_remove}": there is no such card.')

    def export_flashcards(self, filename):
        if not filename:
            filename = self.input_and_add_to_log('File name:\n> ')
        with open(filename, 'w') as json_file:
            json.dump(self.dic_flashcards, json_file)
        if len(self.dic_flashcards) == 1:
            self.print_and_add_to_log('One card has been saved.')
        else:
            self.print_and_add_to_log(f'{len(self.dic_flashcards)} cards have been saved.')

    def import_flashcards(self, filename):
        if not filename:
            filename = self.input_and_add_to_log('File name:\n> ')
        try:
            with open(filename, 'r') as json_file:
                imported_cards = json.load(json_file)
        except FileNotFoundError:
            self.print_and_add_to_log('File not found.')
            return False
        self.print_and_add_to_log(f'{len(imported_cards)} cards have been loaded.')
        self.dic_flashcards = {**self.dic_flashcards, **imported_cards}
        print(self.dic_flashcards)

    def print_and_add_to_log(self, output):
        print(output)
        self.log.append(output)

    def input_and_add_to_log(self, inp_text):
        inp = input(inp_text)
        self.log.append(inp_text + inp)
        return inp

    def save_log(self):
        filename = self.input_and_add_to_log('Filename:\n> ')
        self.print_and_add_to_log('The log has been saved.')
        with open(filename, 'w') as file:
            for line in self.log:
                file.write(line + '\n')

    def hardest_card(self):
        max_error = 0
        hardest_cards = []
        for term, definition in self.dic_flashcards.items():
            if definition[1] > max_error:
                hardest_cards = [term]
                max_error = definition[1]
            elif definition[1] == max_error and max_error > 0:
                hardest_cards.append(term)
        if hardest_cards:
            string = ''
            for card in hardest_cards:
                string += f'"{card}", '
            string = string.rstrip(', ')
            if len(hardest_cards) == 1:
                self.print_and_add_to_log(f'The hardest card is {string}. You have {max_error} errors answering it.')
            else:
                self.print_and_add_to_log(f'The hardest cards are {string}. You have {max_error} errors answering them.')
        else:
            self.print_and_add_to_log('There are no cards with errors.')

    def reset_stats(self):
        for term, definition in self.dic_flashcards.items():
            definition[1] = 0
        self.print_and_add_to_log('Card statistics has been reset.')

    def main(self):
        parser = argparse.ArgumentParser()  # I create instance parser of object ArgumentParser
        parser.add_argument('--import_from',
                            help='Imports flashcards from specified json file')  # I add optional argument
        parser.add_argument('--export_to', help='After typing "exit" the program exports all flashcards '
                                                'to specified json file')  # the same
        args = parser.parse_args()  # I use method parse_args to return the arguments a give them to args
        if args.import_from:
            self.import_flashcards(filename=args.import_from)
        while True:
            action = self.input_and_add_to_log('\nInput the action (add, remove, import, export, ask, exit, log, '
                                               'hardest card, reset stats):\n> ')
            if action == 'add':
                self.add_new_card()
            elif action == 'remove':
                self.remove_card()
            elif action == 'import':
                self.import_flashcards(filename=False)
            elif action == 'export':
                self.export_flashcards(filename=False)
            elif action == 'ask':
                self.ask_and_control()
            elif action == 'exit':
                print('Bye bye!')
                if args.export_to:
                    self.export_flashcards(args.export_to)
                exit()
            elif action == 'log':
                self.save_log()
            elif action == 'hardest card':
                self.hardest_card()
            elif action == 'reset stats':
                self.reset_stats()


flashcard = Flashcard()
flashcard.main()

