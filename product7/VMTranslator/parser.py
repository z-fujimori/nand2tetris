from constants import *

class Parser():
    def __init__(self, filepath):
        self.current_command = None
        self.f_vm = open(filepath)

    # この二つを定義するとこのクラスがwithで使えるようになる！
    def __enter__(self):  # with開始時。asで受け取る値を返せる 
        return self
    def __exit__(self, exc_type, exc_value, traceback):  # withブロック終了時。4つの引数が必要。
        self.f_vm.close()

    def advance(self):
        while True:
            line = self.f_vm.readline()  # 1行だけ読み込む
            if not line:
                self.current_command = None
                return self.current_command
            
            line = line.strip()  # 両端のタブや改行を削除

            # コメントアウトを削除
            comment_index = line.find('//')
            if comment_index != -1:
                line = line[:comment_index]
            
            # 何か書いてあったらコマンドにセット。何もなかったら次のループへGo。
            if line != '':
                self.current_command = line.split()  # スペースで区切って配列に
                return self.current_command

    def commandType(self):
        comand = self.current_command[0]
        if comand == "push":
            return C_PUSH
        elif comand == "pop":
            return C_POP
        elif comand == "label":
            return C_LABEL
        elif comand == "goto":
            return C_GOTO
        elif comand == "if-goto":
            return C_IF
        elif comand == "function":
            return C_FUNCTION
        elif comand == "return":
            return C_RETURN
        elif comand == "call":
            return C_CALL
        elif comand in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return C_ARITHMETIC

    def arg1(self):
        if self.command_type() == C_ARITHMETIC:
            return self.current_command[0]
        else:
            return self.current_command[1]

    def arg2(self):
        if self.command_type() in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
            return self.current_command[2]
