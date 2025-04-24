from constants import *

class CodeWriter():
    def __init__(self, file_path) -> None:
        self.f = open(file_path, 'w')
        self.label_num = 0

    # この二つを定義するとこのクラスがwithで使えるようになる！
    def __enter__(self):  # with開始時。asで受け取る値を返せる 
        return self
    def __exit__(self, exc_type, exc_value, traceback):  # withブロック終了時　4つの引数が必要。
        self.f.close()


    def write_push_pop(self, command, segment, index):
        index = int(index)
        if command == C_PUSH:
            if segment == "constant":
                self.write_codes([
                    "@%d" % index,
                    'D=A'
                ])
                self.write_push_from_d()
                #
                # 続きはここから
                #
        elif command == C_POP:
            if segment in ["local", "argument", "this", "that"]:
                self.write_pop_from_virtual_segment(segment, index)


    def set_file_name(self, file_name):
        self.file_name = file_name

    def write_binary_operation(self, command):
        self.write_pop_to_m()
        self.write_code('D=M')
        self.write_pop_to_m()
        if command == 'add':
            self.write_code('D=D+M')
        elif command == 'sub':
            self.write_code('D=D-M')
        elif command == 'and':
            self.write_code('D=D&M')
        elif command == 'or':
            self.write_code('D=D|M')
        self.write_push_from_d()

    def write_push_from_d(self):
        self.write_codes([
            '@SP',
            'A=M',  # 上の行とセット。SPのアドレスをAにセットして次の行のMをSPが指すアドレスにするため
            'M=D',
            '@SP',
            'M=M+1'
        ])

    def write_pop_to_m(self):
        self.write_codes([
            '@SP',
            'M=M-1',
            'A=M'
        ])

    
    def write_code(self, code):
        self.f.write(code + '\n')
    
    def write_codes(self, codes):
        self.write_code('\n'.join(codes))  # 改行記号を間に挟んで結合