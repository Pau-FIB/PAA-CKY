from typing import Dict, List, Set, Tuple, Union
from copy import deepcopy

class Gramatica():
    def __init__(self, normes_gramatica: Set, simbol_arrel: str = 'S') -> None:
        self.gramatica = deepcopy(normes_gramatica)
        self.regles_binaries = self._preprocessar_regles_binaries()
        self.simbol_arrel = simbol_arrel
        
    def algoritme_cky(self, frase: Union[List[str], str]) -> bool:
        """
        Analitza una frase gramaticalment utilitzant l'algoritme CKY.
        Omple la taula dinàmica de CKY amb la frase donada.
        :param frase: Es tracta de la cadena que volem analitzar.
        :return: Retorna un boolean que inidica si la cadena es pot derivar o no.
        """
        
        if not frase:
            # Comprovem si la cadena buida és derivable (S -> ε)
            return self._comprovar_derivacio_buida()
        
        n = len(frase)
        # Crear tabla como diccionario - CORREGIDO
        taula = [[set() for _ in range(n)] for _ in range(n)]

        # Omplim la primera fila (cas base): terminals
        for col in range(n):
            paraula = frase[col]
            for no_terminal, produccions in self.gramatica.items():
                for produccio in produccions:
                    # Comprovem les produccions terminals (A -> a)
                    if len(produccio) == 1 and produccio[0] == paraula:
                        taula[col][col].add(no_terminal)
        
        # Omplim la resta de la taula (longitud 2 a n)
        for n_fila in range(1, n):  # longitud de la subcadena
            for diag in range(n - n_fila):
                col = diag + n_fila

                # Provem totes les possibles divisions de la subcadena
                for k in range(n_fila):
                    part_diag = taula[diag][diag + k]
                    part_col = taula[diag + k + 1][col]
                    # Si alguna de les dues parts és buida, no podem continuar
                    if not part_diag or not part_col:
                        continue
                    
                    # Comprovem totes les regles de la gramàtica per produccions binàries
                    for no_terminal_diag in part_diag:
                        for no_termina_col in part_col:
                            # Comprovem les produccions binàries (A -> BC)
                            clau = (no_terminal_diag, no_termina_col)
                            if clau in self.regles_binaries:
                                taula[diag][col].update(self.regles_binaries[clau])

        return self.simbol_arrel in taula[0][n-1]
                
    def _preprocessar_regles_binaries(self) -> Dict[Tuple[str, str], Set[str]]:
        """ 
        Preprocessa la gramàtica per accés ràpid a les regles binàries.
        Aquesta funció crea un diccionari on les claus són tuples (esq, dre) i els valors són conjunts de no-terminals.
        """
        regles_binaries = {}  # Diccionari on (esq, dre) -> {no_terminal}
        
        for no_terminal, produccions in self.gramatica.items():
            for produccio in produccions:
                if len(produccio) == 2:  # Només regles binaries
                    clau = (produccio[0], produccio[1])
                    if clau not in regles_binaries:
                        regles_binaries[clau] = set()
                    regles_binaries[clau].add(no_terminal)

        return regles_binaries
    
    def _comprovar_derivacio_buida(self) -> bool:
        """ 
        Comprova si la cadena buida és derivable a partir del símbol d'inici. 
        """
        if self.simbol_arrel in self.gramatica:
            for produccio in self.gramatica[self.simbol_arrel]:
                if len(produccio) == 1 and produccio[0] in ['ε', '']:
                    return True
        return False    

    def __str__(self):
        """
        Retorna una representació en forma de cadena de la gramàtica.
        """
        return "\n".join(
            f"{no_terminal} -> {', '.join(' '.join(map(str, produccio)) for produccio in produccions)}"
            for no_terminal, produccions in self.gramatica.items()
        )