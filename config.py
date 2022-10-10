"""

import random, string

rondomSecure = random.SystemRandom()
"".join([random.choice(string.printable) for _ in range(24)])

"""

SECRET_KEY = "lp |i(.'F<sfuEbCVx\n3,RDt"