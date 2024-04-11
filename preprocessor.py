import sys
import pandas as pd


class CSVPreprocessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self._load_data()
        self._preprocess()

    def _load_data(self):
        try:
            return pd.read_csv(self.filepath)
        except FileNotFoundError:
            print(f"Error: File {self.filepath} not found. Exiting application.")
            sys.exit(1)

    def _preprocess(self):
        self._filter_columns()
        self._aggregate_data()

    def _filter_columns(self):
        columns_to_keep = [
            "Handle",  # Column to group variants by
            "Title",
            "Vendor",  # If the user asks for clothes by specific brand
            "Type",  # If the user asks for specifc type of clothing
            "Tags",  # Additional product information for which the user might ask for
            # If the user asks for specific colors/sizes
            "Option1 Name",
            "Option1 Value",
            "Option2 Name",
            "Option2 Value",
            "Option3 Name",
            "Option3 Value",
            "Variant Price",
            "Image Src",
        ]
        self.data = self.data[columns_to_keep].copy()

    def _aggregate_data(self):
        option_value_columns = [f"Option{i} Value" for i in range(1, 4)]

        def join_option_values(values):
            return ", ".join({str(value) for value in values if pd.notnull(value)})

        agg_funcs = {
            col: join_option_values if col in option_value_columns else "first"
            for col in self.data.columns
        }

        self.data = self.data.groupby("Handle", as_index=False).agg(agg_funcs)
        self.data["Options"] = self.data.apply(self._combine_options, axis=1)
        self.data.drop(
            columns=[
                "Handle",
                "Option1 Name",
                "Option1 Value",
                "Option2 Name",
                "Option2 Value",
                "Option3 Name",
                "Option3 Value",
            ],
            inplace=True,
        )
        self.data.rename(columns={"Variant Price": "Price"}, inplace=True)

    def _combine_options(self, row):
        """Combines all option name-value pairs into a single string."""
        options = [
            f"{row[f'Option{i} Name'].capitalize()}: {row[f'Option{i} Value']}"
            for i in range(1, 4)
            if pd.notnull(row[f"Option{i} Name"])
            and pd.notnull(row[f"Option{i} Value"])
        ]
        return "; ".join(options)

    def trim_data(self, row_count=100):
        """Use this for testing to reduce the amount of tokens being used."""
        self.data = self.data.head(row_count)

    def save_preprocessed_file(self, output_filepath):
        self.data.to_csv(output_filepath, index=False)
