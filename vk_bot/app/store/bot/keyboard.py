import json


class KeyboardGame:

    def __init__(self):
        pass

    async def menu_in_start(self):
        
        # формирование интерактивных кнопок для меню

        buttons = [[{"action": {"type": "text", "label": "Правила игры"}}],
                   [{"action": {"type": "text", "label": "Начать игру" }}],
                   [{"action": {"type": "text", "label": "Турнирная таблица"}}]]
        
        keyboard = json.dumps({"inline": False, "buttons": buttons})
        
        return keyboard
    
    async def menu_in_game(self):
        
        # формирование интерактивных кнопок для меню

        buttons = [[{"action": {"type": "text", "label": "Правила игры"}}],
                   [{"action": {"type": "text", "label": "Стоп игра"}}],
                   [{"action": {"type": "text", "label": "Турнирная таблица"}}]]
        
        keyboard = json.dumps({"inline": False, "buttons": buttons})

        return keyboard
    

    async def question(self):
        
        # формирование интерактивных кнопок для ответа на вопрос

        buttons = [[{"action": {"type": "text", "label": "Ответить"}}],]
        
        keyboard = json.dumps({"inline": True, "buttons": buttons})

        return keyboard
    

    async def is_admin(self):
        
        # формирование интерактивных кнопок для ответа на вопрос

        buttons = [[{"action": {"type": "text", "label": "Назначен"}}],]
        
        keyboard = json.dumps({"inline": True, "buttons": buttons})

        return keyboard
    

    async def question_lap(self, questions):

        # формирование интерактивных кнопок
        buttons = []
        for question in questions:
            buttons.append([{"action": {"type": "callback", "label": question.title, "payload" : str(json.dumps({"type" : "title"}, ensure_ascii=False))}}])
            button = []
            points = question.points
            points.sort()

            for point in points[:-1]:
                button.append({"action": {"type": "text", "label": point, "payload" : str(json.dumps({"title" : question.title,
                                                                                                      "points" : point,
                                                                                                      "id" : question.id}, ensure_ascii=False))}})
            buttons.append(button)
        
        keyboard = json.dumps({"inline": True, "buttons": buttons})

        return keyboard
    

    async def question_lap_apdate(self, questions, points_list):

        # формирование интерактивных кнопок
        buttons = []
        for question in questions:
            buttons.append([{"action": {"type": "callback", "label": question.title, "payload" : str(json.dumps({"type" : "title"}, ensure_ascii=False))}}])
            button = []
            points = question.points
            points.sort()

            for point in points[:-1]:
                if point not in points_list[question.title]:
                    button.append({"action": {"type": "text", "label": point, "payload" : str(json.dumps({"title" : question.title,
                                                                                                        "points" : point,
                                                                                                        "id" : question.id}, ensure_ascii=False))}})
                else:
                    button.append({"action": {"type": "callback", "label": point,
                                               "payload" : str(json.dumps({"type" : "question"}, ensure_ascii=False))},
                                    "color": "primary"})
            buttons.append(button)
        


        keyboard = json.dumps({"inline": True, "buttons": buttons})

        return keyboard
    
        