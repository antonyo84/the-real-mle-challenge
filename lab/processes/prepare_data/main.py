
from pathlib import Path

from airbnb_data import prepare_airbnb_data


DIR_REPO = Path.cwd().parent.parent
DIR_DATA_RAW = Path(DIR_REPO) / "data" / "raw"

DIR_DATA_PROCESSED = Path(DIR_REPO) / "data" / "processed"
FILEPATH_DATA = DIR_DATA_PROCESSED / "preprocessed_listings_test.csv"

if __name__ == "__main__":

    prepare_airbnb_data(dir_input=DIR_DATA_RAW, output_file_path=FILEPATH_DATA)
