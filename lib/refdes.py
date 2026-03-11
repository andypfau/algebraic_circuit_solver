from .types import RefdesType
import re



class RefdesDatabase:


    def __init__(self):
        self._refdes: set[RefdesType] = set()
    

    def register_redes(self, refdes: RefdesType):
        if not re.match(r'[a-zA-Z]+[0-9]*', refdes):
            raise ValueError(f'Invalid refdes "{refdes}"')
        if refdes in self._refdes:
            raise RuntimeError(f'Duplicate refdes: "{refdes}"')
        self._refdes.add(refdes)


    def get_new_refdes(self, prefix: str = 'X') -> RefdesType:
        num = 1
        while True:
            refdes = f'{prefix}{num}'
            if refdes not in self._refdes:
                self.register_redes(refdes)
                return refdes
            num += 1
