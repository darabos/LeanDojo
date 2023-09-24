"""Constants controlling LeanDojo's behaviors. 
Many of them are configurable via :ref:`environment-variables`.
"""
import os
import re
import sys
import subprocess
import multiprocessing
from github import Auth
from pathlib import Path
from typing import Tuple
from github import Github
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

__version__ = "1.2.4"

logger.remove()
if "VERBOSE" in os.environ or "DEBUG" in os.environ:
    logger.add(sys.stderr, level="DEBUG")
else:
    logger.add(sys.stderr, level="INFO")

CACHE_DIR = (
    Path(os.environ["CACHE_DIR"])
    if "CACHE_DIR" in os.environ
    else Path.home() / ".cache/lean_dojo"
)
"""Cache directory for storing traced repos (see :ref:`caching`).
"""

REMOTE_CACHE_URL = "https://lean-dojo.s3.amazonaws.com"
"""URL of the remote cache (see :ref:`caching`)."""

DISABLE_REMOTE_CACHE = "DISABLE_REMOTE_CACHE" in os.environ
"""Whether to disable remote caching (see :ref:`caching`) and build all repos locally.
"""

TMP_DIR = Path(os.environ["TMP_DIR"]) if "TMP_DIR" in os.environ else None
"""Temporary directory used by LeanDojo for storing intermediate files
"""

MAX_NUM_PROCS = 32

NUM_PROCS = int(os.getenv("NUM_PROCS", min(multiprocessing.cpu_count(), MAX_NUM_PROCS)))
"""Number of threads to use
"""

NUM_WORKERS = NUM_PROCS - 1

LEAN3_URL = "https://github.com/leanprover-community/lean"
"""The URL of the Lean 3 repo."""

LEAN3_DEPS_DIR = Path("_target/deps")
"""The directory where Lean 3 dependencies are stored."""

LEAN4_URL = "https://github.com/leanprover/lean4"
"""The URL of the Lean 4 repo."""

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN", None)
"""GiHub personal access token is optional. 
If provided, it can increase the rate limit for GitHub API calls.
"""

if GITHUB_ACCESS_TOKEN:
    logger.debug("Using GitHub personal access token for authentication")
    GITHUB = Github(auth=Auth.Token(GITHUB_ACCESS_TOKEN))
    GITHUB.get_user().login
else:
    logger.debug(
        "Using GitHub without authentication. Don't be surprised if you hit the API rate limit."
    )
    GITHUB = Github()

LEAN4_REPO = GITHUB.get_repo("leanprover/lean4")
"""The GitHub Repo for Lean 4 itself."""

LEAN4_NIGHTLY_REPO = GITHUB.get_repo("leanprover/lean4-nightly")
"""The GitHub Repo for Lean 4 nightly releases."""

LEAN4_DEPS_DIR = Path("lake-packages")
"""The directory where Lean 4 dependencies are stored."""

LOAD_USED_DEPS_ONLY = "LOAD_USED_DEPS_ONLY" in os.environ
"""Only load depdendency files that are actually used by the target repo."""

TACTIC_TIMEOUT = int(os.getenv("TACTIC_TIMEOUT", 5000))
"""Maximum time (in milliseconds) before interrupting a tactic when interacting with Lean (only for Lean 3).
"""

TACTIC_CPU_LIMIT = int(os.getenv("TACTIC_CPU_LIMIT", 1))
"""Number of CPUs for executing tactics when interacting with Lean.
"""

TACTIC_MEMORY_LIMIT = os.getenv("TACTIC_MEMORY_LIMIT", "16g")
"""Maximum memory when interacting with Lean.
"""

CONTAINER = os.getenv("CONTAINER", "docker")
"""Container to use for running LeanDojo. Default to ``docker`` but also support ``native``.
"""

DOCKER_AVAILABLE = os.system("docker version 1>/dev/null 2>/dev/null") == 0

DOCKER_TAG = "yangky11/lean-dojo"

if CONTAINER == "docker":
    assert (
        DOCKER_AVAILABLE
    ), "Failed to access Docker. Please make sure Docker is running and you have access. Alternatively, you can try to run without Docker by setting the `CONTAINER` environment variable to `native` (see https://leandojo.readthedocs.io/en/latest/user-guide.html#advanced-running-without-docker)."
    os.system(f"docker pull {DOCKER_TAG} 1>/dev/null 2>/dev/null")

MIN_LEAN3_VERSION = "v3.42.1"
"""The minimum version of Lean 3 that LeanDojo supports.
"""


def check_git_version(min_version: Tuple[int, int, int]) -> Tuple[int, int, int]:
    """Check the version of Git installed on the system."""
    res = subprocess.run("git --version", shell=True, capture_output=True, check=True)
    output = res.stdout.decode()
    error = res.stderr.decode()
    assert error == "", error
    m = re.match(r"git version (?P<version>[0-9.]+)", output)
    version = tuple(int(_) for _ in m["version"].split("."))

    version_str = ".".join(str(_) for _ in version)
    min_version_str = ".".join(str(_) for _ in min_version)
    assert (
        version >= min_version
    ), f"Git version {version_str} is too old. Please upgrade to at least {min_version_str}."


check_git_version((2, 25, 0))
