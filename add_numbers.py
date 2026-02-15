#!/usr/bin/env python3
import sys

def add(a, b):
    """Return the sum of two numbers."""
    return a + b

def main():
    if len(sys.argv) >= 3:
        try:
            a = float(sys.argv[1])
            b = float(sys.argv[2])
        except ValueError:
            print("Please provide two numeric values.", file=sys.stderr)
            sys.exit(2)
    else:
        try:
            a = float(input("First number: "))
            b = float(input("Second number: "))
        except ValueError:
            print("Please provide valid numbers.", file=sys.stderr)
            sys.exit(2)

    result = add(a, b)
    # Print as int when the result is whole, else as float
    if isinstance(result, float) and result.is_integer():
        print(int(result))
    else:
        print(result)

if __name__ == "__main__":
    main()
