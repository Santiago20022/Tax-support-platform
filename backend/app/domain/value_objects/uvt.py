from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class UVT:
    """Unidad de Valor Tributario value object."""
    amount: Decimal

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))

    def to_cop(self, uvt_value: Decimal) -> Decimal:
        """Convert UVT amount to COP given the UVT value for a fiscal year."""
        return (self.amount * uvt_value).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    def __str__(self) -> str:
        return f"{self.amount:,.0f} UVT"
