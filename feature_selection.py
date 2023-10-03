import argparse
import numpy as np
import pandas as pd
import models
import utils
import data_processing as dp

##########
import logging
import joblib
import cProfile

##########


def main(config_dict, config_path):
    """
    Central function to tie together preprocessing, running the models, and plotting
    """

    # Set the global seed
    np.random.seed(config_dict["ml"]["seed_num"])

    # Create the folders needed
    experiment_folder = utils.create_experiment_folders(config_dict, config_path)

    # Set up process logger
    omicLogger = utils.setup_logger(experiment_folder)

    try:
        omicLogger.info("Loading data...")

        # read the data
        x, y, features_names = dp.load_data(config_dict)
        omicLogger.info("Data Loaded. Splitting data...")

        if len(x.index.unique()) != x.shape[0]:
            raise ValueError("The sample index/names contain duplicate entries")

        # Split the data in train and test
        x_train, x_test, y_train, y_test = dp.split_data(x, y, config_dict)
        omicLogger.info("Data splitted. Standardising...")

        x_ind_train = x_train.index
        x_ind_test = x_test.index

        # standardise data
        x_train, SS = dp.standardize_data(x_train)  # fit the standardiser to the training data
        x_test = dp.transform_data(x_test, SS)  # transform the test data according to the fitted standardiser

        # save the standardiser transformer
        save_name = experiment_folder / "transformer_std.pkl"
        with open(save_name, "wb") as f:
            joblib.dump(SS, f)

        omicLogger.info("Data standardised, transformer saved. Selecting features...")

        # implement feature selection if desired
        if config_dict["ml"]["feature_selection"] is not None:
            x_train, features_names, FS = dp.feat_selection(
                experiment_folder,
                x_train,
                y_train,
                features_names,
                config_dict["ml"]["problem_type"],
                config_dict["ml"]["feature_selection"],
            )
            x_test = FS.transform(x_test)

            # Save the feature selection tranformer
            save_name = experiment_folder / "transformer_fs.pkl"
            with open(save_name, "wb") as f:
                joblib.dump(FS, f)

            omicLogger.info("Features selected, transformer saved. Re-combining data...")
        else:
            print("Skipping Feature selection.")
            omicLogger.info("Skipping feature selection. Re-combining data...")

        # concatenate both test and train into test
        x = np.concatenate((x_train, x_test))
        # y needs to be re-concatenated as the ordering of x may have been changed in splitting
        y = np.concatenate((y_train, y_test))

        # save the transformed input data
        x_df = pd.DataFrame(x, columns=features_names)
        x_df["set"] = "Train"
        x_df["set"].iloc[-x_test.shape[0] :] = "Test"
        x_df.index = list(x_ind_train) + list(x_ind_test)
        x_df.index.name = "SampleID"
        x_df.to_csv(experiment_folder / "transformed_model_input_data.csv", index=True)

        y_df = pd.DataFrame(y, columns=["target"])
        y_df["set"] = "Train"
        y_df["set"].iloc[-y_test.shape[0] :] = "Test"
        y_df.index = list(x_ind_train) + list(x_ind_test)
        y_df.index.name = "SampleID"
        y_df.to_csv(experiment_folder / "transformed_model_target_data.csv", index=True)

        omicLogger.info("Process completed.")
    except Exception as e:
        omicLogger.error(e, exc_info=True)
        logging.error(e, exc_info=True)
        raise e


def activate(args):
    parser = argparse.ArgumentParser(description="Explainable AI framework for omics")
    parser = utils.create_parser()
    args = parser.parse_args(args)
    config_path, config_dict = utils.initial_setup(args)

    # This handles pickling issues when cloning for cross-validation
    multiprocessing.set_start_method("spawn", force=True)
    # Run the models
    main(config_dict, config_path)


if __name__ == "__main__":
    # This handles pickling issues when cloning for cross-validation
    import multiprocessing

    multiprocessing.set_start_method("spawn", force=True)

    # Load the parser for command line (config files)
    parser = utils.create_parser()

    # Get the args
    args = parser.parse_args()

    # Do the initial setup
    config_path, config_dict = utils.initial_setup(args)

    # init the profiler to time function executions
    pr = cProfile.Profile()
    pr.enable()

    # Run the models
    main(config_dict, config_path)

    # save time profile information
    pr.disable()
    csv = dp.prof_to_csv(pr)
    with open(f"{config_dict['data']['save_path']}results/{config_dict['data']['name']}/time_profile.csv", "w+") as f:
        f.write(csv)
