"""Airport model: a vertex in the flight network."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Airport:
    """An airport node identified by a unique airport code.

    The ``code`` is normalised to upper case and must be non-empty. Equality
    and hashing are based solely on ``code`` so that an ``Airport`` can be used
    as a dictionary key and compared by identity of code.
    """

    code: str
    name: str = field(default="", compare=False)

    def __post_init__(self) -> None:
        normalised = str(self.code).strip().upper()
        if not normalised:
            raise ValueError("Airport code must be a non-empty string.")
        # ``frozen=True`` blocks normal assignment; use object.__setattr__.
        object.__setattr__(self, "code", normalised)

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        return f"{self.code}" + (f" ({self.name})" if self.name else "")
