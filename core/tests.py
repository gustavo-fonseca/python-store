from django.test import TestCase

from core.validators import (CPF_validate, brasil_postal_code_validate,
                             cellphone_validate)


class CoreTest(TestCase):
    def test_validators_cpf(self):
        self.assertEqual(CPF_validate("000.000.000-00"), False)
        self.assertEqual(CPF_validate("000.000.000-01"), False)
        self.assertEqual(CPF_validate("999.999.999-99"), False)
        self.assertEqual(CPF_validate("000.000.000"), False)
        self.assertEqual(CPF_validate("000.000.001"), False)
        self.assertEqual(CPF_validate("323.795.000-96"), True)
        self.assertEqual(CPF_validate("442.626.280-19"), True)

    def test_validators_brasi_postal_code(self):
        self.assertEqual(brasil_postal_code_validate("90000-00"), False)
        self.assertEqual(brasil_postal_code_validate("90000-0"), False)
        self.assertEqual(brasil_postal_code_validate("9000-0"), False)
        self.assertEqual(brasil_postal_code_validate("90000-000"), True)
        self.assertEqual(brasil_postal_code_validate("90000-001"), True)
        self.assertEqual(brasil_postal_code_validate("90002-001"), True)

    def test_validators_cellphone(self):
        self.assertEqual(cellphone_validate("(11) 8888-000"), False)
        self.assertEqual(cellphone_validate("(11) 8888-00000"), False)
        self.assertEqual(cellphone_validate("(11) 888-00000"), False)
        self.assertEqual(cellphone_validate("(11) 99888-00000"), False)
        self.assertEqual(cellphone_validate("(1) 99888-0000"), False)
        self.assertEqual(cellphone_validate("(1) 99888-"), False)
        self.assertEqual(cellphone_validate("(11) 99888-a999"), False)
        self.assertEqual(cellphone_validate("(11) 8888-0000"), True)
        self.assertEqual(cellphone_validate("(11) 99888-0000"), True)
        self.assertEqual(cellphone_validate("(11) 99888-0000"), True)
