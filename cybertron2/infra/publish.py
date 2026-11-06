"""Where runs are published, and the files that never are (taken from Cybertron 1's cybertron/publish.py at the split)."""
from __future__ import annotations

import os
import re

DATASET = "zachmacsmith/cybertron2-runs"     # the Hugging Face dataset id: the only place it is written in Python


def default_repo() -> str:
    """The dataset to publish to: $CYBERTRON2_DATASET when set, else DATASET."""
    return os.environ.get("CYBERTRON2_DATASET") or DATASET


# raw files never published: pickles execute code when loaded; claude_sessions / .claude*: the Claude Code CLI's account file and
# transcripts (email, account ids, injected context); credentials, .env files and private keys: secrets. privacy.py scans the rest.
NEVER = re.compile(r"(^|/)(checkpoints?(/|$)|claude_sessions(/|$)|\.claude[^/]*(/|$)|\.credentials[^/]*\.json$|\.env(\.[^/]*)?$"
                   r"|id_(rsa|dsa|ecdsa|ed25519)[^/]*$|[^/]*\.pem$|[^/]*\.pkl$|[^/]*\.pickle$|abandoned_calls\.jsonl$)")
