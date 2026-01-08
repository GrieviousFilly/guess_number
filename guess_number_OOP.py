from random import randint


def is_admin(func):
    def wrapper(obj, name):
        if name == 'Admin':
            result = func(obj)
            return result
        else:
            return 'Не понимаю.. Дай корректный ответ, пж.'

    return wrapper


class Game:
    greeting = """
Привет! Давай сыграем в игру 'Угадай число'.
Правила просты, я загадываю целое число от 1 до 100,
а ты попробуй угадать его за пять попыток.\n"""

    def __init__(self):
        self.guessed_number = None
        self.played_games = 0
        self.player_wins = 0
        self.robot_wins = 0
        self.tries = 5
        self.name = None

    def guess_number(self):
        self.guessed_number = randint(1, 100)
        return self.guessed_number

    def preparation(self):
        print(self.greeting)
        while True:
            if self.guessed_number is None:
                self.guess_number()
            ready = input('\nГотов играть? (Yes|Y/ No|N): ')
            match ready.lower():
                case x if x in ['yes', 'y']:
                    self.play()
                case x if x in ['no', 'n']:
                    break
                case 'stats':
                    print(self.stats(self.name))
                case 'answer':
                    print(self.answer(self.name))
                case 'settings':
                    print(self.set_settings(self.name))
                case 'admin':
                    self.name = ready.capitalize()
                case _:
                    print('Не понимаю.. Дай корректный ответ, пж.')

    def play(self):
        self.played_games += 1
        while True:
            try:
                guess = int(input('Введите число: '))
                if guess < 1 or guess > 100:
                    raise ValueError
            except ValueError:
                print('Нужно ввести число от 1 до 100')
            else:
                self.tries -= 1
                if self.check_winner(guess):
                    break

    def check_winner(self, number):
        # Нужно добавить проверку количества попыток и учет побед робота
        match number:
            case self.guessed_number if self.tries > 0:
                print('Угадал! Победа за тобой..')
                self.guessed_number = None
                self.tries = 5
                self.player_wins += 1
                return True
            case x if self.tries == 0:
                print(
                    'Твои попытки закончились, ты не угадал, я победил! '
                    f'Загаданное число было {self.guessed_number}'
                )
                self.robot_wins += 1
                self.tries = 5
                self.guessed_number = None
                return True
            case x if x < self.guessed_number:
                print('Я загадал число больше :)')
            case x if x > self.guessed_number:
                print('Я загадал число меньше :)')
        return False

    @is_admin
    def stats(self):
        return (
            f'Всего сыграно: \t{self.played_games}\n'
            f'Твоих побед: \t{self.player_wins}\n'
            f'Я победил: \t{self.robot_wins}'
        )

    @is_admin
    def answer(self):
        return f'Загаданное число: {self.guessed_number}'

    @is_admin
    def set_settings(self):
        self.tries = int(input('Введите количество попыток: '))
        return (
            'Настройки успешно сохранены, '
            f'теперь количество попыток: {self.tries}'
        )


if __name__ == '__main__':
    game = Game()
    game.preparation()
