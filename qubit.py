import random

# qubit.py
# Instance of a qubit used for modeling a QKE algorithim.
class Qubit:

    # Constructor.
    def __init__(self, value: int, polarization: int):
        self.set(value, polarization)


    # Sets the states of a qubit given parameters.
    #
    # Param     [value]         The value of this qbuit, 0 or 1.
    # Param     [polarization]  The polarization, 0 for circular or 1 for linear.
    def set(self, value: int, polarization: int):
        if value not in(0, 1):
            raise ValueError("Value of Qubit must be 0 or 1")
        if polarization not in (0, 1):
            raise ValueError("Polarization of Qubit must be 0 or 1")
        else:
            self.value = value
            self.polarization = polarization


    # Measures the qubit's polarization.
    # If not equal, then flips polarization and invokes potential value change.
    #
    # Param     [polarization]  The polarization, 0 for circular or 1 for linear.
    # Returns   The qubit's value, as-is if parameter matches polarization.
    def measure(self, polarization: int) -> int:
        if polarization not in (0, 1):
            raise ValueError("Polarization of Qubit must be 0 or 1")
        if polarization == self.polarization:
            return self.value
        else:
            self.polarization = polarization
            self.value = random.randint(0, 1)

            return self.value

