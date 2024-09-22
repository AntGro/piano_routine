from __future__ import annotations

from enum import Enum
from typing import Any

import numpy as np
import pandas as pd
import tqdm
from pydantic import BaseModel


class Composer(str, Enum):
    CZERNY = "Czerny"
    GURLITT = "Gurlitt"
    CHOPIN = "Chopin"
    PETZOLD = "Petzold"
    NYMAN = "Nyman"
    BARTOK = "Bartok"
    SIBMOL = "Sibmol"
    SIBMOL_LEMOINE = "Sibmol / Lemoine"
    CORELLI = "Corelli"
    DIABELLI = "Diabelli"
    WITTHAUER = "Witthauer"
    BACH = "Bach"
    WOOK = "Wook"
    PAGANINI = "Paganini"
    DOUGAN = "Dougan"
    ELFMAN = "Elfman"
    HUMMEL = "Hummel"
    KOZELUCH = "Kozeluch"
    SCHUMANN = "Schumann"
    CLEMENTI = "Clementi"
    BEETHOVEN = "Beethoven"
    MOZART = "Mozart"
    BURGMULLER = "Burgmüller"
    ZIPOLO = "Zipoli"
    CHIZAT = "Chizat"
    BIZET = "Bizet"
    SHUBERT = "Shubert"
    TCHAIKOVSKI = "Tchaikovski"
    VERDI = "Verdi"
    HOWARD_EMERSON = "Howard & Emerson"
    JOPLIN = "Joplin"
    GERSHWIN = "Gershwin"
    NONE = ""


def spaced_ones_indices(k: int, n: int) -> np.ndarray:
    return np.round(np.arange(k) / k * n + np.random.randint(0, n)).astype(int) % n


class Piece(BaseModel):
    composer: Composer
    chapter: int
    title: str
    module: float
    submodule: int = 0
    percent: float

    def priority_score(self) -> tuple[int, float, int]:
        return self.chapter, self.module, self.submodule

    def __str__(self) -> str:
        r = ""
        if self.chapter <= 3:
            pass
        elif self.chapter == 3:
            r += "[III."
        elif self.chapter == 4:
            r += "[IV."
        elif self.chapter == 5:
            r += "[V."
        elif self.chapter == 6:
            r += "[VI."
        else:
            raise ValueError()

        r += self.title
        if self.chapter <= 3:
            return r
        if self.module <= 6 and int(self.module) == self.module:
            r += f" {int(self.module)}] "
        else:
            r += f" Rép.] "
        r += self.composer.value
        return r


class Routine(BaseModel):
    pieces: list[Piece] = []
    total_budgets: int = 8
    budget_sums: int = 0
    routine_list: list[list[Piece]] = []

    def model_post_init(self, __context: Any) -> None:
        self.routine_list = [[] for _ in range(self.total_budgets)]

    def add_pieces(self, pieces: list[Piece]) -> None:
        for piece in pieces:
            self.add_piece(piece=piece)

    def add_piece(self, piece: Piece):
        self.pieces.append(piece)
        self.budget_sums += round(piece.percent * self.total_budgets / 100)

    def generate_routine(self) -> pd.DataFrame:
        max_len = np.ceil(self.budget_sums / self.total_budgets)

        for piece in tqdm.tqdm(sorted(self.pieces, key=lambda p: - p.percent)):
            inds = spaced_ones_indices(round(piece.percent * self.total_budgets / 100), n=self.total_budgets)
            for ind in inds:
                while len(self.routine_list[ind]) >= max_len:
                    ind = (ind + 1) % self.total_budgets
                self.routine_list[ind].append(piece)
        routine_dict = {
            f"{i + 1}": list(map(str, sorted(routine, key=lambda piece: piece.priority_score()))) for i, routine in
            enumerate(self.routine_list)
        }
        return pd.DataFrame.from_dict(routine_dict)


