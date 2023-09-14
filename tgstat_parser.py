import sys
from classes import Parser, Settings
import argparse
from multiprocessing import Pool
import shlex

# Функция для создания объекта Parser на основе пользовательского ввода
def create_parser_instance(settings_str):
    args = shlex.split(settings_str)
    parser_args = parse_arguments(args)
    if parser_args:
        p = Parser(Settings(
            grps_amount=parser_args.grps_amount,
            keyword=parser_args.keyword,
            region=parser_args.region,
            verify=parser_args.verify,
            subs=parser_args.subs,
            outp_file=parser_args.output,
            runmode=parser_args.runmode,
            filename=parser_args.filename
        ))
        p.scrap_data()
        p.save_data()

# Функция для парсинга именованных аргументов из списка
def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', type=str, required=True, help='Keyword argument "keyword"')
    parser.add_argument('--subs', type=int, required=False, help='Keyword argument "subs"')
    parser.add_argument('--grps_amount', type=int, required=False, help='Keyword argument "grps_amount"')
    parser.add_argument('--region', type=str, required=False, help='Keyword argument "region"')
    parser.add_argument('--verify', type=bool, required=False, help='Keyword argument "verify"')
    parser.add_argument('--output', type=str, default='json', help='Keyword argument "outp_file"')
    parser.add_argument('--runmode', type=str, required=False, help='Keyword argument "runmode"')
    parser.add_argument('-fn', '--filename', type=str, required=True, help='Keyword argument "runmode"')
    try:
        return parser.parse_args(args)
    except argparse.ArgumentError:
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TGStat Parser')
    parser.add_argument('-o', '--objects', type=int, default=1, help='Number of Parser objects to create')

    args = parser.parse_args()

    if args.objects == 1:
        cmd = input('Enter settings for the instance (space-separated): ')
        create_parser_instance(cmd)
    else:
        instances = []
        for i in range(args.objects):
            cmd = input(f'Enter settings for instance {i + 1} (space-separated): ')
            instances.append(cmd)

        # Создаем пул процессов
        with Pool(processes=args.objects) as pool:
            # Инициализируем объекты Parser в каждом процессе и выполняем scrap_data и save_data
            pool.map(create_parser_instance, instances)
            pool.terminate()
            sys.exit()