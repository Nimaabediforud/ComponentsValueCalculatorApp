class Validate:
    """
    Validation Functions:
        .
        .
        .
    """

    def __init__(self, NO_COLOR: str, spec_col: list, tolerance: dict, temp_coeff: dict):
        self.NO_COLOR = NO_COLOR
        self.spec_col = spec_col
        self.tolerance = tolerance
        self.temp_coeff = temp_coeff
        

    def Validate_No_Color(self, digit: int, lst: list):
        if self.NO_COLOR in lst[0:digit]:
            return True


    def Validate_Spec_Colors(self, digit: int, lst: list):
        l = [True for c in self.spec_col if c in lst[0:digit]]
        if any(l): 
            return True
        

    def Validate_Tolerance(self, digit: int, lst: list):
        if lst[digit] not in self.tolerance:
            return True
        
        
    def Validate_Temp_Coeff(self, digit: int | None, lst: list):
        if digit == None:
            return False
        elif lst[digit] not in self.temp_coeff:
            return True
        



