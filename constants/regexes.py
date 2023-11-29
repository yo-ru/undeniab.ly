from __future__ import annotations

import re

email = re.compile(r"^[^@\s]{1,200}@[^@\s\.]{1,30}\.[^@\.\s]{1,24}$")
