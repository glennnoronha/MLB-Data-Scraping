import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from typing import Dict, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLBStatsAnalyzer:
    def __init__(self, csv_path: str, min_plate_appearances: int = 502):
        """
        Initialize the MLB Stats Analyzer.
        
        Args:
            csv_path: Path to the CSV file containing hitting stats
            min_plate_appearances: Minimum plate appearances to qualify
        """
        self.csv_path = csv_path
        self.min_pa = min_plate_appearances
        self.weights = {
            'BA': 0.15,   
            'HR': 0.25,    
            'RBI': 0.20,  
            'OBP': 0.15,   
            'SLG': 0.15,   
            'SB': 0.15,    
        }
        self.selected_columns = [
            'Player', 'WeightedTotal', 'BA', 'HR', 'RBI', 
            'OBP', 'SLG', 'OPS', 'SB', 'TB', 'R'
        ]
        self.data = None
        self.data_sorted = None

    def load_data(self) -> None:
        """Load and validate the CSV data."""
        try:
            self.data = pd.read_csv(self.csv_path)
            logger.info(f"Successfully loaded data from {self.csv_path}")
        except FileNotFoundError:
            logger.error(f"Could not find file: {self.csv_path}")
            raise
        except pd.errors.EmptyDataError:
            logger.error(f"The file {self.csv_path} is empty")
            raise
        
        # Validate required columns
        required_columns = set(self.weights.keys()) | {'PA'}
        missing_columns = required_columns - set(self.data.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

    def process_data(self) -> None:
        """Process the MLB stats data."""
        # Filter qualified players
        self.data = self.data[self.data['PA'] >= self.min_pa]
        logger.info(f"Filtered to {len(self.data)} qualified players")

        # Calculate weighted total
        self.data['WeightedTotal'] = sum(
            self.data[stat] * weight 
            for stat, weight in self.weights.items()
        )

        # Sort by weighted total
        self.data_sorted = self.data.sort_values(
            by='WeightedTotal', 
            ascending=False
        )

    def save_top_players(self, output_path: str, num_players: int = 25) -> None:
        """Save top players to CSV file."""
        try:
            self.data_sorted[self.selected_columns].head(num_players).to_csv(
                output_path, 
                index=False
            )
            logger.info(f"Saved top {num_players} players to {output_path}")
        except Exception as e:
            logger.error(f"Error saving to {output_path}: {str(e)}")
            raise

    def plot_correlation_matrix(self) -> None:
        """Plot correlation matrix heatmap."""
        numeric_columns = [
            'WeightedTotal', 'BA', 'HR', 'RBI', 'OBP', 
            'SLG', 'OPS', 'SB', 'TB', 'R'
        ]
        correlation_matrix = self.data_sorted[numeric_columns].corr()

        plt.figure(figsize=(12, 8))
        sns.heatmap(
            correlation_matrix,
            annot=True,
            cmap='coolwarm',
            fmt='.2f',
            square=True
        )
        plt.title('Correlation Matrix of Offensive Stats')
        plt.tight_layout()
        plt.show()

    def plot_top_players(self, num_players: int = 15) -> None:
        """Plot top players bar chart."""
        fig = px.bar(
            self.data_sorted.head(num_players),
            x='Player',
            y='WeightedTotal',
            title=f'Top {num_players} Players by Weighted Total',
            labels={'WeightedTotal': 'Weighted Total Score'},
            template='plotly_white'
        )
        
        # Customize the layout
        fig.update_layout(
            xaxis_tickangle=-45,
            showlegend=False,
            height=600,
            margin=dict(b=100)  # Increase bottom margin for rotated labels
        )
        
        fig.show()

def main():
    """Main execution function."""
    try:
        # Initialize analyzer
        analyzer = MLBStatsAnalyzer('hitting_stats.csv')
        
        # Load and process data
        analyzer.load_data()
        analyzer.process_data()
        
        # Save top players
        analyzer.save_top_players('top_players.csv')
        
        # Create visualizations
        analyzer.plot_correlation_matrix()
        analyzer.plot_top_players()
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()