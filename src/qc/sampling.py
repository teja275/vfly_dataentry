import numpy as np
import scipy.stats as stats
import openpyxl
from openpyxl.styles import PatternFill
from itertools import product

# step 1 -> construct 2 arrays. array1 would be a 2d array with cell references and array 2 would be a 2d array with
# the corresponding sheet references
# probabilities would be given as input
# step 2 -> Using probabilities for columns, sample the columns and rows using uniform distribution. output the indices.
# step 3 -> Using the indices, get the cell references and sheet references as 2 arrays
# step 4 -> Using the cell references and sheet references, highlight the cells in the excel sheet


def create_sheet_cell_references(file_path):
    workbook = openpyxl.load_workbook(file_path)
    cell_references = []
    sheet_references = []
    for sheet in workbook.worksheets:
        columns = [chr(col + 65) for col in range(sheet.max_column)]
        rows = range(2, sheet.max_row + 1)
        cell_references.extend([f"{col}{row}" for row, col in product(rows, columns)])
        sheet_references.extend([sheet.title] * sheet.max_row * sheet.max_column)
    cell_references = np.array(cell_references).reshape(-1, sheet.max_column)
    sheet_references = np.array(sheet_references).reshape(-1, sheet.max_column)
    # cell_references.reshape(-1, sheet.max_column)
    # sheet_references.reshape(-1, sheet.max_column)
    return cell_references, sheet_references, workbook


def sample_cells_with_probabilities(
    cell_references, sheet_references, n, column_probabilities=None, seed=1234
):
    if column_probabilities is None:
        column_probabilities = (
            np.ones(cell_references.shape[1]) / cell_references.shape[1]
        )
    else:
        column_probabilities = np.array(column_probabilities)
        # Normalize probabilities in each column
        normalized_probabilities = column_probabilities / column_probabilities.sum()

    # Generate random indices based on column-wise probabilities
    column_indices = np.random.choice(
        cell_references.shape[1], size=n, p=normalized_probabilities
    )

    # Generate random indices for rows
    row_indices = np.random.choice(cell_references.shape[0], size=n)

    # Combine row and column indices to get the final sampled coordinates
    sampled_coordinates = (row_indices, column_indices)

    # Get the sampled elements
    sampled_cell_references = cell_references[sampled_coordinates]
    sampled_sheet_references = sheet_references[sampled_coordinates]

    return sampled_coordinates, sampled_cell_references, sampled_sheet_references


def highlight_cells_workbook(
    workbook, sampled_cell_references, sampled_sheet_references
):
    yellow_fill = PatternFill(
        start_color="FFFF00", end_color="FFFF00", fill_type="solid"
    )
    for sheet_name in workbook.sheetnames:
        worksheet = workbook[sheet_name]
        for cell in sampled_cell_references[sampled_sheet_references == sheet_name]:
            worksheet[cell].fill = yellow_fill


def calculate_sample_size(observed_error_rate, confidence_level, margin_of_error):
    z_score = np.abs(stats.norm.ppf((1 + confidence_level) / 2))
    # Calculate sample size (n)
    sample_size = (
        z_score**2 * observed_error_rate * (1 - observed_error_rate)
    ) / margin_of_error**2

    # Round up to the nearest integer since the sample size must be a whole number
    sample_size = int(np.ceil(sample_size))

    return sample_size


if __name__ == "__main__":
    file_path = "/Users/bhanuteja/Downloads/qc_report_sampling.xlsx"
    observed_error_rate = 0.03  # Replace with your observed error rate
    confidence = 0.95  # Replace with your desired confidence interval
    margin_of_error = 0.01
    n = calculate_sample_size(observed_error_rate, confidence, margin_of_error)
    print(n)
    probabilities = [
        0,
        0.03,
        0.06,
        0.14,
        0,
        0,
        0.06,
        0.02,
        0,
        0,
        0.02,
        0.07,
        0.08,
        0,
        0.02,
        0.03,
        0.05,
        0,
        0.22,
        0.03,
        0,
        0,
        0.16,
    ]
    cell_references, sheet_references, workbook = create_sheet_cell_references(
        file_path
    )
    (
        sampled_coordinates,
        sampled_cell_references,
        sampled_sheet_references,
    ) = sample_cells_with_probabilities(
        cell_references, sheet_references, n, probabilities
    )
    highlight_cells_workbook(
        workbook, sampled_cell_references, sampled_sheet_references
    )
    workbook.save(file_path)
