class Messages:

    def __init__(self):
        pass

    async def game_rules(self):
        
        one = "1. Бот перед началом игры показывает список всех возможных тем и вопросов для выбора."
        two = "2. Бот рандомно выбирает пользователя, который будет ходить первым."
        three = "3. Пользователь выбирает тему и баллы, которые будут начисленны в случае правильного ответа."
        four = '4. Пользователь, который раньше остальных нажмет на кнопку "Ответить" - будет называть свой вариант ответа.'
        five = "5. В случае если ответ был верный, - пользователю будет начислены баллы и предоставлено право выбрать следующий вопрос. \
                В случае неправильного ответа баллы будут списаны со счета игрока, и ход перейдет другому игроку. \
                Игра идет до тех пор, пока не останется ни одного вопроса"
        text = f"Своя игра%0a%0a{one}%0a{two}%0a{three}%0a{four}%0a{five}"

        return text

    
    async def answer_action(self, player):

        user = player.first_name + " " +   player.last_name
        
        text = f"Отвечает%0a{user}"

        return text
    

    async def answer_true(self, points):
    
        text = f"Правильно%0a%0a{str(points)} очков"

        return text
    

    async def answer_false(self, points: int):
        
        text = f"Не правильно.%0a%0a{str(points)} очков"

        return text


    async def start_game(self):
        
        text = 'Для начала игры%0aкликнуть "Начать игру"%0a%0a'

        return text
    
    async def themes(self, theme_titles):

        themes = "".join([theme.title + "%0a" for theme in theme_titles])

        text = f"Темы игры%0a%0a{themes}"

        return text
        
    async def is_admin(self):

        text = 'Назначьте "Своя игра"%0aадмином общего чата%0a%0aПосле этого кликнуть "Назначен"%0a%0a'

        return text
    
    async def select_question(self, player):

        text = f"{player.first_name} {player.last_name}%0aВыбирайте вопрос игры"

        return text
    
    async def game_leader_board(self, leader_board):

        text_board = [[f"{val.first_name} {val.last_name}", "|", val.points + "%0a"] for val in leader_board]
        
        text_board = [" ".join(board) for board in text_board]

        
        text = "Турнирная таблица%0a" + \
        "____________________________%0a" +  \
        "".join(text_board)

        return text
    

    async def end_game(self):

        text = "Игра завершена%0a%0aЭто была хорошая игра%0a%0aЖдём вас снова"

        return text
