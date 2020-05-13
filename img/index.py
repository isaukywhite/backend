import sys
from tkinter.filedialog import askopenfilename
from methods import filters as ft
from methods import convolution_filters as conv


def main():

    print('')
    print('Escolha uma opção:')
    print('')
    print('1. Filtro de Limiar')
    print('2. Filtro de Limiar em Y')
    print('3. Mostrar imagem em R, G, B or Cinza')
    print('4. Converter imagem RGB em YIQ ou vice-versa')
    print('5. Filtro Negativo')
    print('6. Aumentar Brilho')
    print('7. Multiplaicar Brilho')
    print('8. Filtro de Convolução do Kernel')
    print('9. Filtro de Convolução do Sobel')
    print('10. Filtro Medial')
    print('11. Mostrar imagem em YIQ')
    print('')
    option = input()
    filename = askopenfilename()

    if option == "1":
        print('Escolha entre 0 e 255:')
        measure = input()
        print('Tipo de imagem:')
        print('1. Monocromatica')
        print('2. Colorida')
        imgType = input()
        ft.thresholding(filename, measure, imgType)
    elif option == "2":
        print('1. Inserir Medida')
        print('2. Tirar Media')
        choose = input()
        if choose == '1':
            print('Escolha entre 0 e 255:')
            measure = input()
            ft.thresholding_y(filename, choose, measure)
        else:
            ft.thresholding_y(filename, choose, 'measure')
    elif option == "3":
        print('1. Red')
        print('2. Green')
        print('3. Blue')
        print('4. Gray')
        color = input()
        if color == "1":
            ft.show_rgb(filename, 'red')
        elif color == "2":
            ft.show_rgb(filename, 'green')
        elif color == "3":
            ft.show_rgb(filename, 'blue')
        elif color == "4":
            ft.show_rgb(filename, 'gray')
    elif option == "4":
        ft.rgb_yiq_rgb(filename)
    elif option == "5":
        print('1. RGB')
        print('2. YIQ')
        print('3. RGB YIQ RGB')
        measure = input()
        ft.negative(filename, measure)
    elif option == "6":
        print('Insira uma medida de aumento:')
        measure = input()
        ft.brightness_handler(filename, measure, 'add')
    elif option == "7":
        print('Insira uma medida multiplicada:')
        measure = input()
        ft.brightness_handler(filename, measure, 'multiply')

    elif option == "8":
        mask = askopenfilename()
        conv.kernel_filter(filename, mask)
    elif option == "9":
        mask = askopenfilename()
        conv.sobel_filter(filename, mask)
    elif option == "10":
        mask = askopenfilename()
        conv.median_filter(filename, mask)
    elif option == "11":
        ft.show_yiq(filename)
    else:
        print('Fechado!')


if __name__ == '__main__':
    main()
