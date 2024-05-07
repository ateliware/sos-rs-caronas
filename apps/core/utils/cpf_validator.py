class CpfValidator:
    def validate_cpf(self, cpf: str) -> bool:
        has_equal_digits = self.check_equal_digits(cpf)
        if has_equal_digits:
            return False

        length_is_valid = len(cpf) == 11

        if not length_is_valid:
            return False

        first_digit = self.calculate_cpf_verifier_digit(cpf, 1)
        second_digit = self.calculate_cpf_verifier_digit(cpf, 2)
        return first_digit == cpf[-2] and second_digit == cpf[-1]

    @staticmethod
    def check_equal_digits(text: str) -> bool:
        qtt_digits = len(text)
        equal_digits = text[0].ljust(qtt_digits, text[0])
        return text == equal_digits

    @staticmethod
    def calculate_cpf_verifier_digit(cpf: str, digit: int) -> str:
        """
        This method calculates the verifier digit of a CPF number.
        Must receive a CPF number and the digit to be calculated (1 or 2).
        """
        list_sum = 0
        max_sequence_value = digit + 9
        sequence = list(range(max_sequence_value, 1, -1))

        for index, number in enumerate(sequence):
            list_sum += number * int(cpf[index])

        raw_digit = (list_sum * 10) % 11
        return str(raw_digit) if raw_digit < 10 else "0"
