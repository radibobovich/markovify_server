with open('telegram_@best_reserve.log', 'r', encoding='utf-8') as file:
    lines = file.readlines()

output_lines = []
for line in lines:
    # Разделение строки по двоеточиям и выбор второго элемента
    parts = line.split(':', 2)
    if len(parts) > 2:
        output_lines.append(':'.join(parts[2:])[1:])

with open('lr_clean.txt', 'w', encoding='utf-8') as file:
    file.writelines(output_lines)
