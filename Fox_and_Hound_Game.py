from colorama import Fore, Style, init # Pour colorer le texte dans le terminal
init(autoreset=True)

class gameBoard:
    def __init__(self, size=8):
        self.size = size
        self.__initialize_board(size) # Ici j'appelle la méthode 'initialize_board' pour initialiser le plateau
        self.__place_pieces() # Ici j'appelle la méthode 'place_pieces' pour initialiser le plateau et les positions des pions
        
    def __initialize_board(self, taille): # C'est une méthode
        self.liste = []
        self.taille = taille
        if self.taille % 4 != 0 : # Au cas ou la taille passer par l'utilisateur n'est pas un multiple de 4
            for i in range(5):
                self.taille += 1
                if self.taille % 4 == 0:
                    break # Si c'est un multiple de 4 on sort du for
                #break
        self.board = [[0 for _ in range(self.taille)] for _ in range(self.taille)] # '_' est juste une juste une var (c'est pas une var de boucle)
        self.fox_position = (self.taille-1 , int(self.taille / 2 + 1)-1) # Je donne les coordonnes du renard
        #self.board[self.fox_position[0]][self.fox_position[1]] = -1 # Attention dans le 'self.fox_position(1)' comme tu met les parenthèse , il pense que tu appelle une fonction! Alrors que toi tu vas chercher des élements d'un tuple! Donc tu mets des '[]' pour acceder aux elements d'une liste ou d'un tuple!
        self.hound_positions = [(0, i) for i in range(1, self.taille+1, 2)] # J'initialise les coordonnées des chiens qui sont à par exemples : board[0][1], puis le suivant est à board[0][3] etc.. c'est ce que j' enregistre sous forme de tuple
        #print(self.hound_positions)
        
        
    def __place_pieces(self): # C'est une méthode
        x, y = self.fox_position
        self.board[x][y] = -1 # Place le renard
        for i in range(len(self.hound_positions)):
            self.board[0][self.hound_positions[i][1]] = i + 1 # Ici je modifie les élements de la 1ere lignes pour les élements comme ..[0][1], ..[0][3], ..[0][5] etc... C'est pour ca que je vais voir les 2ièmes élements de ma liste de tuple et je modifie les élements de 'board' correspondant par la valeur de i+1 qui s'incrémente à chaque boucle
            self.liste.append(i+1) # Cette liste sera utile plus tard pour verifier le choix du joueur par rapport au numéro du chien avec ceux possible

    def _display(self): # Pareil ici, c'est une méthode
        for i in range(self.taille):
            for j in range(self.taille):
                if self.board[i][j] == 0 or self.board[i][j] == '.':
                    print('.', end=' ')
                elif self.board[i][j] in self.liste : # Ici je remplace la var de type int en string
                    print(Fore.RED + f'{self.board[i][j]}'  + Style.RESET_ALL, end=' ')
                elif self.board[i][j] == -1:
                    print(Fore.BLUE + 'W' + Style.RESET_ALL, end=' ')
            print("")
     
    def getValuue(self,i,j): # Pour l'encapsulation
        return self.board[i][j]
    
    def setValue(self,i,j,val): # Pour l'encapsulation
        self.board[i][j] = val

