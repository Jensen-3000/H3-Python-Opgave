Forsøgt med at få ChatGPT til at lave et python api med en csv som "database".


## How-2-Run:
Udpak games.rar
Opret evt. et virtuelt miljø og skriv commandoen under cmd.


## Links

Dataset:
https://www.kaggle.com/datasets/fronkongames/steam-games-dataset/data
-- Note: Der er fejl i datasættet, som de også skriver i deres discussions. Opdagede det bare for sent.

Http:
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc



## Cmds -- One Liners er meget street

.venv\Scripts\activate; pip install -r requirements.txt; py main.py



## Kun prompts og kode nede under
<details> <summary><strong>Prompt 1</strong></summary>

Can you help me setup a api, using fastapi and panda in python, that can do crud on a .csv file?
The api should support pagination, filtering and sorting.
If a lib can be used to make it easier, then do so.

This is a sample of the csv:
AppID,Name,Release date,Estimated owners,Peak CCU,Required age,Price,DiscountDLC count,About the game,Supported languages,Full audio languages,Reviews,Header image,Website,Support url,Support email,Windows,Mac,Linux,Metacritic score,Metacritic url,User score,Positive,Negative,Score rank,Achievements,Recommendations,Notes,Average playtime forever,Average playtime two weeks,Median playtime forever,Median playtime two weeks,Developers,Publishers,Categories,Genres,Tags,Screenshots,Movies
20200,"Galactic Bowling","Oct 21, 2008","0 - 20000",0,0,19.99,0,0,"Galactic Bowling is an exaggerated and stylized bowling game with an intergalactic twist. Players will engage in fast-paced single and multi-player competition while being submerged in a unique new universe filled with over-the-top humor, wild characters, unique levels, and addictive game play. The title is aimed at players of all ages and skill sets. Through accessible and intuitive controls and game-play, Galactic Bowling allows you to jump right into the action. A single-player campaign and online play allow you to work your way up the ranks of the Galactic Bowling League! Whether you have hours to play or only a few minutes, Galactic Bowling is a fast paced and entertaining experience that will leave you wanting more! Full Single-player story campaign including 11 Characters and Environments. 2 Single-player play modes including Regular and Battle Modes. Head to Head Online Multiplayer play Modes. Super Powers, Special Balls, and Whammies. Unlockable Characters, Environments, and Minigames. Unlock all 30 Steam Achievements!","['English']","[]","","https://cdn.akamai.steamstatic.com/steam/apps/20200/header.jpg?t=1640121033","http://www.galacticbowling.net","","",True,False,False,0,"",0,6,11,"",30,0,"",0,0,0,0,"Perpetual FX Creative","Perpetual FX Creative","Single-player,Multi-player,Steam Achievements,Partial Controller Support","Casual,Indie,Sports","Indie,Casual,Sports,Bowling","https://cdn.akamai.steamstatic.com/steam/apps/20200/0000005994.1920x1080.jpg?t=1640121033,https://cdn.akamai.steamstatic.com/steam/apps/20200/0000005993.1920x1080.jpg?t=1640121033,https://cdn.akamai.steamstatic.com/steam/apps/20200/0000005992.1920x1080.jpg?t=1640121033,https://cdn.akamai.steamstatic.com/steam/apps/20200/0000006011.1920x1080.jpg?t=1640121033,https://cdn.akamai.steamstatic.com/steam/apps/20200/0000005685.1920x1080.jpg?t=1640121033,https://cdn.akamai.steamstatic.com/steam/apps/20200/0000005686.1920x1080.jpg?t=1640121033,https://cdn.akamai.steamstatic.com/steam/apps/20200/0000005995.1920x1080.jpg?t=1640121033,https://cdn.akamai.steamstatic.com/steam/apps/20200/0000005688.1920x1080.jpg?t=1640121033,https://cdn.akamai.steamstatic.com/steam/apps/20200/0000005689.1920x1080.jpg?t=1640121033,https://cdn.akamai.steamstatic.com/steam/apps/20200/0000005690.1920x1080.jpg?t=1640121033","http://cdn.akamai.steamstatic.com/steam/apps/256863704/movie_max.mp4?t=1638854607"

Theres much more data, this is just a sample.

ChatGPT said:
ChatGPT
Memory updated
To set up a FastAPI application that performs CRUD operations on a CSV file using pandas, you can follow these steps. This API will support pagination, filtering, and sorting.

1. Install Required Libraries
Make sure you have fastapi, uvicorn, and pandas installed. You can install them using pip:

bash
Copy code
pip install fastapi uvicorn pandas
2. Create the FastAPI Application
Here's a sample implementation for your FastAPI application:

python
Copy code
from fastapi import FastAPI, HTTPException, Query
import pandas as pd
from typing import List, Optional

app = FastAPI()

# Load the CSV file into a DataFrame
data_file = 'path_to_your_file.csv'  # Update with your CSV file path
df = pd.read_csv(data_file)

