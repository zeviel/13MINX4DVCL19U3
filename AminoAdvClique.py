import asyncio
import pyfiglet
from sty import fg; print(fg(221))
from configs import main_functions
print("""Script by DeLuvSushi
Github : https://github.com/deluvsushi""")
print(pyfiglet.figlet_format("aminoadvclique", font="slant"))

asyncio.get_event_loop().run_until_complete(main_functions.main())
