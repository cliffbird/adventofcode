from main import BaseProcessor
import re


class D4Processor(BaseProcessor):
    KEYS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
    VALID_ECLS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

    def run_all(self):
        self.base_run(path_suffix="invalid")
        self.base_run(path_suffix="valid")
        self.base_run(path_suffix="example")
        self.base_run()

    def run1(self):
        pass

    def run2(self):
        path = self.path
        optional = ["cid"]
        num_valid = 0
        with open(path, "r") as f:
            valid_keys = list(self.KEYS)
            for line in f:
                line = line.strip()
                if not line:
                    # blank line
                    if len(valid_keys) == 0:
                        num_valid += 1
                    valid_keys = list(self.KEYS)

                parts = line.split()
                for part in parts:
                    key, value = part.split(":")
                    if key in valid_keys:
                        can_remove = False
                        if key == "byr":
                            try:
                                value = int(value)
                                if value >= 1920 and value <= 2002:
                                    can_remove = True
                            except:
                                pass
                        elif key == "iyr":
                            try:
                                value = int(value)
                                if value >= 2010 and value <= 2020:
                                    can_remove = True
                            except:
                                pass
                        elif key == "eyr":
                            try:
                                value = int(value)
                                if value >= 2020 and value <= 2030:
                                    can_remove = True
                            except:
                                pass
                        elif key == "hgt":
                            if "cm" in value:
                                m = re.match("([0-9]{3})cm\\Z", value)
                                if m:
                                    value = int(m.group(1))
                                    if value >= 150 and value <= 193:
                                        can_remove = True
                            elif "in" in value:
                                m = re.match("([0-9]{2})in\\Z", value)
                                if m:
                                    value = int(m.group(1))
                                    if value >= 59 and value <= 76:
                                        can_remove = True
                        elif key == "hcl":
                            m = re.match("#[0-9a-f]{6}\\Z", value)
                            if m:
                                can_remove = True
                        elif key == "ecl":
                            if value in self.VALID_ECLS:
                                can_remove = True
                        elif key == "pid":
                            m = re.match("\\A[0-9]{9}\\Z", value)
                            if m:
                                can_remove = True

                        if can_remove:
                            valid_keys.remove(key)
                for opt in optional:
                    if opt in valid_keys:
                        valid_keys.remove(opt)
            if len(valid_keys) == 0:
                num_valid += 1

        print(f"num valid: {num_valid}")
        return num_valid
