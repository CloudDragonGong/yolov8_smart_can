# 要表示的大整数
large_integer = 1000

# 将大整数转换为二进制表示（4个字节，大端序）
byte_representation = large_integer.to_bytes(4, byteorder='big')

# 打印结果
print(byte_representation)
