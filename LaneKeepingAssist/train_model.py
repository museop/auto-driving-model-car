import argparse
from steering_model import SteeringModel

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='train steering angle')
    parser.add_argument('-d', help='data directory',        dest='data_dir',          type=str,   default='data')
    parser.add_argument('-t', help='test size fraction',    dest='test_size',         type=float, default=0.2)
    parser.add_argument('-k', help='drop out probability',  dest='keep_prob',         type=float, default=0.5)
    parser.add_argument('-n', help='number of epochs',      dest='nb_epoch',          type=int,   default=10)
    parser.add_argument('-s', help='samples per epoch',     dest='samples_per_epoch', type=int,   default=20000)
    parser.add_argument('-b', help='batch size',            dest='batch_size',        type=int,   default=40)
    parser.add_argument('-l', help='learning rate',         dest='learning_rate',     type=float, default=1.0e-4)
    parser.add_argument('-p', help='previous model',        dest='previous_model',    type=str,   default='none')
    args = parser.parse_args()
    
    print('-' * 30)
    print('Parameters')
    print('-' * 30)
    for key, value in vars(args).items():
        print('{:<20} := {}'.format(key, value))
    print('-' * 30)
    
    steering_model = SteeringModel()
    if args.previous_model == 'none':
        steering_model.build_model( args.keep_prob )
    else:
        steering_model.load_model_from( args.previous_model )

    steering_model.train_model( args.data_dir,
                                args.learning_rate,
                                args.batch_size,
                                args.samples_per_epoch,
                                args.nb_epoch,
                                args.test_size )
        
    del steering_model
