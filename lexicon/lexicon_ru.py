def donate_message(bills: dict):
    bill_info = ''
    for bank_name, bill_number in bills.items():
        bill_info += f'{bank_name}: `{bill_number}`\n'
    return (f'Мне будет очень приятно, если вы поддержите проект рублём\\.\n'
            f'{bill_info}')


LEXICON_RU: dict[str, str] = {
    'forward': '>>',
    'backward': '<<',
    '/start': 'hello epta',
    '/settings': 'here description of settings',
    '/analyze': 'send me file',
    '/help': 'this is how you can use bot',
    'not_analyze_state': 'Если ты хочешь загрузить файл - используй команду /analyze',
}

LEXICON_MENU: dict[str, str] = {
    '/analyze': 'Вывести слова и количество их появлений в книге',
    '/settings': 'Настроить вывод слов',
    '/help': 'Как пользоваться ботом',
    '/donate': 'Поблагодарить разработчика',
}
a = {'Юmoney': '4100 1188 6516 7780', 'Тинькоф': '5536 9138 6122 2186'}
donate_message(a)