@app.get("/games/", response_model=List[dict])
async def get_games(
    page: int = 1,
    page_size: int = 10,
    sort_by: Optional[str] = None,
    filter_by: Optional[str] = None,
    filter_value: Optional[str] = None,
):
    # Filter data if filter_by and filter_value are provided
    if filter_by and filter_value:
        filtered_df = df[df[filter_by].str.contains(filter_value, case=False, na=False)]
    else:
        filtered_df = df

    # Sort data if sort_by is provided
    if sort_by and sort_by in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by=sort_by)

    # Pagination
    start = (page - 1) * page_size
    end = start + page_size
    paginated_df = filtered_df.iloc[start:end]

    # Convert DataFrame to a list of dictionaries
    return paginated_df.to_dict(orient='records')

@app.get("/games/{game_id}", response_model=dict)
async def get_game(game_id: int):
    game = df[df['AppID'] == game_id]
    if game.empty:
        raise HTTPException(status_code=404, detail="Game not found")
    return game.iloc[0].to_dict()

@app.post("/games/", response_model=dict)
async def create_game(game: dict):
    global df
    new_game = pd.DataFrame([game])
    df = pd.concat([df, new_game], ignore_index=True)
    df.to_csv(data_file, index=False)
    return game

@app.put("/games/{game_id}", response_model=dict)
async def update_game(game_id: int, updated_game: dict):
    global df
    index = df.index[df['AppID'] == game_id].tolist()
    if not index:
        raise HTTPException(status_code=404, detail="Game not found")
    
    df.loc[index[0]] = updated_game
    df.to_csv(data_file, index=False)
    return updated_game

@app.delete("/games/{game_id}", response_model=dict)
async def delete_game(game_id: int):
    global df
    index = df.index[df['AppID'] == game_id].tolist()
    if not index:
        raise HTTPException(status_code=404, detail="Game not found")
    
    deleted_game = df.loc[index[0]]
    df = df.drop(index[0]).reset_index(drop=True)
    df.to_csv(data_file, index=False)
    return deleted_game.to_dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
Explanation
Data Loading: The CSV file is loaded into a pandas DataFrame when the application starts.
CRUD Operations:
GET /games/: Retrieve games with pagination, sorting, and filtering.
GET /games/{game_id}: Retrieve a specific game by its AppID.
POST /games/: Create a new game entry.
PUT /games/{game_id}: Update an existing game entry by its AppID.
DELETE /games/{game_id}: Delete a game entry by its AppID.
Pagination: You can control the page size and which page of data to return.
Filtering: You can filter games based on any specified column and value.
Sorting: You can sort the games based on any specified column.
3. Run the Application
Save the code in a file, for example, app.py, and run the FastAPI application with:

bash
Copy code
uvicorn app:app --reload
You can now access the API at http://127.0.0.1:8000/games/. You can also view the automatically generated API documentation at http://127.0.0.1:8000/docs.

4. Example API Requests
Get Games:

GET /games/?page=1&page_size=10&sort_by=Name&filter_by=Genres&filter_value=Indie
Create Game:

POST /games/ with a JSON body containing game details.
Update Game:

PUT /games/{game_id} with a JSON body containing updated game details.
Delete Game:

DELETE /games/{game_id}
This setup should give you a solid starting point for managing your CSV data with an API. Let me know if you need any modifications or additional features!

</details>



<details> <summary><strong>Prompt 2</strong></summary>

Can you put some doc strings on this, to explain the code?
And maybe a comment where it could be hard to know what its doing.


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
    if filter_by and filter_value:
        filtered_df = df[
            df[filter_by].astype(str).str.contains(filter_value, case=False, na=False)
        ]
    else:
        filtered_df = df

    if sort_by and sort_by in filtered_df.columns:
        filtered_df = filtered_df.sort_values(by=sort_by)

    start = (page - 1) * page_size
    end = start + page_size
    paginated_df = filtered_df.iloc[start:end]

    return paginated_df.to_dict(orient="records")


@app.get("/games/{game_id}", response_model=dict)
async def get_game(game_id: int):
    game = df[df["AppID"] == game_id]
    if game.empty:
        raise HTTPException(status_code=404, detail="Game not found")
    return game.iloc[0].to_dict()


@app.post("/games/", response_model=dict)
async def create_game(game: dict):
    global df
    new_game = pd.DataFrame([game])
    df = pd.concat([df, new_game], ignore_index=True)
    df.to_csv(data_file, index=False)
    return game


@app.put("/games/{game_id}", response_model=dict)
async def update_game(game_id: int, updated_game: dict):
    global df
    game_index = df[df["AppID"] == game_id].index
    if game_index.empty:
        raise HTTPException(status_code=404, detail="Game not found")

    df.loc[game_index[0]] = updated_game
    df.to_csv(data_file, index=False)
    return updated_game


@app.delete("/games/{game_id}", response_model=dict)
async def delete_game(game_id: int):
    global df
    game_index = df[df["AppID"] == game_id].index
    if game_index.empty:
        raise HTTPException(status_code=404, detail="Game not found")

    deleted_game = df.loc[game_index[0]].to_dict()
    df = df.drop(game_index[0]).reset_index(drop=True)
    df.to_csv(data_file, index=False)
    return deleted_game


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
ChatGPT said:
ChatGPT
Here's the code with docstrings and comments added to clarify its functionality:

python
Copy code
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
Key Explanations:
get_games(): Filters, sorts, and paginates games. The .str.contains() method is used to make filtering case-insensitive.
create_game(): Adds a new row to the CSV, saving the file each time.
update_game() and delete_game(): Locate game by AppID, update/delete it, and save changes.

</details>