import pandas as pd


def preprocess_data(filename="hashtag_data.csv"):
    df = pd.read_csv(filename, names=["timestamp", "hashtag", "post_count"])

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Extract time components
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day
    df['weekday'] = df['timestamp'].dt.weekday

    return df


if __name__ == "__main__":
    df = preprocess_data()
    print(df.head())
