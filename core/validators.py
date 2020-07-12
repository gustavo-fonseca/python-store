import re
from validate_docbr import CPF


def cellphone_validate(value: str) -> bool:
    """
    Validate cellphone with format: (00) 91111-1111
    """
    return re.match(r"^\([1-9]{2}\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$", value)


def CPF_validate(value: str) -> bool:
    """
    Validate cellphone with format: 000.000.000-00
    It also check the CPF DV
    """
    return CPF().validate(value)
