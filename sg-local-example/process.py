import numpy as np
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-ratio', type=float)
    parser.add_argument('--output-dir', type=str)
    return parser.parse_args()

def main():
    args = parse_args()
    print(args)

    rng = np.random.RandomState(42)
    # Generate train data
    X = 0.3 * rng.randn(300, 2)
    X_train = np.r_[X + 2, X - 2]
    normal_observations = pd.DataFrame(X_train)
    normal_observations['target'] = 0
    # Generate some abnormal novel observations
    X_outliers = rng.uniform(low=-4, high=4, size=(40, 2))
    novelty_observations = pd.DataFrame(X_outliers)
    novelty_observations['target'] = 1

    # Merge observations and train test split dataset
    dataset = pd.concat([novelty_observations, normal_observations])
 
    X_train, X_test = train_test_split(dataset)

    # Save datasets
    X_train.to_csv(f'{args.output_dir}train.csv')
    X_test.to_csv(f'{args.output_dir}test.csv')
    print(f'{args.output_dir}train.csv')

if __name__ == '__main__':
    main()