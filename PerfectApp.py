import json
import random 

DATA_PATH = "./user_questions.json"

def get_prompt(message, list_of_posible_answers = ('y','n','yes','no')):
    user_answer = input(message).lower().strip()
    while user_answer not in list_of_posible_answers:
        user_answer = input('Votre reponse doit être entre '+ str(list_of_posible_answers))
    return user_answer       

class Question: 
    number_of = 0
    reponse_juste = ''
    reponse_fause = ''
    def __init__(self, intitule, list_of_possible_answers, list_of_another_answers):
       self.intitule = intitule
       self.list_of_possible_answers = list_of_possible_answers
       self.list_of_another_answers = list_of_another_answers 
       self.number_of += 1
       
    def get_intitule(self):
        return self.intitule
    
    def get_list_of_possible_answers(self):
        return  self.list_of_possible_answers
    
    def get_list_of_another_answers(self):
        return self.list_of_another_answers 
    
    def get_list_with_one_answer( self):  
        list_of_possible_answer = self.get_list_of_possible_answers()  
        rand = random.choice(list_of_possible_answer) 
        list_with_one_correct_answer =[rand]  

        while len(list_with_one_correct_answer) < 4:
            list_of_another_town = random.sample(self.get_list_of_another_answers(), 3)
            for town in list_of_another_town:
                if (town not in list_with_one_correct_answer) and ( town not in list_of_possible_answer):
                    list_with_one_correct_answer.append(town)   
        return random.sample(list_with_one_correct_answer, 4)
    
    def get_index_of_good_answer(self, list_with_one_answer):
        for items in list_with_one_answer:
            if items in  self.get_list_of_possible_answers():  
                return list_with_one_answer.index(items) + 1 
            
    def number_of_questions(self) :
        return self.get_index_of_good_answer(self.get_list_with_one_answer() )
    
    def is_it_correct_answer(self,list_of_possible_answers, list_wtih_one_answer,user_answer):   
        return (user_answer in list_of_possible_answers and user_answer in list_wtih_one_answer)
   
    def build_score(self): 
        print('------------------------')
        list_wtih_one_answer =  self.get_list_with_one_answer() 
        print(self.get_intitule())
        _number = self.get_index_of_good_answer(list_wtih_one_answer) 
        self.reponse_juste += f" : {list_wtih_one_answer[_number - 1]}"
        for i in range(1,len(list_wtih_one_answer) + 1):
            print(i,'-',list_wtih_one_answer[i - 1])
            
        user_answer = str(input('Entrez votre reponse : ') ).strip(" ,:());'/-.")
        print('------------------------') 
        if self.is_it_correct_answer( self.get_list_of_possible_answers() , list_wtih_one_answer, user_answer) or  user_answer == str(_number) : 
            counter_score = 3  
            print('Vrai')
        else: 
            counter_score = - 1 
            if user_answer.isdigit() and int(user_answer) > len(list_wtih_one_answer)-1: 
                print ("cette entrée n'existe pas") 
                user_answer = 0
                self.reponse_fause += f" : {list_wtih_one_answer[int(user_answer) -1]}"
            else: 
                self.reponse_fause += f" : {user_answer}" 
            print("Faux")  
        return counter_score
    
class Fichier(Question):
    def __init__(self, file_name, intitule= None, list_of_possible_answers= None, list_of_another_answers= None):
        super().__init__(intitule, list_of_possible_answers, list_of_another_answers)
        self.file_name = file_name 
      
    def read_in_data_file(self): 
        try:
            with open(self.file_name,'r', encoding="utf8") as file:
                data = json.load(file)
                file.close()
            return data 
        except FileNotFoundError:
            print(output_information('On ne peu ecrire dans votre fichier'))
    
    def __str__(self) :
        return f"Vous avez au total {len( self.read_in_data_file()) } questions"
     
    def write_in_data_file(self, data): 
        with open(self.file_name, 'w',encoding="utf8") as file:
            json.dump(data, file, indent = 4, ensure_ascii = False, sort_keys = True )  
            file.close()  
        
    def get_list_of_existing_question(self):
        list_of_question = []   
        try:
            for question in self.read_in_data_file(): 
                list_of_question.append(question) 
            return list_of_question  
        except TypeError : 
            print(output_information('Votre fichier ne peu être lu'))
            
