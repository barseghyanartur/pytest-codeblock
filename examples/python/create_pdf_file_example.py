from fake import FAKER

file = FAKER.pdf_file()

assert file.data["storage"].exists(str(file))
