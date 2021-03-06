import importlib
import argparse


default_usecase = 'GASchedulerTestUseCase'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Task Scheduling Algorithms based on Machine Learning')
    parser.add_argument('--usecase', metavar='U', default=default_usecase,
                        help='use case from folder `usecases`')
    args = parser.parse_args()

    UseCasePacket = importlib.import_module('usecases.' + args.usecase)
    usecase = getattr(UseCasePacket, args.usecase)
    usecase.run()
