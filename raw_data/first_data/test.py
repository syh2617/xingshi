import PyPDF2


pages_to_keep = {1, 2, 7, 8, 51, 52, 53, 54, 75, 76, 83, 84}


with open('1.pdf', 'rb') as file:
    pdf = PyPDF2.PdfReader(file)


    writer = PyPDF2.PdfWriter()


    for page_num in range(len(pdf.pages)):
        if page_num+1 in pages_to_keep:
            writer.add_page(pdf.pages[page_num])


    with open('new_1.pdf', 'wb') as new_file:
        writer.write(new_file)

print("指定页面已被保留，并存储为new_1.pdf文件")
