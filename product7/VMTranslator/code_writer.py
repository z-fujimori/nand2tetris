class CodeWriter():
    def __init__(self, file_path) -> None:
        self.f = open(file_path, 'w')
        self.label_num = 0

    # この二つを定義するとこのクラスがwithで使えるようになる！
    def __enter__(self):  # with開始時。asで受け取る値を返せる 
        return self
    def __exit__(self, exc_type, exc_value, traceback):  # withブロック終了時　4つの引数が必要。
        self.f.close()

    def set_file_name(self, file_name):
        self.file_name = file_name