class hound:
    def __init__(self, i=0, j=0):
        #gameBoard.__init__(self,4, )
        self.__abscisse = i # Ce sont des var privés on ne peut pas les changer ni avoir accès en dehors de la classe,d'ou la présence des '__'
        self.__ordonne = j

    def getValueHound(self): # Pour l'encapsulation
        return self.__abscisse, self.__ordonne
    
    def setValueHound(self, k, l): # Pour l'encapsulation
        self.__abscisse = k
        self.__ordonne = l

    def _canMoveTo(self, board): 
        new_i, new_j = hound.getValueHound(self) # Pas besoin de lui donner des para de coordonnées, car lors de l'appel de la méthode en dehors de la class, on aura deja determiner le chien avec lequel on veut voir les mouvements et ces coordonnées seront 'automatiquement' fourni en même temps que l'appel de la méthode (celle si se paser un peu comme ca : hound_objet1._methode(para) <- les coordonnées sont dans l'objet de class 'hound' créer dans la liste de hound créer) 
        directions = [(1, -1), (1, 1)]  # Mouvement diagonal vers le bas gauche et bas droite
        for di, dj in directions:
            new_i1 = new_i + di # On ajoute ces éventuelles mouvements possibles du chien
            new_j2 = new_j + dj
            if 0 <= new_i1 < len(board) and 0 <= new_j2 < len(board): # On regarde si ils sont a l'interieur du plateau
                if board[new_i1][new_j2] == 0:  # Vérifie si la case est vide
                    return True
        return False
    
    def _move(self, board):
        directions = [(1, -1), (1, 1)]  # Mouvement diagonal vers le bas gauche et bas droite
        while True:
            try:
                print("Which row ? ")
                choice = int(input()) - 1
                print("Which column ? ")
                choice1 = int(input()) - 1
                for di, dj in directions:
                    new_i, new_j = hound.getValueHound(self) # J'ai creer ces var temporaire pour ne pas modifier les coordonnées du renard avant de vérifier si le mouvement est valide
                    new_i, new_j = new_i + di, new_j + dj
                    if self._canMoveTo(board) and new_i == choice and new_j == choice1 and board[new_i][new_j] == 0: # Regarde si les choix de l'utilisateur correspondent à un mouvements possible
                        var_temp1, var_temp2 = hound.getValueHound(self) # Sauvegarde les coordonnées actuelles du chien 
                        varTemp = board[var_temp1][var_temp2] # Sauvegarde la valeur actuelle   
                        board[var_temp1][var_temp2] = 0  # Vide la case actuelle
                        hound.setValueHound(self, new_i, new_j) # Met à jour les coordonnées du chien
                        board[new_i][new_j] = varTemp  # Place le pion à la nouvelle position
                        return False
                return True
            except ValueError:
                print("Veuillez entrer un nombre valide.")
    

class fox(hound): # La classe 'fox' hérite de la classe 'hound', donc elle a accès à toutes ses méthodes et attributs. Je le fait pratiquement en écrivant class 'nom de la classe'(nom de la classe dont elle hérite)
    def __init__(self, d=0, e=0):
        self.__abscisse_fox = d # Pour l'encapsulation
        self.__ordonne_fox = e
    
    def getValueFox(self): # Pour l'encapsulation
        return self.__abscisse_fox, self.__ordonne_fox
    
    def setValueFox(self, m, n): # Pour l'encapsulation
        self.__abscisse_fox = m
        self.__ordonne_fox = n

    def _canMoveTo1(self, board): 
        new_i1, new_j2 = fox.getValueFox(self) # Pas besoin de lui donner des para de coordonnées, car la position du renard est déjà définie lors de l'initialisation de la classe 'fox'. Et en plus je le met à jour à chaque tour en utilisant le 'setValueFox()'.
        directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]  # Mouvement diagonal vers le bas gauche et bas droite et haut droite et haut gauche
        for di, dj in directions:
            self.new_i1 = new_i1 + di 
            self.new_j2 = new_j2 + dj
            if 0 <= self.new_i1 < len(board) and 0 <= self.new_j2 < len(board):
                if board[self.new_i1][self.new_j2] == 0:  # Vérifie si la case est vide
                    return True
        return False
    
    def _move1(self, board):
        directions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]  # Mouvement diagonal vers le bas gauche et bas droite et haut gauche et haut droite
        while True:
            try:
                print("Which row ? ")
                choice = int(input()) - 1
                print("Which column ? ")
                choice1 = int(input()) - 1
                var_temp_fox_i, var_temp_fox_j = fox.getValueFox(self) # J'ai creer ces var temporaire pour ne pas modifier les coordonnées du renard avant de vérifier si le mouvement est valide0
                for di, dj in directions:
                    new_i = var_temp_fox_i + di
                    new_j = var_temp_fox_j + dj
                    if fox._canMoveTo1(self, board) and new_i == choice and new_j == choice1 and board[new_i][new_j] == 0: # Ici je dois appeler la méthode '_canMoveTo1' de la class 'fox', donc je l'appelle en écrivant 'fox._canMoveTo1(self, board)' car si j'écris juste 'self._canMoveTo1(board)', il va chercher la méthode dans la class 'foxAndHounds' (car je suis dans cette class actuellement) et il ne la trouvera pas! Donc je précise que je veux la méthode de la class 'fox'
                        varTemp = board[var_temp_fox_i][var_temp_fox_j] # Sauvegarde la valeur actuelle    
                        board[var_temp_fox_i][var_temp_fox_j] = 0  # Vide la case actuelle
                        fox.setValueFox(self, new_i, new_j) # Met à jour les coordonnées du renard et je passe par le 'fox' car j'appelle la méthode à l'interieur de la class 'fox' (donc je dois préciser que je veux la méthode de la class 'fox')
                        board[new_i][new_j] = varTemp  # Place le pion à la nouvelle position
                        return False
                return True
            except ValueError:
                print("Veuillez entrer un nombre valide.")
    
    def win(self):
        var_temp_x, var_temp_y = fox.getValueFox(self) # Je recupere les coordonnées du renard
        if var_temp_x == 0:
            return True
        return False


