from typing import Iterator, List
from itertools import chain

class Comments:

    def __init__(self, iter_connections:Iterator[str], parts_expr:List[str]):
        self.iter_connections = iter_connections
        self.parts_expr = parts_expr

    def generate(self) -> Iterator[str]:

        '''

        Generates every comment from an expression and a list of connections

        '''

        last_part = self.parts_expr[-1]

        while True:

            if len(self.parts_expr) == 1:
                yield last_part

            else:

                try:

                    users = next(self.iter_connections)
                except StopIteration:
                    return

                comment = ''.join(chain.from_iterable(zip(self.parts_expr, users)))

                yield (comment + last_part).replace(r'\@', '@')
