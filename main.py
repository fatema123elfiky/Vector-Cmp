import VectorQuantization as VQ

while True:
    print('\nWelcome to the Vector Quantization Program')
    print('1. Vector Quantization Compression\n2. Vector Quantization Decompression\n3. Quit')
    choice = input('Enter your choice: ')

    if choice == '1':
        VQ.compress()

    elif choice == '2':
        VQ.decompress()

    elif choice == '3':
        print('Thank you for using this program')
        break

    else:
        print('Invalid choice')

