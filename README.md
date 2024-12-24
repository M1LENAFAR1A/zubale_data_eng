# Code Explanation - Data Processing Project

## 1. Purpose of the Code
The goal of this project is to efficiently process and analyze **product and order data** using **Python and SQL**. It is divided into three main parts:
- **Challenge_1.py:** Merges and consolidates data from `products.csv` and `orders.csv`.
- **Challenge_2.py:** Converts prices from **BRL** to **USD** using an **API**.
- **Challenge_3.ipynb:** Executes **SQL queries** to extract strategic insights.

---

## 2. Use of `config.json` for API Key Management
The **API key** was stored in `config.json` to avoid hardcoding sensitive information into the scripts.

**Example structure:**
```json
{
    "api_key": "YOUR_API_KEY"
}
```

**Placement:** Ensure that `config.json` is placed in the **root directory** of the project. If the file is not in the root directory, the code will not function correctly.

**Reasoning:**
- Centralizes sensitive information.
- Simplifies updates to the **API key**.

**Note:** The `config.json` file will be included as an attachment in the email. Make sure to add it to the **root directory** of your project.

---

## 3. Security: `.gitignore`
The `config.json` file was added to `.gitignore` to prevent the **API key** from being exposed in version control.

---

## 4. Results Saved in `results/` Folder
- `order_full_information.csv`: Raw merged data from **products** and **orders**.
- `fixed_order_full_information.csv`: Data with **currency converted to USD**.
- `kpi_product_orders.csv`: Key **performance indicators** from **SQL analysis**.

**Reasoning:**
- Separating **raw** and **processed data** makes it easier to track the data processing workflow.
- Clear **naming conventions** ensure clarity for future updates or debugging.

---

## 5. SQL Queries in Jupyter Notebook (`Challenge_3.ipynb`)
SQL queries were executed in **Jupyter Notebooks** for better organization. Each query is accompanied by **text explanations** and query results are displayed **inline**.

---

## 6. Quick Summary of Decisions
- **Base CSVs in `data/`:** Keeps source data organized and easy to locate.
- **Separate scripts for each challenge:** Ensures modularity.
- **API key in `config.json`:** Enhances security and flexibility.
- **Use of `.gitignore`:** Prevents accidental exposure of sensitive data.
- **Organized results in `results/`:** Maintains clarity.
- **SQL in Jupyter Notebook:** Improves documentation and visualization.
- **`config.json` in root directory:** Ensures compatibility across environments and proper code execution.

---

## 7. Code Purpose and Design Decisions Documentation

### 7.1 Libraries Used and Reasons
- **Pandas:**
   - **Why:** Pandas is the standard library for **data reading and manipulation** in Python.
   - **Usage:** Reading and writing **CSV files**, data merging, and aggregations.
- **Requests:**
   - **Why:** Facilitates **API communication**.
   - **Usage:** Fetching **real-time exchange rates** from an external API.

### 7.2 Key Technical Decisions
- **Separate Scripts for Each Challenge:**
   - Each challenge was implemented in a **separate file** for better clarity and easier debugging.
- **Folder Structure:**
   - `data/`: Stores base **CSV files**.
   - `results/`: Stores processed **output files**.
- **Use of `merge` (`Challenge_1.py`):**
   - `left_on` and `right_on`: The `pd.merge` method was used to match the `product_id` column in orders with the `id` column in products. This ensures each order is paired with its corresponding product details.
- **Use of `try-except` (`Challenge_2.py`):**
   - Used to **handle errors** when calling the API for currency conversion.
   - Ensures that if the API fails or the response is incorrect, the program can gracefully fall back to a **default exchange rate**.

---

