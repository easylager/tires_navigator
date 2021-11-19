import easyocr

def text_recognition(file_path):
    reader = easyocr.Reader(['ru'])
    result = reader.readtext(file_path, detail=0)
    return result

def main():
    phone_number = text_recognition(file_path='../telephone.png')
    print(phone_number)


if __name__ == '__main__':
    main()