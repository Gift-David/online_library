def menu(title: str, items: list):
    print(title.title())
    i = 1
    for item in items:
        print(f"{i}. {item}")
        i += 1