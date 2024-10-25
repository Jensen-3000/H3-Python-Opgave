from fastapi import FastAPI, HTTPException
from typing import List, Optional
import pandas as pd
import uvicorn

app = FastAPI()

# Load the CSV file into a DataFrame
data_file = "data/games.csv"
print("Loading data...")
try:
    df = pd.read_csv(data_file, encoding="utf-8", index_col=False)
    print("Data loaded successfully")
except Exception as e:
    print("Error loading CSV:", e)


@app.get("/games/", response_model=List[dict])
async def get_games(
    page: int = 1,
    page_size: int = 10,
    sort_by: Optional[str] = None,
    filter_by: Optional[str] = None,
    filter_value: Optional[str] = None,
):
    """
    Retrieve a paginated list of games with optional sorting and filtering.

    Parameters:
    - page: The page number for pagination.
    - page_size: Number of games per page.
    - sort_by: Optional column name to sort the games.
    - filter_by: Optional column name to filter games.
    - filter_value: Value to filter the specified column by.

    Returns:
    - List of dictionaries, each representing a game.
    """
    # Filter the DataFrame based on the specified column and value
    if filter_by and filter_value:
        filtered_df = df[
            df[filter_by].astype(str).str.contains(filter_value, case=False, na=False)
        ]
    else:
        filtered_df = df

    # Sort the DataFrame if a valid column is specified
    if sort_by and sort_by in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by=sort_by)

    # Calculate start and end indices for pagination
    start = (page - 1) * page_size
    end = start + page_size
    paginated_df = filtered_df.iloc[start:end]

    return paginated_df.to_dict(orient="records")


@app.get("/games/{game_id}", response_model=dict)
async def get_game(game_id: int):
    """
    Retrieve a specific game by its unique ID.

    Parameters:
    - game_id: The unique identifier (AppID) of the game.

    Returns:
    - Dictionary containing game details.

    Raises:
    - HTTPException with 404 status if game is not found.
    """
    game = df[df["AppID"] == game_id]
    if game.empty:
        raise HTTPException(status_code=404, detail="Game not found")
    return game.iloc[0].to_dict()


@app.post("/games/", response_model=dict)
async def create_game(game: dict):
    """
    Add a new game to the dataset.

    Parameters:
    - game: Dictionary containing game data.

    Returns:
    - The newly added game data as a dictionary.
    """
    global df
    # Convert new game data to DataFrame and append it to existing data
    new_game = pd.DataFrame([game])
    df = pd.concat([df, new_game], ignore_index=True)
    df.to_csv(data_file, index=False)
    return game


@app.put("/games/{game_id}", response_model=dict)
async def update_game(game_id: int, updated_game: dict):
    """
    Update details of an existing game.

    Parameters:
    - game_id: The unique identifier (AppID) of the game to update.
    - updated_game: Dictionary containing updated game data.

    Returns:
    - The updated game data as a dictionary.

    Raises:
    - HTTPException with 404 status if game is not found.
    """
    global df
    # Find the index of the game to update
    game_index = df[df["AppID"] == game_id].index
    if game_index.empty:
        raise HTTPException(status_code=404, detail="Game not found")

    # Update the game's data at the found index
    df.loc[game_index[0]] = updated_game
    df.to_csv(data_file, index=False)
    return updated_game


@app.delete("/games/{game_id}", response_model=dict)
async def delete_game(game_id: int):
    """
    Delete a game from the dataset.

    Parameters:
    - game_id: The unique identifier (AppID) of the game to delete.

    Returns:
    - The deleted game data as a dictionary.

    Raises:
    - HTTPException with 404 status if game is not found.
    """
    global df
    # Find the index of the game to delete
    game_index = df[df["AppID"] == game_id].index
    if game_index.empty:
        raise HTTPException(status_code=404, detail="Game not found")

    # Retrieve the game's data before deletion
    deleted_game = df.loc[game_index[0]].to_dict()
    # Drop the game from the DataFrame
    df = df.drop(game_index[0]).reset_index(drop=True)
    df.to_csv(data_file, index=False)
    return deleted_game


if __name__ == "__main__":
    # Start the FastAPI application with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
