# Fantasy Premier League - Best Player Predictor

This is a **Fantasy Premier League (FPL) Best Player Predictor** web app built using **Streamlit**. The app allows users to filter and select FPL players based on various factors such as position, team, price range, and predicted performance.

## Features
- Select players based on position, team, and price range.
- Predict upcoming event points using a trained **PyCaret regression model**.
- Enforce FPL constraints (**2 Goalkeepers, 5 Defenders, 5 Midfielders, 3 Forwards**).
- Display selected players in a separate tab.
- Reset selections when needed.

## Installation & Setup

### 1. Clone the Repository
```sh
git clone https://github.com/bhumilad/FPL.git
or
Download manually
```

### 2. Create Virtual Environment
```sh
python -m venv env
```

### 3. Activate Virtual Environment
#### Windows:
```sh
env\Scripts\activate
```
#### Mac/Linux:
```sh
source env/bin/activate
```


### 5. Download Model & Data
- Ensure that the trained **PyCaret model** (`fpl_points_predictor3`) is available in the project folder.
- Ensure that the **dataset** (`final_fpl_data.csv`) is also available in the project folder.

## How to Run
```sh
streamlit run fpl.py
```

## File Structure
```
FPL-Streamlit-App/
│── fpl.py                 # Main Streamlit app
│── final_fpl_data.csv     # Dataset
│── fpl_points_predictor3  # Trained PyCaret model
│── README.md              # Project documentation
```

## Technologies Used
- **Python**
- **Streamlit** (for web UI)
- **Pandas** (for data manipulation)
- **PyCaret** (for machine learning predictions)
- **GitHub** (for version control)

## Future Improvements
- Enhance UI with better visualization.
- Improve model performance with advanced feature engineering.
- Integrate real-time FPL data.

## License
This project is open-source and available under the MIT License.

