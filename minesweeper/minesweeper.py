import itertools
import random
import copy

#replacing copy.deepcopy() with .copy() and replacing repeating code with a funciton
class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if(len(self.cells)==self.count):
            return self.cells
        else:return 0

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if(self.count==0):
            return self.cells
        else:return 0

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)




class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        #set of cells for one sentence
        c=set()
    
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds 
                if 0 <= i < self.height and 0 <= j < self.width and (i,j) not in self.moves_made:
                    c.add((i,j))

        sentence=Sentence(c,count)
        self.knowledge.append(sentence)
        #make a function for this garbage
        for s in range(len(self.knowledge)):
            temp=0
            if(len(self.knowledge)==0): break
            if(self.knowledge[s].known_safes()): 
                temp_copy1=copy.deepcopy(self.knowledge[s].known_safes())
                for i in temp_copy1:
                    temp=1
                    self.mark_safe(i)
                if(temp):
                    s=-1
                    continue
            elif(self.knowledge[s].known_mines()):
                temp_copy2=copy.deepcopy(self.knowledge[s].known_mines())
                for i in temp_copy2:
                    self.mark_mine(i)
                if(temp):
                    s=-1
                    continue

        length_of_knowledge=len(self.knowledge)
        i=0
        while(i<length_of_knowledge):
            if self.knowledge[i].cells==set():
                self.knowledge.remove(self.knowledge[i])
                i-=1
                length_of_knowledge-=1
            i+=1
            
        knowledge_copy=[]
    
        #making inferences in knowledge base
        if(len(self.knowledge)>1):
            for s1 in self.knowledge:
                s2=self.knowledge[-1]
                if(s1.cells!=s2.cells):
                    temp_num=0
                    if(s2.cells.issubset(s1.cells)):
                        temp_sentence=s1.cells-s2.cells
                        temp_count=s1.count-s2.count
                    elif(s1.cells.issubset(s2.cells)):
                        temp_sentence=s2.cells-s1.cells
                        temp_count=s2.count-s1.count  
                    else: continue                     
                    if(len(temp_sentence)==0): continue
                    # check for repetition
                    for i in self.knowledge: 
                        if i.cells == temp_sentence: 
                            temp_num=1
                            break
                    if(temp_num): continue
                    else:
                        knowledge_copy.append(Sentence(temp_sentence,temp_count))
                        #print(s1.cells,"-",s1.count,"  <-->  ",s2.cells,"-",s2.count,"  inference->  ",temp_sentence,"-",temp_count)

        self.knowledge.extend(knowledge_copy)
        for s in range(len(self.knowledge)):
            temp=0
            if(len(self.knowledge)==0): break
            if(self.knowledge[s].known_safes()): 
                temp_copy1=copy.deepcopy(self.knowledge[s].known_safes())
                for i in temp_copy1:
                    self.mark_safe(i)
                if(temp):
                    s=-1
                    continue
            elif(self.knowledge[s].known_mines()):
                temp_copy2=copy.deepcopy(self.knowledge[s].known_mines())
                for i in temp_copy2:
                    self.mark_mine(i)
                if(temp):
                    s=-1
                    continue
        length_of_knowledge=len(self.knowledge)
        i=0
        while(i<length_of_knowledge):
            if self.knowledge[i].cells==set():
                self.knowledge.remove(self.knowledge[i])
                i-=1
                length_of_knowledge-=1
            i+=1

        for i in self.knowledge:
            print(i.cells," - ",i.count)

        for i in (self.safes-self.moves_made):
            print("safe-->  ",i,end=" - ")
        print(end="\n")
        for i in self.mines:
            print("mines-> ",i,end=" - ")
        print(end="\n")


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                print("MOVE-", cell)
                print("-----------------")
                return cell 
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        lst=[]
        for i in range(0,self.height):
            for j in range(0,self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    lst.append((i,j))
        if(lst!=[]): 
            cell=random.choice(lst)
            print("MOVE-", cell)
            print("------------------")
            return cell
        else: return None
