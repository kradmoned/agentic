from functions.write_file import write_file

print(write_file("calculator", "lorem.txt", "wait, this isn't lorem impsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file("calculator", "/temp/temp.txt", "this should not be allowed"))