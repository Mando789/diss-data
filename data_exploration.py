import pm4py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class BPIDataExplorer:
    def __init__(self, data_dir="data/bpi_challenge_2020"):
        self.data_dir = Path(data_dir)
        self.datasets = {}
        
    def load_xes_files(self):
        """Load all XES files from BPI Challenge 2020"""
        
        xes_files = {
            "travel_permits": "PermitLog.xes",
            "domestic_declarations": "DomesticDeclarations.xes", 
            "international_declarations": "InternationalDeclarations.xes",
            "prepaid_travel": "PrepaidTravelCost.xes",
            "request_for_payment": "RequestForPayment.xes"
        }
        
        for name, filename in xes_files.items():
            filepath = self.data_dir / filename
            if filepath.exists():
                print(f"Loading {name}...")
                try:
                    log = pm4py.read_xes(str(filepath))
                    self.datasets[name] = log
                    print(f"✅ Loaded {name}: {len(log)} cases")
                except Exception as e:
                    print(f"❌ Error loading {name}: {e}")
            else:
                print(f"⚠️  File not found: {filepath}")
        
        return self.datasets
    
    def analyze_dataset_structure(self, dataset_name):
        """Analyze structure of a specific dataset"""
        
        if dataset_name not in self.datasets:
            print(f"Dataset {dataset_name} not loaded")
            return
        
        log = self.datasets[dataset_name]
        
        print(f"\n=== Analysis of {dataset_name.upper()} ===")
        print(f"Number of cases: {len(log)}")
        
        # Convert to DataFrame for easier analysis
        df = pm4py.convert_to_dataframe(log)
        
        print(f"Number of events: {len(df)}")
        print(f"Time range: {df['time:timestamp'].min()} to {df['time:timestamp'].max()}")
        
        # Activity analysis
        activities = df['concept:name'].value_counts()
        print(f"\nTop 10 Activities:")
        print(activities.head(10))
        
        # Case duration analysis
        case_durations = []
        for case_id in df['case:concept:name'].unique():
            case_events = df[df['case:concept:name'] == case_id]
            duration = (case_events['time:timestamp'].max() - 
                       case_events['time:timestamp'].min()).total_seconds() / 86400  # days
            case_durations.append(duration)
        
        print(f"\nCase Duration Statistics (days):")
        print(f"Average: {np.mean(case_durations):.1f}")
        print(f"Median: {np.median(case_durations):.1f}")
        print(f"Min: {np.min(case_durations):.1f}")
        print(f"Max: {np.max(case_durations):.1f}")
        
        return df
    
    def identify_bottlenecks(self, dataset_name):
        """Identify potential bottlenecks based on research findings"""
        
        if dataset_name not in self.datasets:
            return
        
        df = pm4py.convert_to_dataframe(self.datasets[dataset_name])
        
        print(f"\n=== BOTTLENECK ANALYSIS: {dataset_name.upper()} ===")
        
        # Look for approval activities (key bottleneck indicators)
        approval_activities = df[df['concept:name'].str.contains('APPROVED|FINAL|SUPERVISOR|DIRECTOR', 
                                                                na=False, case=False)]
        
        if len(approval_activities) > 0:
            print("Approval Activities Found:")
            approval_counts = approval_activities['concept:name'].value_counts()
            print(approval_counts)
            
            # Calculate time between submissions and approvals
            for case_id in df['case:concept:name'].unique()[:5]:  # Sample first 5 cases
                case_events = df[df['case:concept:name'] == case_id].sort_values('time:timestamp')
                
                submitted = case_events[case_events['concept:name'].str.contains('SUBMITTED', 
                                                                               na=False, case=False)]
                approved = case_events[case_events['concept:name'].str.contains('APPROVED', 
                                                                               na=False, case=False)]
                
                if len(submitted) > 0 and len(approved) > 0:
                    approval_time = (approved['time:timestamp'].iloc[0] - 
                                   submitted['time:timestamp'].iloc[0]).total_seconds() / 86400
                    print(f"Case {case_id}: {approval_time:.1f} days from submission to approval")
        
        # Look for rejection patterns
        rejections = df[df['concept:name'].str.contains('REJECT|DECLINED', na=False, case=False)]
        if len(rejections) > 0:
            rejection_rate = len(rejections['case:concept:name'].unique()) / len(df['case:concept:name'].unique())
            print(f"\nRejection Rate: {rejection_rate:.1%}")
    
    def extract_training_features(self, dataset_name):
        """Extract features that will be used for AI training"""
        
        if dataset_name not in self.datasets:
            return None
        
        df = pm4py.convert_to_dataframe(self.datasets[dataset_name])
        
        # Group by case to extract case-level features
        training_data = []
        
        for case_id in df['case:concept:name'].unique():
            case_events = df[df['case:concept:name'] == case_id].sort_values('time:timestamp')
            
            # Extract features
            features = {
                'case_id': case_id,
                'total_duration_days': (case_events['time:timestamp'].max() - 
                                       case_events['time:timestamp'].min()).total_seconds() / 86400,
                'activity_count': len(case_events),
                'unique_activities': len(case_events['concept:name'].unique()),
                'has_rejections': any('REJECT' in str(act) for act in case_events['concept:name']),
                'rejection_count': sum(1 for act in case_events['concept:name'] if 'REJECT' in str(act)),
                'is_international': 'international' in dataset_name.lower(),
                'activities_sequence': list(case_events['concept:name']),
                'timestamps': list(case_events['time:timestamp'])
            }
            
            # Calculate approval times
            submitted_events = case_events[case_events['concept:name'].str.contains('SUBMITTED', na=False, case=False)]
            approved_events = case_events[case_events['concept:name'].str.contains('APPROVED', na=False, case=False)]
            
            if len(submitted_events) > 0 and len(approved_events) > 0:
                features['approval_time_days'] = (approved_events['time:timestamp'].iloc[0] - 
                                                 submitted_events['time:timestamp'].iloc[0]).total_seconds() / 86400
            else:
                features['approval_time_days'] = None
            
            training_data.append(features)
        
        return pd.DataFrame(training_data)

def main():
    """Main execution function"""
    
    print("🚀 Starting BPI Challenge 2020 Data Exploration")
    print("This will analyze your travel approval workflow data for AI training")
    
    explorer = BPIDataExplorer()
    
    # Load datasets
    datasets = explorer.load_xes_files()
    
    if not datasets:
        print("❌ No datasets loaded. Please run the download script first.")
        return
    
    # Analyze each dataset
    for dataset_name in datasets.keys():
        df = explorer.analyze_dataset_structure(dataset_name)
        explorer.identify_bottlenecks(dataset_name)
        
        # Extract training features
        features_df = explorer.extract_training_features(dataset_name)
        if features_df is not None:
            # Save features for later use
            output_file = f"data/processed/{dataset_name}_features.csv"
            Path("data/processed").mkdir(parents=True, exist_ok=True)
            features_df.to_csv(output_file, index=False)
            print(f"💾 Saved features to {output_file}")
    
    print("\n✅ Data exploration complete!")
    print("Next step: Run the labeling script to create training labels")

if __name__ == "__main__":
    main()