import h5py
import numpy as np
import pandas as pd


def load_wavelengths(dir_path):
    """
    Reads part of HDF5 train file and returns wavelength calibration.

    :param dir_path: path to directory where datasets are stored
    :return: numpy 1D array (vector) with wavelength calibration
    """
    print("Reading wavelengths ... ", end="", flush=True)
    with h5py.File(dir_path + "contest_TRAIN.h5", 'r') as train_file:
        wavelengths = train_file["Wavelengths"]["1"][:]
    print("done")
    return wavelengths


def load_train_data(dir_path, spectra_count=100):
    """
    Reads HDF5 train file and returns spectra of training dataset in form of
    numpy 2D array (matrix) with spectra in rows. Full train dataset contains
    100 samples, each with 500 spectra. Use 'spectra_count' parameter
    to set the number of spectra per sample to be taken.

    :param dir_path: path to directory where datasets are stored
    :param spectra_count: number of spectra per sample to be loaded
                          from full train dataset (default: 100)
    :return: numpy 2D array (matrix) with train spectra in rows
    """
    print("Reading TRAIN samples (100 samples; {} spectra per sample):"
          .format(spectra_count))
    train_data = []   
    with h5py.File(dir_path + "contest_TRAIN.h5", 'r') as train_file:
        for i_sample, sample in train_file["Spectra"].items():
            print("\r-> sample: {}".format(i_sample), end='', flush=True)
            train_data.append(sample[:, :spectra_count].transpose())
    print("\n-> combining samples into final matrix ... ", end="", flush=True)
    train_data = np.concatenate(train_data)
    print("done [shape: {}]".format(train_data.shape))
    return train_data


def load_train_labels(dir_path, spectra_count=100):
    """
    Reads part of HDF5 train file and returns class labels for train dataset
    based on 'spectra_count' parameter. Make sure to choose the same value
    of the parameter as in 'load_train_data()'. For more details see
    'load_train_data()'.

    :param dir_path: path to directory where datasets are stored
    :param spectra_count: number of spectra per sample to be loaded from full
                          train dataset (default: 100)
    :return: numpy 1D array (vector) with class labels of train dataset
    """
    print("Reading TRAIN labels ... ", end="", flush=True)
    train_labels = []
    with h5py.File(dir_path + "contest_TRAIN.h5", 'r') as train_file:
        all_labels = train_file["Class"]["1"]
        for i in range(0, 50000, 500):
            train_labels.extend(all_labels[i:i+spectra_count])
    train_labels = np.array(train_labels, dtype=int)
    print("done")
    return train_labels


def load_test_data(dir_path):
    """
    Reads HDF5 test file and returns spectra of whole test dataset in form
    of numpy 2D array (matrix) with spectra in rows.

    :param dir_path: path to directory where datasets are stored
    :return: numpy 2D array (matrix) with test spectra in rows
    """
    print("Reading TEST samples (2 blocks per 10000 spectra):")
    test_data = np.ndarray((20000, 40002))
    with h5py.File(dir_path + "contest_TEST.h5", 'r') as test_file:
        for i_block, block in test_file["UNKNOWN"].items():
            print("-> block {} ... ".format(i_block), end="", flush=True)
            spectra = block[:].transpose()
            for i_spec in range(10000):
                test_data[(10000*(int(i_block)-1))+i_spec] = spectra[i_spec]
            print("done", flush=True)
            del spectra
    return test_data


def train_to_numpy_pickle(dir_path, spectra_count=100):
    """
    Loads train dataset (wavelengths, class labels and spectra) and stores
    them to numpy pickles (.npy) in the same folder. Loading numpy pickles
    is faster than reading HDF5 (.h5) file, but there is no compression, so
    they require more space on disk. For more info about pickles, see
    https://docs.python.org/3/library/pickle.html.

    :param dir_path: path to directory where are datasets stored and pickles
                     are to be saved
    :param spectra_count: number of spectra per sample to be loaded from full
                          train dataset (default: 100)
    """
    # Load and save wavelengths
    wavelengths = load_wavelengths(dir_path)
    np.save(dir_path + "contest_wavelengths.npy", wavelengths)
    # Load and save class labels
    y_train = load_train_labels(dir_path, spectra_count)
    np.save(dir_path + "contest_TRAIN-{}-labels.npy".format(spectra_count),
            y_train)
    # Load and save spectra
    x_train = load_train_data(dir_path, spectra_count)
    np.save(dir_path + "contest_TRAIN-{}-data.npy".format(spectra_count),
            x_train)


def test_to_numpy_pickle(dir_path):
    """
    Loads test dataset and stores it to numpy pickle (.npy) in the same folder.
    For more info about pickles, see 'train_to_numpy_pickle()' or
    https://docs.python.org/3/library/pickle.html.

    :param dir_path: path to directory where are datasets stored and pickles
                     are to be saved
    """
    # Load and save spectra
    x_test = load_test_data(dir_path)
    np.save(dir_path + "contest_TEST.npy", x_test)


def train_to_pandas_pickle(dir_path, spectra_count=100):
    """
    Loads train dataset (wavelengths, class labels and spectra), combine them
    into a Pandas DataFrame and stores it into a pickle. For more info about pickles,
    see 'train_to_numpy_pickle()' or https://docs.python.org/3/library/pickle.html.

    :param dir_path: path to directory where are datasets stored and pickles
                     are to be saved
    :param spectra_count: number of spectra per sample to be loaded from full
                          train dataset (default: 100)
    """
    # Load and round wavelengths
    wavelengths = np.round(load_wavelengths(dir_path), 2)
    # Load class labels
    y_train = load_train_labels(dir_path, spectra_count)
    # Load spectra
    x_train = load_train_data(dir_path, spectra_count)
    # Create and save Pandas DataFrame into pickle
    df = pd.DataFrame(x_train, columns=wavelengths)
    df['class'] = y_train
    df.to_pickle(dir_path + "contest_TRAIN-{}.pkl".format(spectra_count))


def test_to_pandas_pickle(dir_path):
    """
    Loads test dataset (wavelengths and spectra), combine them into a Pandas DataFrame
    and stores it into a pickle. For more info about pickles, see 'train_to_numpy_pickle()'
    or https://docs.python.org/3/library/pickle.html.
    Note: Saving Pandas DataFrame into pickle takes significantly more time than using
    numpy.

    :param dir_path: path to directory where are datasets stored and pickles
                     are to be saved
    """
    # Load and round wavelengths
    wavelengths = np.round(load_wavelengths(dir_path), 2)
    # Load spectra
    x_test = load_test_data(dir_path)
    # Create and save Pandas DataFrame into pickle
    print("-> creating Pandas DataFrame ... ", end="", flush=True)
    df = pd.DataFrame(x_test, columns=wavelengths)
    print("done")
    print("-> writing DataFrame into pickle ... ", end="", flush=True)
    df.to_pickle(dir_path + "contest_TEST.pkl")
    print("done")


if __name__ == "__main__":
    datasets_dir = "../datasets/"
    train_to_pandas_pickle(datasets_dir, 50)
    test_to_pandas_pickle(datasets_dir)
