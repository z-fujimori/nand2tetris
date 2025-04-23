import argparse

def main():
    parser = argparse.ArgumentParser(description="VM → アセンブリの変換を行います")
    parser.add_argument("path", help="ファイルパスを指定")

    args = parser.parse_args()
    path = args.path
    print(f"{path}")

    if path.endswith(".vm"):  # 末尾が.vmかを確認してファイルとフォルダ判別
        asm_path = path[:-3] + ".asm"

def translate(vm_file, asm_file):
    print()


if __name__ == "__main__":
    main()