def push_in_data_file(question,data_path): 
    _dict = {}
    intitule = input("entrez l'intitulé de la question ")
    list_of_correct_answers = input("Entrez les reponses juste séparées par des virgule \n").split(',')
    list_of_an_order_answers =  input("Entrez d'autres reponses séparées par des virgule \n").split(',')
    
    _dict['intitule'] = intitule
    _dict['list_of_correct_answers'] = list_of_correct_answers
    _dict['list_of_an_order_answers'] = list_of_an_order_answers 
    
    if _dict.values():
        fichier = Fichier(data_path, intitule, list_of_correct_answers, list_of_an_order_answers) 
        existing_data = fichier.read_in_data_file() 
        if question not in fichier.get_list_of_existing_question():
            existing_data[question] = [_dict]
            fichier.write_in_data_file(existing_data)
            print(output_information("enregistré avec succès"))
            return True 
        
        existing_data[question].append(_dict) 
        fichier.write_in_data_file(existing_data)   
        print(output_information("enregistré avec succès"))
    else:
        print(output_information(f"An error has occur \n Vous avez surement mal renseignez un champ ou alors vérifiver le chemin vers fichier"))

def display_quiz(question,data_path):
    score = 0
    fichiers = Fichier(data_path) 
    data_list = fichiers.read_in_data_file()[question]
    length_of_list = len(data_list) 
    print(f"Vous avez {length_of_list} Au total") 
    data_random_list = random.sample(data_list, length_of_list)  
    result_set = ""
    
    for datum in data_random_list: 
        intitule = datum['intitule']
        list_of_correct_answers = datum['list_of_correct_answers']
        list_of_an_order_answers = datum['list_of_an_order_answers']
        fichier = Fichier(data_path, intitule, list_of_correct_answers, list_of_an_order_answers)  
        score += fichier.build_score()  
        result_set += f"{fichier.get_intitule()}\t{fichier.reponse_fause} \t{fichier.reponse_juste}\n"
    if score < 0:
        score = 0 
        
    return output_information(f"On {len(data_random_list)} questions asked\nyou have  {score} / {len(data_random_list)*3} points\nReponses justes : \n{(result_set)}")

def output_information(message): 
    string_mesasage = (f"\n-------------------IDRIS GAME-------------------\n{message}\n------------------------------------------------  ")
    return string_mesasage

def existing_solutions(data_path):
    print()
    print(output_information("Une question trouvée donne 3 points \nUne question faussée soustrait 1 point"))
    fichier = Fichier(data_path).get_list_of_existing_question() 
    return f"Sujets déjà disponibles {fichier}"
    
def play_action(fichier, data_path):
    print(existing_solutions(data_path))
    user_answer = ((input("Entrez le sujet de votre jeu: ")).lower()).strip(" ',;")
    while user_answer not in fichier:
        print (output_information("Ce sujet n'existe pas encore"))
        print(existing_solutions(data_path))
        user_answer = (input("Entrez le sujet de votre jeu: ")).lower()
    print(display_quiz(user_answer, data_path))

def relancer_le_jeu(data_path):
    is_launch = True
    while is_launch: 
        fichier = Fichier(data_path).get_list_of_existing_question() 
        if fichier == None:
            return False  
        
        if  get_prompt('Voulez-vous jouez [Y - N]: ') in ('y','yes'): 
            play_action(fichier, data_path ) 
            replay_action = get_prompt("Voulez-vous rejouez [Y-N] ")
            while replay_action in ('y','yes'):
                play_action(fichier, data_path) 
                replay_action = get_prompt("Voulez-vous rejouez [Y-N] ") 
            if replay_action in ('n','no'):
                print (output_information("Merci d'avoir éssayé ce jeu"))
                is_launch = False 
                input("Apuyez la touche entrée de votre clavier pour sortir")
               
        else:
            print(output_information("Vous êtes en train de vouloir concevoir une question"))
            print(existing_solutions(data_path))
            user_answer = input('Entrez le sujet de votre jeu: ').lower()
            if user_answer not in fichier:
                print(output_information( "Vous voulez créer votre Quiz"))
            push_in_data_file(user_answer,data_path)
            replay_action = get_prompt("Voulez-vous inserer à nouveau  [Y-N] ")
            while replay_action in ('y','yes'):
                push_in_data_file(user_answer, data_path)
                replay_action = get_prompt("Voulez-vous inserer à nouveau  [Y-N] ")
            if replay_action in ('n','no'):
                is_launch = True 
if __name__ == '__main__': 
    print(output_information(f"Jouez et concevez votre propre Quiz \nEntrer : \nY - Pour jouer \nN - Pour concevoir vos Quiz")) 
    if get_prompt("Would you want to provide your own json file ? ") in ("y","yes") : 
        print("C:/Users/Idris/Desktop/user_question.json")
        user_path = input("enter the path of your json file : ") 
        new_path = relancer_le_jeu(user_path)
        while new_path == False:
            user_path = input("enter the best path of your json file : ") 
            relancer_le_jeu(user_path)
            
    else: 
        try:
            print(output_information("Vous utilisez le fichier par défaut !"))
            relancer_le_jeu(DATA_PATH)
        except FileNotFoundError:
            print(output_information('Vous avez modifier le chemin du fichier par defaut !'))
