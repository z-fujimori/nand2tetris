from constants import *

class CodeWriter():
    def __init__(self, file_path) -> None:
        self.f = open(file_path, 'w')
        self.if_label_num = 0
        self.return_label_num = 0

        self.write_init()

    # この二つを定義するとこのクラスがwithで使えるようになる！
    def __enter__(self):  # with開始時。asで受け取る値を返せる 
        return self
    def __exit__(self, exc_type, exc_value, traceback):  # withブロック終了時　4つの引数が必要。
        self.f.close()

    def write_init(self):
        self.write_set_sp(256) # スタックが256から始まることを定義
        self.write_call("Sys.init", 0)
    # スタックのポインタを管理
    def write_set_sp(self, address):
        self.write_codes([
            '@%d' % address,
            'D=A',
            '@SP',
            'M=D'
        ])
    def write_call(self, function_name, num_of_args):
        return_label = self.get_new_return_label()
        self.write_codes([
            '// return-label',
            '@%s' % return_label,
            'D=A'
        ])
        self.write_push_from_d()  # push return-address
        self.write_codes([
            '@LCL',
            'D=M',
        ])
        self.write_push_from_d()
        self.write_codes([
            '@ARG',
            'D=M',
        ])
        self.write_push_from_d()
        self.write_codes([
            '@THIS',
            'D=M',
        ])
        self.write_push_from_d()
        self.write_codes([
            '@THAT',
            'D=M',
        ])
        self.write_push_from_d()
        self.write_codes([
            '@SP',
            'D=M',
            '@5',
            'D=D-A',
            '@%d' % int(num_of_args),
            'D=D-A',
            '@ARG',
            'M=D',  # ARG = SP - n - 5
            '@SP',
            'D=M',
            '@LCL',
            'M=D'  # LCL = SP
        ])
        self.write_codes([
            '@%s' % function_name,
            '0;JMP',  # goto function
            '(%s)' % return_label
        ])
    def get_new_return_label(self):
        self.return_label_num += 1
        return '_RETURN_LABEL_' + str(self.return_label_num)


    def writeArithmetic(self, command):
        if command in ["add", "sub", "and", "or"]:
            self.write_binary_operation(command)
        elif command in ["neg", "not"]:
            self.write_unary_operation(command)
        elif command in ["eq", "gt", "lt"]:
            self.write_binary_operation(command)

    def write_push_pop(self, command, segment, index):
        index = int(index)
        if command == C_PUSH:
            if segment == "constant":
                self.write_codes([
                    "@%d" % index,
                    'D=A'
                ])
                self.write_push_from_d()
            elif segment in ["local", "argument", "this", "that"]:
                self.write_push_from_virtual_segment(segment, index)
            elif segment in ["temp", "pointer"]:
                self.write_push_from_static_segment(segment, index)
            if segment == "static":
                self.write_codes([
                    "@%s.%d" % (self.file_name, index),
                ])
                self.write_code('D=M')
                self.write_push_from_d()

        elif command == C_POP:
            if segment in ["local", "argument", "this", "that"]:
                self.write_pop_from_virtual_segment(segment, index)
            elif segment in ["temp", "pointer"]:
                self.write_pop_from_static_segment(segment, index)
            if segment == "static":
                self.write_pop_to_m()
                self.write_codes([
                    'D=M',
                    '@%s.%d' % (self.file_name, index),
                ])
                self.write_code('M=D')

    def set_file_name(self, file_name):
        self.file_name = file_name

    def write_push_from_virtual_segment(self, segment, index):
        if segment == "local":
            register_name = "LCL"
        elif segment == "argument":
            register_name = "ARG"
        elif segment == "this":
            register_name = "THIS"
        elif segment == "that":
            register_name = "THAT"
        self.write_codes([
            '@%s' % register_name,
            'A=M'
        ])
        for i in range(index):
            self.write_code('A=A+1')
        self.write_code('D=M')
        self.write_push_from_d()

    def write_pop_from_virtual_segment(self, segment, index):
        if segment == "local":
            register_name = "LCL"
        elif segment == "argument":
            register_name = "ARG"
        elif segment == "this":
            register_name = "THIS"
        elif segment == "that":
            register_name = "THAT"
        self.write_pop_to_m()
        self.write_codes([
            'D=M',
            '@%s' % register_name,
            'A=M'
        ])
        for i in range(index):
            self.write_code('A=A+1')
        self.write_code('M=D')
    
    def write_push_from_static_segment(self, segment, index):
        if segment == "temp":
            base_address = TEMP_BASE_ADDRESS
        elif segment == "pointer":
            base_address = POINTER_BASE_ADDRESS
        self.write_codes([
            "@%d" % base_address,
        ])
        for i in range(index):
            self.write_code('A=A+1')
        self.write_code('D=M')
        self.write_push_from_d()

    def write_pop_from_static_segment(self, segment, index):
        if segment == "temp":
            base_address = TEMP_BASE_ADDRESS
        elif segment == "pointer":
            base_address = POINTER_BASE_ADDRESS
        self.write_pop_to_m()
        self.write_codes([
            'D=M',
            '@%d' % base_address,
        ])
        for i in range(index):
            self.write_code('A=A+1')
        self.write_code('M=D')

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

    def write_unary_operation(self, command):
        self.write_codes([
            '@SP',
            'A=M-1',
        ])
        if command == 'neg':
            self.write_code('M=-M')
        elif command == 'not':
            self.write_code('M=!M')

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

    # labelの時
    def write_named_label(self, label):
        print("test: (%s)" % self.get_label_name(label))
        self.write_code("(%s)" % self.get_label_name(label))

    def get_label_name(self, label):
        try:
            return "%s$%s" % (self.current_function_name, label)
        except AttributeError:
            return "%s$%s" % ("null", label)
    
    # gotoの時
    def write_goto(self, label):
        self.write_codes([
            "@%s" % self.get_label_name(label),
            '0;JMP'
        ])

    # ifの時
    def write_if(self, label):
        self.write_pop_to_m()
        self.write_codes([
            'D=M',
            '@%s' % self.get_label_name(label),
            "D;JNE"
        ])