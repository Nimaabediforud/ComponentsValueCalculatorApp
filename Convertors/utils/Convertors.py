from .utilities import Validate

class Resistor:
    """
    A class to encode color band and label of resistors to calculate resistance value and interpret them
    """

    # All colors used for value and decimal multiplier
    colors = {
        "black": 0,
        "brown": 1,
        "red": 2,
        "orange": 3,
        "yellow": 4,
        "green": 5,
        "blue": 6,
        "purple": 7,
        "gray": 8,
        "white": 9,
        "gold": -1,
        "silver": -2
    }

    # All colors used for tolerance
    tolerance = {
        "brown": '1',
        "red": '2',
        "green": '0.5',
        "blue": '0.25',
        "purple": '0.1',
        "gold": '5',
        "silver": '10',
        "": '20' # No color
    }

    # All colors used for temperature coefficient
    temp_coeff = {
        "brown": 100,
        "red": 50,
        "orange": 15,
        "yellow": 25,
    }

    # All letters used in smd resistor labels
    smd_letters = {
        "r": ".",
        "d": 0.5,
        "f": 1.0,
        "g": 2.0,
        "h": 5.0
    }

    # Global list and variable
    spec_col = ["gold", "silver"]
    NO_COLOR = ""


    def __init__(self):
        pass


    def Unit_Convertor(self, num: int):
        """
        
        """

        num_of_digits = len(str(num))

        if 0 <= num_of_digits <= 3:
            return f"{num} "
        elif 3 < num_of_digits <= 6:
            num = num/(10**3)
            return f"{num} k"
        elif 6 < num_of_digits <= 9:
            num = num/(10**6)
            return f"{num} M"
        elif 9 < num_of_digits <= 12:
            num = num/(10**9)
            return f"{num} G"
        elif 12 < num_of_digits <= 15:
            num = num/(10**12)
            return f"{num} T"


    def Jumper(self, lbl: str | list):
            """
            
            """
            if type(lbl) == list:
                lbl = lbl[0]

            lbl = lbl.lower()

            if lbl == "black":
                return "A JUMPER so 0 Ω", "Single band black color"
            elif lbl == "o"  or lbl == "0":
                return "A JUMPER so 0 Ω", "Single character label 'o'"
            elif lbl == "000":
                return "A JUMPER so 0 Ω", "Your label '000'"
            else:
                return False

    def Validations(self, num1: str, num2: str, num3: str, band: list, No_Col_Digit: int,
                     Spec_Col_Digit: int, Tolerance_Digit: int, Temp_Coe_Digit: int=None):
        """
        
        """
        # Check user's input to validate it by validation functions
        v = Validate(Resistor.NO_COLOR, Resistor.spec_col, Resistor.tolerance, Resistor.temp_coeff)
        check_1 = v.Validate_No_Color(No_Col_Digit, band)
        check_2 = v.Validate_Spec_Colors(Spec_Col_Digit, band)
        check_3 = v.Validate_Tolerance(Tolerance_Digit, band)
        check_4 = v.Validate_Temp_Coeff(Temp_Coe_Digit, band)

        # Messages in case of invalidation
        if check_1:
            return f"The first {num1} bands must not be COLORLESS!", band
        if check_2:
            return f"The first {num2} bands can not be GOLD or SILVER!", band
        if check_3:
            return f"The correspondent band to tolerance ({num3} band) is incorrect!", band
        if check_4:
            return "The correspondent band to temperature coefficient is incorrect!", band
        
        return False
        


    def FourColor(self, lst: list):
        """
        
        """

        #--------------------------------------------------------

        # Initial check for a 4-band resistor code - (Becomes a 3-band if its tolerance is 20%)
        if len(lst) == 3:
            band = lst[0:3] + [""] # Three digits + One no color or tolerance
        elif len(lst) == 4: 
            band = lst[0:4] # Take exactly four bands (digits)
        else:
            return False

        #--------------------------------------------------------

        # Check user's input to validate it by validation functions
        val = self.Validations("three", "two", "last", band, 3, 2, -1)

        if val:
            return val

        #--------------------------------------------------------

        # Build up each digit from the 4-band code
        first_two_digits = int("".join([str(Resistor.colors.get(c)) for c in band[0:2]]))
        third_digit = 10**(Resistor.colors.get(band[2]))
        fourth_digit = Resistor.tolerance.get(band[-1])

        #--------------------------------------------------------

        # Calculate and Interpret the final result
        result = f"{self.Unit_Convertor(first_two_digits*third_digit)}Ω ± {fourth_digit}%"

        #--------------------------------------------------------
        
        return result, band


    def FiveColor(self, lst: list):
        """
        
        """

        #--------------------------------------------------------

        # Initial check for a 5-band resistor code
        if len(lst) == 5: 
            band = lst[0:5] # Take exactly five bands (digits)
        else:
            return False
        
        #--------------------------------------------------------

        # Check user's input to validate it by validation functions
        val = self.Validations("four", "three", "last", band, 4, 3, -1)

        if val:
            return val

        #--------------------------------------------------------

        # Build up each digit from the 5-band code
        first_three_digits = int("".join([str(Resistor.colors.get(c)) for c in band[0:3]]))
        fourth_digit = 10**(Resistor.colors.get(band[3]))
        fifth_digit = Resistor.tolerance.get(band[-1])

        #--------------------------------------------------------

        # Calculate and Interpret the final result
        result = f"{self.Unit_Convertor(first_three_digits*fourth_digit)}Ω ± {fifth_digit}%"

        #--------------------------------------------------------
        
        return result, band


    def SixColor(self, lst: list):
        """
        
        """

        #--------------------------------------------------------

        # Initial check for a 6-band resistor code
        if len(lst) == 6: 
            band = lst[0:6] # Take exactly six bands (digits)
        else:
            return False
    
        #--------------------------------------------------------

        # Check user's input to validate it by validation functions
        val = self.Validations("four", "three", "fifth", band, 4, 3, 4, -1)

        if val:
            return val

        #--------------------------------------------------------

        # Build up each digit from the 6-band code
        first_three_digits = int("".join([str(Resistor.colors.get(c)) for c in band[0:3]]))
        fourth_digit = 10**(Resistor.colors.get(band[3]))
        fifth_digit = Resistor.tolerance.get(band[4])
        sixth_digit = Resistor.temp_coeff.get(band[-1])

        #--------------------------------------------------------

        # Calculate and Interpret the final result
        result = f"{self.Unit_Convertor(first_three_digits*fourth_digit)}Ω ± {fifth_digit}% | TC: {sixth_digit} ppm"

        #--------------------------------------------------------
        
        return result, band


    def Three_Digit(self, label: str):
        """
        
        """

        #--------------------------------------------------------

        if len(label) != 3:
            return False
        
        #--------------------------------------------------------
        
        r_count = label.count("r")

        if  r_count > 1:
            return "Only one letter of R is allowed!", "Please try again!"
        elif r_count == 1:
            if label.index("r") == 0:
                result = f"{'0' + label.replace('r', Resistor.smd_letters.get('r'))} Ω"
            elif label.index("r") == 1:
                result = f"{label.replace('r', Resistor.smd_letters.get('r'))} Ω"
            else:
                result = f"{label[0:2]} Ω"
        else:
            # Build up each digit from the 4-band code
            first_two_digits = int(label[0:2])
            third_digit = 10**(int(label[-1]))

            # Calculate and Interpret the final result
            result = f"{self.Unit_Convertor(first_two_digits*third_digit)}Ω"
        
        return result, label.upper()
    

    def Four_Digit(self, label: str):
        """
        
        """

        #--------------------------------------------------------

        if len(label) != 4:
            return False
        
        #--------------------------------------------------------
        
        if label[3] in list(Resistor.smd_letters.keys())[1:]:
            r_count = label.count("r")

            if  r_count > 1:
                return "Only one letter of R is allowed!", "Please try again!"
            elif r_count == 1:
                if label.index("r") == 0:
                    result = f"{'0' + label[0:3].replace('r', Resistor.smd_letters.get('r'))} Ω ± {Resistor.smd_letters.get(label[-1])}%"
                elif label.index("r") == 1 or label.index("r") == 2:
                    result = f"{label[0:3].replace('r', Resistor.smd_letters.get('r'))} Ω ± {Resistor.smd_letters.get(label[-1])}%"
                else:
                    result = f"{label[0:3]} Ω ± {Resistor.smd_letters.get(label[-1])}%"
            else:
                # Build up each digit from the label
                first_two_digits = int(label[0:2])
                third_digit = 10**(int(label[2]))

                # Calculate and Interpret the final result
                result = f"{self.Unit_Convertor(first_two_digits*third_digit)}Ω ± {Resistor.smd_letters.get(label[-1])}%"
            
        elif label[3] == list(Resistor.smd_letters.keys())[0] or label[3].isdigit():
            r_count = label.count("r")

            if  r_count > 1:
                return "Only one letter of R is allowed!", "Please try again!"
            elif r_count == 1:
                if label.index("r") == 0:
                    result = f"{'0' + label.replace('r', Resistor.smd_letters.get('r'))} Ω"
                elif label.index("r") == 1 or label.index("r") == 2:
                    result = f"{label.replace('r', Resistor.smd_letters.get('r'))} Ω"
                else:
                    result = f"{label[0:3]} Ω"
            else:
                # Build up each digit from the label
                first_three_digits = int(label[0:3])
                fourth_digit = 10**(int(label[-1]))

                # Calculate and Interpret the final result
                result = f"{self.Unit_Convertor(first_three_digits*fourth_digit)}Ω"
            
            
        return result, label.upper()




    def Dip_Res(self, col: str=None, stat: bool=True):
        """
        
        """
        #--------------------------------------------------------
        if stat and col == None:
            col = input(f"Enter the band colors (Separated with '-'): ").strip()

        colors_lst = [c.lower().strip() for c in col.split("-")]
        
        for c in colors_lst:
            if c not in Resistor.colors.keys():
                return "Oops, Seems like we have a problem!", f"Make sure you have not misspelled the name of the color {c}!"

        #--------------------------------------------------------

        if self.Jumper(colors_lst) != False:
            return f"Colors: {self.Jumper(colors_lst)[1]}", f"Result: {self.Jumper(colors_lst)[0]}"  
        elif self.FourColor(colors_lst) != False:
            return f"Colors: {self.FourColor(colors_lst)[1]}", f"Result: {self.FourColor(colors_lst)[0]}"  
        elif self.FiveColor(colors_lst) != False:
            return f"Colors: {self.FiveColor(colors_lst)[1]}", f"Result: {self.FiveColor(colors_lst)[0]}"    
        elif self.SixColor(colors_lst) != False:
            return f"Colors: {self.SixColor(colors_lst)[1]}", f"Result: {self.SixColor(colors_lst)[0]}"
        
        return "Unrecognized format", "Please use 3, 4, 5, or 6 color bands separated by hyphens."

    def SMD_Res(self, label: str=None, stat: bool=True):
        """
        
        """

        #--------------------------------------------------------
        if stat and label == None:
            label = input(f"Enter the label: ").strip()

        label = label.lower()

        try:
            check_ = []
            if len(label) == 1 or 3 <= len(label) <= 4:
                for c in label.lower():
                    if c.isdigit() or c in ["r", "o"]:
                        check_.append(True)
                    elif c in Resistor.smd_letters.keys() and label.index(c) == 3:
                        check_.append(True)
                    else:
                        check_.append(False)
            else:
                return "There should be 3-4 characters in the label!", "Try again!"
        except TypeError:
            return "Label's type must be string!", "Not integer or any other!"
        
        #--------------------------------------------------------
        
        if all(check_):
            if self.Jumper(label) != False:
                return f"Label: {self.Jumper(label)[1]}", f"Result: {self.Jumper(label)[0]}"  
            elif self.Three_Digit(label) != False:
                return f"Label: {self.Three_Digit(label)[1]}", f"Result: {self.Three_Digit(label)[0]}"  
            elif self.Four_Digit(label) != False:
                return f"Label: {self.Four_Digit(label)[1]}", f"Result: {self.Four_Digit(label)[0]}"    
        else:
            return "Oops, Seems like we have a problem!", "Make sure you have entered the label correctly!!"
        
        return "Invalid SMD label", "Label must be 3 or 4 characters (digits and/or R, o, d, f, g, h)."
        


    def Run(self, type: str=None, value: str=None, stat: bool=True):
        """
        
        """

        if stat and type == None and value == None:
            type = input("Select the type of your resistor:\n1. Dip 2. SMD\n>> ").strip().lower()

            if type == "dip" or type == "1":
                color, result = self.Dip_Res()
                return color, result
            elif type == "smd" or type == "2":
                label, result = self.SMD_Res()
                return label, result
            else:
                return "Your choice is not among the options!", "Please try again!"
            
        else:
            type = type.lower()

            if type == "dip" or type == "1":
                color, result = self.Dip_Res(col=value, stat=False)
                return color, result
            elif type == "smd" or type == "2":
                label, result = self.SMD_Res(label=value, stat=False)
                return label, result
            else:
                return "Your choice is not among the options!", "Please try again!"
            