class foxAndHounds(gameBoard, fox, hound):
    def __init__(self, size=8):
        gameBoard.__init__(self, size) # Initialisation du plateau de jeu et acces aux instances de la class 'gameBoard', comme tu initialise, tu donne le nom de la classe (et apres dans ta classe, si tu veux accéder aux méthodes des autres classes, tu fais 'self.' cartu auras deja initialiser la classe 'cible' àl'intérieur de ta classe actuelle)
        fox.__init__(self, self.fox_position[0], self.fox_position[1]) # Initialisation de la position du renard si tu ne l'initialise pas lecode ne passera jamais dans la class 'fox'
        self.hounds = [hound(i, j) for i, j in self.hound_positions] # Lorsque je créer une liste de objets 'hound', pour s'initialiser, il a besoin de para (i,j) donc je lui fourni les positions des hounds, et quand j'appelle un objet declass hound de la liste, sa position est deja defini (il est deja crer, donc à ces para sinon il n'aurait pas pu etre creer en premiere lieu)

    def FoxAndHounds(self):
        while True:
            var_condition = True
            self._display()
            print("Fox's turn: (W)")
            while var_condition: # la méthode '_move' de 'fox' renvois un True ou False, c'est ce qui permet de demander en boucle le 'Which row ?' et le 'Which column ?' tant que le renard peut bouger
                var_condition = self._move1(self.board) # Le pb avec cette écriture : 'fox._move(self.board)' c'est que j'appelle la méthode '_move' sur la classe 'fox' au lien de sur L'INSTANCE!! (car tu est en dehors de la class 'fox'!!) En fait t'appelle la méthode '_move' (qui est dans une autre classe), et donc j'imagine tu dois utiliser le 'self.' car dans le '__init__' de la classe actuelle, tu fais 'fox.__init__' et donc tu viens de l'initialiser et donc il faut que tu utilise le 'self' (à cause de l'initialisation) Et comme t'a fait en sorte de initialiser la class 'fox' et que la class 'foxAndHounds' tu peux simplement appeler les méthodes des autres class simplement en écrivant : 'self' devant. Et comme il n'y a que un renard, tu peux directement appeler la méthode (celle ci aussi a besoin de coordonnes) mais du coup elle n'a les coordonnées que pour un seul objet de classe 'fox' qui a été initialser au début dans le '__init__' de la class actuelle
            self._display()
            if self.win(): # regarde si le renard a gagné, si c'est le cas, sors du while
                print("Fox wins!")
                break

            print("Hounds' turn: (Red numbers)")
            var_condition1 = True
            var_condition2 = True
            while var_condition1:
                try: 
                    print("Choose a hound : (enter the number) ")
                    choice3 = int(input())
                    for _ in range(len(self.liste)): # Je parcours la liste des hounds (qui est une liste de nombre)
                        if choice3 == self.liste[_] : # Je regarde si le choix du joueur correspond à un hound sur le plateau
                            if self.hounds[choice3-1]._canMoveTo(self.board): # Je verifie si le hound choisi peut bouger
                                print(f"Hound n°{choice3} to move : ")
                                while var_condition2:
                                    var_condition2 = self.hounds[choice3-1]._move(self.board) # J'appelle la méthode '_move' à partir du hounds choisi (vois ca plutot comme si tu appeler l'objet de classe 'hounds' (n° quelquonque) et tu veux lui appliquer la méthode '_move' donc automatiquement dans cette méthode comme elle a besoin des coordonnées du hound, elle prendra celle du hound à laquelle tu applique)
                                var_condition1 = False
                except ValueError:
                    print("Veuillez entrer un nombre valide.")
            if not self._canMoveTo1(self.board): # regarde si le renard peut encore bougé, si ce n'est pas le cas, les chiens ont gagné et sors du while
                self._display()
                print("Hounds win!")
                break

        print("Game over.")
    

plateau = 4
jeu1 = foxAndHounds(plateau) # Je créer l'objet de class 'foxAndHounds'
jeu1.FoxAndHounds() # J'appel la méthode 'FoxAndHounds' qui fait tourner le jeu