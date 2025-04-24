import argparse
from code_writer import CodeWriter
from parser import Parser
import os
from constants import *

def main():
    parser = argparse.ArgumentParser(description="VM → アセンブリの変換を行います")
    parser.add_argument("path", help="ファイルパスを指定")

    args = parser.parse_args()
    path = args.path
    print(f"{path}")

    if path.endswith(".vm"):  # 末尾が.vmかを確認してファイルとフォルダ判別
        asm_path = path[:-3] + ".asm"
        with CodeWriter(asm_path) as code_writer:
            translate(path, code_writer)

def translate(file_path, code_writer):
    filename, _ = os.path.splitext(os.path.basename(file_path))  # 拡張子なし(pathからファイル名の部分を抜きだし)
    code_writer.set_file_name(filename)
    with Parser(file_path) as parser:
        parser.advance()
        while parser.current_command != None:
            print(parser.current_command)
            if parser.commandType() == C_ARITHMETIC:
                code_writer.writeArithmetic(parser.arg1())
            elif parser.command_type() == C_PUSH:
                code_writer.write_push_pop(C_PUSH, parser.arg1(), parser.arg2())
            elif parser.command_type() == C_POP:
                code_writer.write_push_pop(C_POP, parser.arg1(), parser.arg2())

            parser.advance()

if __name__ == "__main__":
    main()
