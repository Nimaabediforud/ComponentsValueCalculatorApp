class Validate:
    """
    Validation Functions:
    In order to check that the colors are in their correct bands
    """

    def __init__(self, NO_COLOR: str, spec_col: list, tolerance: dict, temp_coeff: dict):
        self.NO_COLOR = NO_COLOR
        self.spec_col = spec_col
        self.tolerance = tolerance
        self.temp_coeff = temp_coeff
        

    def Validate_No_Color(self, digit: int, lst: list):
        # If there are NO COLOR from band 0 to digit return True
        if self.NO_COLOR in lst[0:digit]:
            return True


    def Validate_Spec_Colors(self, digit: int, lst: list):
        # If there are Specific Colors (Like GOLD & SILVER) from band 0 to digit return True
        l = [True for c in self.spec_col if c in lst[0:digit]]
        if any(l): 
            return True
        

    def Validate_Tolerance(self, digit: int, lst: list):
        # If one specific Color Band is not among Tolerance Colors return True
        if lst[digit] not in self.tolerance:
            return True
        
        
    def Validate_Temp_Coeff(self, digit: int | None, lst: list):
        # If one specific Color Band is NONE return False
        if digit == None:
            return False
        # If one specific Color Band is not among Temp_Coeff Colors return True
        elif lst[digit] not in self.temp_coeff:
            return True
        



