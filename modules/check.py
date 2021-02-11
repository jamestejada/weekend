from modules import process
from colorama import Style, Fore


class Check_BASE(process.Reveal):
    def check(self):
        print(Fore.CYAN, f'\n-{self}-', Style.RESET_ALL)
        exist_dict = self._which_exist()
        for segment in exist_dict:
            color = Fore.GREEN if exist_dict.get(segment) else Fore.RED
            style = Style.BRIGHT if exist_dict.get(segment) else Style.DIM
            print(color, style, segment.replace('_', ' ').title(), Style.RESET_ALL)
    
    def _which_exist(self):
        return {
            segment_name: (segment_name in self.source_paths.keys())
            for segment_name in self.CUT_NUMBERS.keys()
        }
    
    def __str__(self):
        return self.__class__.__name__.replace('_', ' ')


class Reveal(Check_BASE, process.Reveal): ...
class Latino_USA(Check_BASE, process.Latino_USA): ...
class Says_You(Check_BASE, process.Says_You): ...
class The_Moth(Check_BASE, process.The_Moth): ...
class Snap_Judgment(Check_BASE, process.Snap_Judgment): ...
class This_American_Life(Check_BASE, process.This_American_Life): ...


CHECK_SHOWS = [
    Reveal, 
    Latino_USA,
    Says_You,
    The_Moth,
    Snap_Judgment,
    This_American_Life
]


def check_all():
    for show_class in CHECK_SHOWS:
        show = show_class()
        show.check()
    print()
