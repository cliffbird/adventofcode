import argparse
import importlib
import os
import time


class BaseProcessor:
    INPUT_PATH_FORMAT = os.path.join("{}", "input", "day{}{}.txt")

    def __init__(self, year, day):
        self.year = year
        self.day = day
        self.path = self.get_path_from_day(year, day)

    @classmethod
    def get_path_from_day(cls, year, day, path_suffix=""):
        return cls.INPUT_PATH_FORMAT.format(year, day, f"_{path_suffix}" if path_suffix else "")

    def run_all(self):
        self.base_run(path_suffix="example")
        self.base_run()

    def base_run(self, path_suffix=""):
        self.path_suffix = path_suffix
        self.path = self.get_path_from_day(self.year, self.day, path_suffix)
        if os.path.exists(self.path):
            if path_suffix:
                print(f"*** Running {path_suffix} ***")
            else:
                print("*** Running primary ***")
            self.run1()
            self.run2()
            print()
        else:
            print(f"*** File does not exist: {self.path}")

    def run1(self):
        pass

    def run2(self):
        pass


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)

    args = parser.parse_args()

    module_name = f"day{args.day}"
    if not os.path.exists(f"{args.year}/{module_name}.py"):
        raise ModuleNotFoundError(f"No module named '{args.year}.{module_name}'")
    mod = importlib.import_module(f"{args.year}.{module_name}")

    start_time = time.time()
    processor_class = getattr(mod, f"D{args.day}Processor")
    p = processor_class(args.year, args.day)
    p.run_all()
    print(f"Run time: {time.time() - start_time:0.3f}s")

if __name__ == "__main__":
    main()
