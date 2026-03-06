from importlib.metadata import version, PackageNotFoundError

from .sign import Signer, HeaderSigner
from .verify import Verifier, HeaderVerifier

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    pass

__all__ = (Signer, HeaderSigner, Verifier, HeaderVerifier)