if __name__ == "__main__":
    routine_ = Routine()

    starting_pieces = [
        Piece(composer=Composer.NONE, title="Doigts plaqués", chapter=0, module=0, percent=100),
        Piece(composer=Composer.NONE, title="3, 4, 5, 4-4, 3...", chapter=0, module=1, percent=50),
        Piece(composer=Composer.NONE, title="mi,ré,do x 3...", chapter=0, module=2, percent=50),
        Piece(composer=Composer.NONE, title="gamme chrom.", chapter=0, module=3, percent=50),
        Piece(composer=Composer.NONE, title="Exo accords", chapter=0, module=4, percent=50),
        Piece(composer=Composer.NONE, title="3ces, 6tes, 8ves", chapter=0, module=5, percent=50),
        Piece(composer=Composer.NONE, title="Exo arpeges", chapter=0, module=6, percent=50),
    ]
    pieces_ = [
        Piece(composer=Composer.SIBMOL, title="4 mains nb. 1", chapter=1, module=1, percent=25),
        Piece(composer=Composer.SIBMOL, title="4 mains nb. 2", chapter=1, module=2, percent=25),
        Piece(composer=Composer.SIBMOL, title="4 mains nb. 3", chapter=1, module=3, percent=25),
        Piece(composer=Composer.CZERNY, title="Etude", chapter=3, module=2, submodule=3, percent=100 / 8),
        Piece(composer=Composer.GURLITT, title="Valse, op. 101", chapter=3, module=3, submodule=3, percent=0),
        Piece(composer=Composer.CHOPIN, title="Grande valse brillante, Op. 18", chapter=3, module=3, submodule=4,
              percent=100 / 8),
        Piece(composer=Composer.PETZOLD, title="Menuet, Anh. 114", chapter=3, module=4, submodule=3, percent=100 / 8),
        Piece(composer=Composer.NYMAN, title="La lecon de piano", chapter=3, module=10, submodule=0, percent=100 / 8),
        Piece(composer=Composer.SHUBERT, title="Ländler", chapter=3, module=5, submodule=2, percent=0),
        Piece(composer=Composer.SIBMOL, title="Valse perdue", chapter=3, module=5, submodule=3, percent=0),
        Piece(composer=Composer.BARTOK, title="In Yugolav style", chapter=3, module=6, submodule=1, percent=0),
        Piece(composer=Composer.BARTOK, title="Song of the rogue", chapter=3, module=6, submodule=3, percent=0),
        Piece(composer=Composer.SIBMOL, title="Etude", chapter=4, module=1, submodule=1, percent=0),
        Piece(composer=Composer.SIBMOL_LEMOINE, title="Prélude", chapter=4, module=1, submodule=2, percent=0),
        Piece(composer=Composer.CORELLI, title="Sarabande", chapter=4, module=1, submodule=3, percent=100 / 4),
        Piece(composer=Composer.SIBMOL, title="Tricotage", chapter=4, module=2, submodule=2, percent=0),
        Piece(composer=Composer.DIABELLI, title="Les premières leçons", chapter=4, module=2, submodule=3, percent=0),
        Piece(composer=Composer.SIBMOL, title="La séparation", chapter=4, module=2, submodule=4, percent=100 / 4),
        Piece(composer=Composer.SIBMOL, title="La Harpe", chapter=4, module=3, submodule=2, percent=0),
        Piece(composer=Composer.WITTHAUER, title="Allegretto", chapter=4, module=3, submodule=3, percent=0),
        Piece(composer=Composer.SIBMOL, title="Boogie", chapter=4, module=3, submodule=4, percent=0),
        Piece(composer=Composer.BACH, title="Jésus, que ma joie demeure, Bach", chapter=4, module=3, submodule=5,
              percent=100 / 8),
        Piece(composer=Composer.SIBMOL, title="Main dans la main", chapter=4, module=4, submodule=1, percent=0),
        Piece(composer=Composer.CZERNY, title="Allegro, Op. 599", chapter=4, module=4, submodule=2, percent=100 / 8),
        Piece(composer=Composer.SIBMOL, title="La complainte", chapter=4, module=5, submodule=3, percent=0),
        Piece(composer=Composer.SIBMOL, title="Octavia", chapter=4, module=5, submodule=4, percent=100 / 4),
        Piece(composer=Composer.CZERNY, title="Opus 453, n°6", chapter=4, module=6, submodule=1, percent=0),
        Piece(composer=Composer.SIBMOL, title="La barcarolle", chapter=4, module=6, submodule=2, percent=0),
        Piece(composer=Composer.CZERNY, title="Opus 599, n°84", chapter=4, module=6, submodule=3, percent=100 / 2),
        Piece(composer=Composer.WOOK, title="The Last waltz", chapter=4, module=10, submodule=0, percent=100 / 4),
        Piece(composer=Composer.PAGANINI, title="Caprice n°24", chapter=4, module=10, submodule=1, percent=100 / 8),
        Piece(composer=Composer.DOUGAN, title="Clubbed to death", chapter=4, module=10, submodule=2, percent=100 / 4),
        Piece(composer=Composer.ELFMAN, title="Bittlejuice", chapter=4, module=10, submodule=3, percent=100 / 4),
        Piece(composer=Composer.SIBMOL, title="Regard 1 - Promenade - Do maj", chapter=4, module=10, submodule=4,
              percent=100 / 4),
        Piece(composer=Composer.SIBMOL, title="Regard 4 - Marche funebre - Do# min.", chapter=4, module=10,
              submodule=5, percent=100 / 8),
        Piece(composer=Composer.SIBMOL, title="Regard 3 - Invitation a la valse - Do# maj.", chapter=4, module=10,
              submodule=6, percent=100 / 4),
        Piece(composer=Composer.HUMMEL, title="Ecossaise", chapter=5, module=1, submodule=1, percent=100 / 4),
        Piece(composer=Composer.KOZELUCH, title="Romance", chapter=5, module=1, submodule=2, percent=100 / 8),
        Piece(composer=Composer.SCHUMANN, title="Mélodie", chapter=5, module=1, submodule=3, percent=100 / 8),
        Piece(composer=Composer.CLEMENTI, title="Sonatine n°1 Do majeur, Op. 36 n°1", chapter=5, module=1, submodule=4,
              percent=100 / 8 * 3),
        Piece(composer=Composer.BEETHOVEN, title="Sonatine en Sol maj.", chapter=5, module=1, submodule=5,
              percent=100 / 8 * 3),
        Piece(composer=Composer.SCHUMANN, title="Le petit cavalier", chapter=5, module=1, submodule=6, percent=100 / 2),
        Piece(composer=Composer.MOZART, title="Valse favorite", chapter=5, module=1, submodule=7, percent=100 / 8 * 3),
        Piece(composer=Composer.SIBMOL, title="Regard 8 - Resignation - Mib min.", chapter=5, module=1.5, submodule=1,
              percent=100 / 4),
        Piece(composer=Composer.SIBMOL, title="Une journée de pluie", chapter=5, module=1.5, submodule=2,
              percent=100 / 2),
        Piece(composer=Composer.BURGMULLER, title="Arabesque", chapter=5, module=2, submodule=1, percent=100 / 8 * 3),
        Piece(composer=Composer.ZIPOLO, title="Versetto", chapter=5, module=2, submodule=2, percent=100 / 2),
        Piece(composer=Composer.BACH, title="Prélude BWV", chapter=5, module=2, submodule=3, percent=100 / 8 * 6),
        Piece(composer=Composer.CHIZAT, title="Nuits perdues, n°2, Reproches", chapter=5, module=2, submodule=4,
              percent=100 / 8 * 3),
        Piece(composer=Composer.BIZET, title="Les marches des rois", chapter=5, module=3, submodule=1,
              percent=100 / 8 * 3),
        Piece(composer=Composer.CLEMENTI, title="Sonatine n°2, Mvt. 2 en Do maj.", chapter=5, module=3, submodule=2,
              percent=100 / 8 * 0),
        Piece(composer=Composer.TCHAIKOVSKI, title="L'enterrement de la poupée", chapter=5, module=3, submodule=3,
              percent=100 / 8 * 4),
        Piece(composer=Composer.SHUBERT, title="Valse en Si mineur", chapter=5, module=3, submodule=4,
              percent=100 / 8 * 5),
        Piece(composer=Composer.TCHAIKOVSKI, title="Reverie", chapter=5, module=3, submodule=5, percent=100 / 8 * 6),
        Piece(composer=Composer.VERDI, title="Traviata - Ah, Fors'è Lui", chapter=5, module=4, submodule=1,
              percent=100 / 8 * 4),
        Piece(composer=Composer.SHUBERT, title="Rosamunde", chapter=5, module=4, submodule=2, percent=100 / 8 * 7),
        Piece(composer=Composer.SHUBERT, title="Sérénade D. 957 - N°4", chapter=5, module=4, submodule=3,
              percent=100 / 8 * 7),
        Piece(composer=Composer.CHOPIN, title="Mazurka Op. 7 N°5", chapter=5, module=4, submodule=4,
              percent=100 / 8 * 8),
        Piece(composer=Composer.HOWARD_EMERSON, title="Ragtime song fest", chapter=5, module=5, submodule=1,
              percent=100 / 8 * 3),
        Piece(composer=Composer.JOPLIN, title="Maple leaf rag", chapter=5, module=5, submodule=2, percent=100 / 8 * 8),
        Piece(composer=Composer.JOPLIN, title="The Entertainer", chapter=5, module=5, submodule=3, percent=100 / 8 * 8),
        Piece(composer=Composer.GERSHWIN, title="Rhapsody in blue", chapter=5, module=5, submodule=4,
              percent=100 / 8 * 8),
    ]

    routine_.add_pieces(pieces=pieces_)
    routine_df = routine_.generate_routine()
    routine_df.to_csv("./routine.csv")
    routine_df.to_excel("./routine.xlsx", index=False)
    print(routine_df)
