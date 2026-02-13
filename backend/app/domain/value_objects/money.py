from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class COP:
    """Colombian Peso amount value object."""
    amount: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))

    def __str__(self) -> str:
        return f"${self.amount:,.0f} COP"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, COP):
            return self.amount == other.amount
        return NotImplemented

    def __lt__(self, other: "COP") -> bool:
        return self.amount < other.amount

    def __le__(self, other: "COP") -> bool:
        return self.amount <= other.amount

    def __gt__(self, other: "COP") -> bool:
        return self.amount > other.amount

    def __ge__(self, other: "COP") -> bool:
        return self.amount >= other.amount

    def rounded(self) -> "COP":
        return COP(self.amount.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
