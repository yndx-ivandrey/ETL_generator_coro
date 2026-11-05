def sum1(initial, increase, count):
    result = initial
    for _ in range(count):
        print(result := result + increase)


def sum2(initial, increase, count):
    result = initial
    for _ in range(count):
        result += increase
        yield result


if __name__ == "__main__":
    print("Call function:")
    sum1(0, 2, 5)

    print("Receive from generator:")
    for i in sum2(0, 2, 5):
        print(i)

    print("From generator expression:")
    expr = (2 + i * 2 for i in range(5))
    for i in expr:
        print(i)

    print("Конец программы")
