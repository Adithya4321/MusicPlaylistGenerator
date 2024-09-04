import pandas as pd

# Load the original dataset
df = pd.read_csv('DataSet_Music/tcc_ceds_music.csv')

# Extract only the specified columns
selected_columns = ['artist_name', 'track_name', 'release_date', 'genre', 'lyrics']
df_selected = df[selected_columns]

# Check for any null values in the selected columns
null_values = df_selected.isnull().sum()
print("Null values in selected columns:")
print(null_values)

# Save the selected columns to a new CSV file
df_selected.to_csv('DataSet_Music/selected_music_data.csv', index=False)
print("Selected columns have been saved to 'selected_music_data.csv'.")
