from tkinter import *


def converter(expression: str) -> str:
    """Converts numbers to decimal notation and returns the result in the specified system"""
    
    dct_dec_to_sym = {n - 48: chr(n) for n in range(48, 58)}
    dct_symbols = {n - 55: chr(n) for n in range(65, 91)}
    dct_dec_to_sym.update(dct_symbols)
    
    dct_sym_to_dec = {v: k for k, v in dct_dec_to_sym.items()}
    
    def decimal_to_p(n: float, p: int) -> str:
        """Converts a decimal number 'n' to a number based on 'p'"""
        nonlocal dct_dec_to_sym
        
        int_part, fract_part = divmod(n, 1)
        int_part, fract_part = (int(int_part), fract_part) if fract_part else (int(int_part), 0)
        
        intp, fractp = divmod(int_part, p)
        res_int_part = [fractp]
        while intp:
            intp, fractp = divmod(intp, p)
            res_int_part.append(fractp)
        res_int_part = ''.join(dct_dec_to_sym[e] for e in res_int_part[-1::-1])
        
        intp, fractp = divmod(fract_part * p, 1)
        res_fract_part, Eps = [int(intp)], 0.001
        while fractp > Eps:
            intp, fractp = divmod(fractp * p, 1)
            res_fract_part.append(int(intp))
        res_fract_part = ''.join(dct_dec_to_sym[e] for e in res_fract_part)
        
        return '.'.join([res_int_part, res_fract_part]) if fract_part else res_int_part
    
    def p_to_decimal(s: str, p: int) -> float:
        """Converts the number 's' of the system based on 'p' to a decimal number"""
        nonlocal dct_sym_to_dec
        
        i = s.index('.') if '.' in s else 0
        int_part, fract_part = ([dct_sym_to_dec[e] for e in s[i - 1::-1]], [dct_sym_to_dec[e] for e in s[i + 1:]]) \
            if i else ([dct_sym_to_dec[e] for e in s[::-1]], 0)
        res_int_part, res_fract_part = (sum([e * p ** i for i, e in enumerate(int_part)]),
                                        sum([e * p ** (-i - 1) for i, e in enumerate(fract_part)])) if fract_part \
            else (sum([e * p ** i for i, e in enumerate(int_part)]), 0)
        
        return res_int_part + res_fract_part
    
    def parser() -> (list, int):
        lst = expression.split()
        print(lst)
        expr, res_p = (lst[:-2], lst[-1]) if '>' in lst[-1:-4:-1] else (lst, 10)
        print(expr, res_p)
        res = []
        for e in expr:
            if e not in '+-*/':
                tmp = tuple(e.split('_')) if '_' in e else (e, 10)
                res.append(tmp)
            else:
                res.append(e)
        print(res)
        return res, int(res_p)
    
    def all_p_to_decimal() -> (list, int):
        expr, res_p = parser()
        res = []
        for e in expr:
            if isinstance(e, tuple):
                res.append(p_to_decimal(e[0], int(e[1])))
            else:
                res.append(e)
        print('converted to decimals')
        print(res)
        return res, res_p
    
    decimals, res_p = all_p_to_decimal()
    res = decimal_to_p(eval(''.join(str(e) for e in decimals)), res_p)
    return res


def start():
    """Starts the calculator"""
    
    def btn_click(item):
        nonlocal expression
        
        try:
            input_field['state'] = 'normal'
            output_field['state'] = 'normal'
            if item in '>+-*/=':
                expression += ' ' + item + ' '
                input_field.insert(END, ' ' + item + ' ')
            else:
                expression += item
                input_field.insert(END, item)
            
            if item == '=':
                print(f'expression is: {expression}')
                result = converter(expression[:-2])
                input_field.insert(END, result)
                output_field.insert(0, result)
                expression = ''
            input_field['state'] = 'readonly'
        
        except ZeroDivisionError:
            input_field.delete(0, END)
            input_field.insert(0, 'Деление на 0')
        except SyntaxError:
            input_field.delete(0, END)
            input_field.insert(0, 'Ошибка')
    
    def btn_clear():
        nonlocal expression
        expression = ''
        input_field['state'] = 'normal'
        input_field.delete(0, END)
        input_field['state'] = 'readonly'
        
        output_field['state'] = 'normal'
        output_field.delete(0, END)
        output_field['state'] = 'readonly'
    
    def btn_del():
        nonlocal expression
        print(expression)
        expression = expression[:-1] if expression[-1] != ' ' else expression[:-2]
        print(expression)
        input_field['state'] = 'normal'
        input_field.delete(0, END)
        input_field.insert(END, expression)
        input_field['state'] = 'readonly'
    
    root = Tk()
    # root.geometry('268x288') 346
    root.geometry('775x288')
    root.resizable(True, True)
    root.title('Calculator of number systems (up to 36 point system). '
               'Use: 2 + 2 = 4 or '
               '100101_2 + 34_7 * 10  + 56_8 > 16 = 14D or '
               '46255 > 36 = ZOV or '
               '1L_36 = 57. '
               '(C) Belous, 2023')
    
    frame_input = Frame(root)
    frame_input.grid(row=0, column=0, columnspan=11, sticky='nsew')
    input_field = Entry(frame_input, font='Arial 15 bold', width=70, state='readonly')
    input_field.pack(fill=BOTH)
    
    frame_out = Frame(root)
    frame_out.grid(row=1, column=0, columnspan=9, sticky='nsew')
    output_field = Entry(frame_out, font='Arial 15 bold', width=58, state='readonly')
    output_field.pack(fill='none')
    
    buttons = (('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '11'),
               ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', '-', '11'),
               ('K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', '*', '11'),
               ('U', 'V', 'W', 'X', 'Y', 'Z', '.', '_', '>', '=', '/', '11'))
    
    expression = ''
    
    button_clear = Button(root, text='C', command=lambda: btn_clear())
    button_clear.grid(row=1, column=10, sticky='nsew')
    
    button_del = Button(root, text='<-', command=lambda: btn_del())
    button_del.grid(row=1, column=9, sticky='nsew')
    
    for row in range(4):
        for col in range(11):
            Button(root, width=2, height=3, text=buttons[row][col],
                    command=lambda row=row, col=col: btn_click(
                            buttons[row][col])).grid(row=row + 2, column=col, sticky='nsew', padx=1, pady=1)
    
    root.mainloop()


if __name__ == '__main__':
    start()
