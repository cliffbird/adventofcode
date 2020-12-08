import argparse
import importlib
import os
import time


class BaseProcessor:
    INPUT_PATH_FORMAT = os.path.join("input", "day{}{}.txt")

    def __init__(self, day):
        self.day = day
        self.path = self.get_path_from_day(day)

    @classmethod
    def get_path_from_day(cls, day, path_suffix=""):
        return cls.INPUT_PATH_FORMAT.format(day, f"_{path_suffix}" if path_suffix else "")

    def run_all(self):
        self.base_run(path_suffix="example")
        self.base_run()

    def base_run(self, path_suffix=""):
        self.path = self.get_path_from_day(self.day, path_suffix)
        if os.path.exists(self.path):
            if path_suffix:
                print(f"*** Running {path_suffix} ***")
            else:
                print("*** Running primary ***")
            self.run1()
            self.run2()
            print()

    def run1(self):
        pass

    def run2(self):
        pass


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("day", type=int)

    args = parser.parse_args()

    module_name = f"day{args.day}"
    if not os.path.exists(f"{module_name}.py"):
        raise ModuleNotFoundError(f"No module named '{module_name}'")
    mod = importlib.import_module(f"{module_name}")

    start_time = time.time()
    processor_class = getattr(mod, f"D{args.day}Processor")
    p = processor_class(args.day)
    p.run_all()
    print(f"Run time: {time.time() - start_time:0.3f}s")

if __name__ == "__main__":
    main()
