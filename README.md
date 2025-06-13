# Financial Waterfall Calculation Engine

This project provides a Python-based engine for calculating financial distributions according to a standard multi-tier waterfall model. It's designed to process commitment and transaction data for Limited Partners (LPs) and determine how proceeds are allocated between LPs and the General Partner (GP).

## Table of Contents
- [How the Waterfall Calculation Works](#how-the-waterfall-calculation-works)
- [Data Format](#data-format)
- [Running the Application](#running-the-application)
- [Testing the Engine](#testing-the-engine)
- [Potential Enhancements (Future Works)](#potential-enhancements-future-works)
- [Contributing](#contributing)
- [License](#license)

Key Features:
*   Processes CSV data for commitments and transactions.
*   Implements a 4-tier waterfall: Return of Capital, Preferred Return, Catch-up, and Final Split.
*   Outputs a tabulated summary of the distribution for a specified LP.
*   Includes example data and unit tests.
*   GitHub repository: https://github.com/i5m/waterfall

## How the Waterfall Calculation Works

A financial waterfall is a method used to distribute profits or proceeds among participants in an investment, where funds flow downwards through a series of predetermined tiers. Each tier must be satisfied before funds can flow to the next. This engine implements a common four-tier model:

1.  **Return of Capital (ROC):**
    *   The first priority is to return the initial capital contributed by the Limited Partners (LPs).
    *   100% of the distributions go to the LPs until their total contributed capital is paid back.

2.  **Preferred Return (Pref):**
    *   Once capital is returned, LPs receive a preferred rate of return on their investment.
    *   This is typically an annual percentage, and this engine calculates it based on the timing of contributions and the last distribution date.
    *   100% of further distributions go to the LPs until this preferred return is met.

3.  **Catch-up:**
    *   After the LPs receive their preferred return, there's often a "catch-up" phase for the General Partner (GP).
    *   The GP receives a high percentage (e.g., 80-100%) of the distributions until they have received a certain percentage (e.g., 20%) of the profits distributed in the Preferred Return and Catch-up tiers combined. This engine uses a configurable catch-up percentage and carried interest for this calculation.

4.  **Final Split (Carried Interest):**
    *   Once the catch-up tier is complete, remaining proceeds are split between LPs and the GP according to a predetermined ratio (e.g., 80% to LPs, 20% to GP). The GP's portion is often referred to as "carried interest."

## Data Format

The engine expects input data in CSV format, specifically in two files: `commitments.csv` and `transactions.csv`. These files should be placed in a `data/` directory relative to `main.py`. For an example of how to use your own data, you can replace the example files in `data/` with your own, following the formats below.

### `commitments.csv`

This file contains information about each Limited Partner (LP) and their total commitment.

| Column             | Type   | Description                                  | Example     |
|--------------------|--------|----------------------------------------------|-------------|
| `id`               | Integer| Unique identifier for the LP commitment.     | `1`         |
| `entity_name`      | String | The name of the Limited Partner entity.      | `LP Alpha`  |
| `commitment_amount`| String | Total amount committed by the LP (e.g., "$1,000,000.00"). Can include currency symbols and commas. | `$500,000`  |

*Example `data/commitments.csv`:*
```csv
id,entity_name,commitment_amount
1,"LP Alpha","$1,000,000.00"
2,"LP Beta","$2,500,000.00"
```

### `transactions.csv`

This file contains all capital calls (contributions) and distributions for each commitment.

| Column                        | Type   | Description                                                                 | Example        |
|-------------------------------|--------|-----------------------------------------------------------------------------|----------------|
| `commitment_id`               | Integer| Identifier linking to the `id` in `commitments.csv`.                        | `1`            |
| `transaction_date`            | String | Date of the transaction in `MM/DD/YYYY` format.                             | `01/15/2023`   |
| `transaction_amount`          | String | Amount of the transaction (e.g., "$50,000.00"). Can include currency symbols and commas. | `$25,000.00`   |
| `contribution_or_distribution`| String | Type of transaction. Must be either `"contribution"` or `"distribution"`.     | `contribution` |

*Example `data/transactions.csv`:*
```csv
commitment_id,transaction_date,transaction_amount,contribution_or_distribution
1,01/15/2023,"$50,000.00",contribution
1,06/20/2023,"$100,000.00",contribution
1,12/01/2024,"$30,000.00",distribution
```

**Note:** The currency cleaning function (`utils.funcs.clean_currency`) is designed to handle strings with '$', ',', '(', and ')' characters. Ensure your numeric values in `commitment_amount` and `transaction_amount` are compatible.

## Running the Application

### 1. Install Dependencies

Ensure you have Python 3 installed. Then, install the necessary modules:
```bash
pip3 install pandas tabulate
```

### 2. Prepare Your Data (Optional)

If you want to use your own data:
*   Create a `data/` directory in the same location as `main.py`.
*   Inside `data/`, place your `commitments.csv` and `transactions.csv` files, following the structure described in the "Data Format" section.

Clarification on data usage:
*   Running `python3 main.py` will attempt to load `data/commitments.csv` and `data/transactions.csv`.
*   Running `python3 main.py --example` will load `data/test_commitments.csv` and `data/test_transactions.csv`.

### 3. Execute the Program

Run the program from your terminal:
```bash
python3 main.py
```
Or, to run with the example dataset:
```bash
python3 main.py --example
```

The program will prompt you to "Enter Commitment ID:". Provide the ID of the LP for whom you want to calculate the waterfall (this ID should exist in your `commitments.csv` or `test_commitments.csv`).

### 4. Understanding the Output

After processing, the program will display:
*   The LP's name and total commitment amount.
*   A summary of their contributions.
*   A summary of their distributions, including the total amount and the date of the last distribution.
*   A detailed table showing the waterfall calculation. This table breaks down how the total distributed amount is allocated across the four tiers:
    *   **Return on Capital:** Shows how much of the distribution goes to returning the LP's contributed capital.
    *   **Preferred Return:** Shows the portion allocated to the LP's preferred return.
    *   **Catch Up:** Shows the portion allocated to the GP during the catch-up phase.
    *   **Final Split:** Shows how the remaining amount is split between the LP and GP.

Each row in the table corresponds to one of these tiers, detailing the starting capital for that tier, allocations to LP and GP, the total distribution for that tier, and the remaining capital passed to the next tier.

## Testing the Engine

This project includes a suite of unit tests to verify the functionality of individual components, particularly the calculation logic in `utils/funcs.py` and data models in `utils/models.py`.

To run the unit tests, execute the following command in your terminal:
```bash
python3 unit_tests.py
```
This will run all defined unit tests and report any failures.

For testing the end-to-end application flow with predefined example data, please refer to the "Running the Application" section on using the `--example` flag.

## Potential Enhancements (Future Works)

The current engine provides a solid foundation for waterfall calculations. Future development could explore the following areas:

*   **Handling Multiple Distributions:**
    *   Extend the logic to manage scenarios with multiple distribution dates over the lifetime of a fund. This would involve tracking changes in capital accounts and tier satisfaction over time.

*   **Support for Multiple Funds/Enterprises:**
    *   Develop the infrastructure to support data from various funds or enterprises, potentially with customizable configurations or data mapping for each.

*   **User Interface (UI):**
    *   Create a graphical user interface (GUI) or web interface to allow users to upload data, configure parameters, run calculations, and visualize results more interactively.

*   **Advanced Reporting:**
    *   Implement more detailed and customizable reporting options, such as exporting results to different formats (e.g., Excel, PDF) or generating visual charts.

*   **Configuration Flexibility:**
    *   Allow for more dynamic configuration of waterfall tiers and rules, perhaps through a separate configuration file or UI settings, to accommodate different fund agreements.

## Contributing

Contributions to enhance the Waterfall Engine are welcome! If you have suggestions for improvements or new features, please feel free to:

1.  **Fork the repository.**
2.  **Create a new branch** for your changes (`git checkout -b feature/your-feature-name`).
3.  **Make your modifications.**
4.  **Add or update tests** as appropriate.
5.  **Ensure your changes pass all tests.**
6.  **Commit your changes** (`git commit -am 'Add some feature'`).
7.  **Push to the branch** (`git push origin feature/your-feature-name`).
8.  **Create a new Pull Request.**

Please provide a clear description of your changes in the pull request. If you're addressing an existing issue, please reference it.

## License

This project is currently not licensed.

It is recommended to choose an open-source license to clarify how others can use, modify, and distribute the code. The [MIT License](https://opensource.org/licenses/MIT) is a popular choice for its simplicity and permissiveness.

To add a license:
1.  Choose a license (e.g., MIT).
2.  Create a file named `LICENSE` or `LICENSE.md` in the root of the project.
3.  Copy the full text of your chosen license into this file.
4.  You can then update this section to refer to the chosen license, e.g., "This project is licensed under the MIT License - see the LICENSE.md file for details."

