import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime, timedelta

class ResearchBasedLabeler:
    """
    Labels workflow data based on published research findings from BPI Challenge 2020
    
    Research findings used for labeling:
    - Domestic declarations: 8-11 days average, 95.62% success rate
    - International declarations: 66-86 days average, 95.94% success rate  
    - Supervisor approval bottleneck: 39 days average (45.3% of process time)
    - Director approval bottleneck: 55 days average (63.9% of process time)
    - Rejection rates: 12% domestic, 27% international
    """
    
    def __init__(self):
        # Research-validated thresholds from BPI Challenge 2020 papers
        self.thresholds = {
            'domestic_normal_duration': 11,      # Research: 8-11 days normal
            'domestic_excessive_duration': 20,   # 80% above normal
            'international_normal_duration': 86, # Research: 66-86 days normal  
            'international_excessive_duration': 150, # 75% above normal
            'supervisor_approval_bottleneck': 30,    # Research: 39 days average
            'director_approval_bottleneck': 45,      # Research: 55 days average
            'excessive_rejections': 2,               # Research: >2 rejections = inefficient
            'budget_variance_threshold': 0.3,        # >30% variance = poor planning
            'late_submission_days': 60               # >2 months after trip
        }
        
        # Framework mappings for inefficiencies
        self.framework_mappings = {
            'supervisor_approval_bottleneck': {
                'lean_waste': 'waiting',
                'agile_principle': 'working_software_over_documentation',
                'optimization': 'increase_supervisors_or_delegation'
            },
            'director_approval_bottleneck': {
                'lean_waste': 'waiting',
                'agile_principle': 'responding_to_change',
                'optimization': 'implement_escalation_rules'
            },
            'excessive_rejections': {
                'lean_waste': 'defects',
                'agile_principle': 'working_software_over_documentation',
                'optimization': 'implement_pre_validation_checks'
            },
            'excessive_duration': {
                'lean_waste': 'waiting',
                'agile_principle': 'deliver_working_software_frequently',
                'optimization': 'streamline_approval_process'
            },
            'late_submission': {
                'lean_waste': 'transportation',
                'agile_principle': 'deliver_working_software_frequently', 
                'optimization': 'implement_automated_reminders'
            }
        }
    
    def label_case_inefficiencies(self, case_features):
        """
        Label individual case based on research findings
        
        Args:
            case_features (dict): Case features extracted from process data
            
        Returns:
            dict: Labeled inefficiencies with severity and framework mappings
        """
        
        labels = []
        severity_score = 0
        
        # Duration-based inefficiencies
        duration = case_features.get('total_duration_days', 0)
        is_international = case_features.get('is_international', False)
        
        if is_international:
            if duration > self.thresholds['international_excessive_duration']:
                labels.append({
                    'type': 'excessive_duration_international',
                    'severity': 'high' if duration > 200 else 'medium',
                    'actual_value': duration,
                    'expected_range': '66-86 days',
                    'framework_violation': self.framework_mappings['excessive_duration']
                })
                severity_score += 3 if duration > 200 else 2
        else:
            if duration > self.thresholds['domestic_excessive_duration']:
                labels.append({
                    'type': 'excessive_duration_domestic', 
                    'severity': 'high' if duration > 30 else 'medium',
                    'actual_value': duration,
                    'expected_range': '8-11 days',
                    'framework_violation': self.framework_mappings['excessive_duration']
                })
                severity_score += 3 if duration > 30 else 2
        
        # Approval bottlenecks (from research: 45.3% and 63.9% of process time)
        approval_time = case_features.get('approval_time_days')
        if approval_time:
            if approval_time > self.thresholds['supervisor_approval_bottleneck']:
                labels.append({
                    'type': 'supervisor_approval_bottleneck',
                    'severity': 'high' if approval_time > 50 else 'medium',
                    'actual_value': approval_time,
                    'expected_value': '3-5 days',
                    'research_finding': '39 days average (45.3% of total process time)',
                    'framework_violation': self.framework_mappings['supervisor_approval_bottleneck']
                })
                severity_score += 3
        
        # Rejection inefficiencies (from research: 27% international, 12% domestic rejection rate)
        rejection_count = case_features.get('rejection_count', 0)
        if rejection_count > self.thresholds['excessive_rejections']:
            expected_rejection_rate = 0.27 if is_international else 0.12
            labels.append({
                'type': 'excessive_rejections',
                'severity': 'high' if rejection_count > 3 else 'medium',
                'actual_value': rejection_count,
                'expected_rate': f'{expected_rejection_rate:.0%}',
                'research_finding': f'Normal rejection rate: {expected_rejection_rate:.0%}',
                'framework_violation': self.framework_mappings['excessive_rejections']
            })
            severity_score += 2
        
        # Activity complexity (too many activities = process bloat)
        activity_count = case_features.get('activity_count', 0)
        if activity_count > 20:  # Threshold based on typical approval workflows
            labels.append({
                'type': 'process_complexity',
                'severity': 'medium',
                'actual_value': activity_count,
                'expected_range': '8-15 activities',
                'framework_violation': {
                    'lean_waste': 'overprocessing',
                    'agile_principle': 'simplicity',
                    'optimization': 'consolidate_approval_steps'
                }
            })
            severity_score += 1
        
        return {
            'inefficiencies': labels,
            'severity_score': severity_score,
            'total_inefficiency_count': len(labels),
            'optimization_potential': self._calculate_optimization_potential(labels, case_features)
        }
    
    def _calculate_optimization_potential(self, inefficiencies, case_features):
        """Calculate potential improvement percentage"""
        
        if not inefficiencies:
            return 0
        
        # Research-based improvement potentials
        improvement_potential = 0
        
        for inefficiency in inefficiencies:
            if inefficiency['type'] == 'supervisor_approval_bottleneck':
                improvement_potential += 45.3  # Research: 45.3% of process time
            elif inefficiency['type'] == 'excessive_duration_international':
                improvement_potential += 30    # Conservative 30% reduction potential
            elif inefficiency['type'] == 'excessive_duration_domestic':
                improvement_potential += 50    # Higher potential for domestic
            elif inefficiency['type'] == 'excessive_rejections':
                improvement_potential += 20    # Avoid rework cycles
            elif inefficiency['type'] == 'process_complexity':
                improvement_potential += 15    # Streamline activities
        
        return min(improvement_potential, 80)  # Cap at 80% improvement
    
    def generate_optimization_recommendations(self, inefficiencies):
        """Generate specific optimization recommendations"""
        
        recommendations = []
        
        for inefficiency in inefficiencies:
            inefficiency_type = inefficiency['type']
            framework_info = inefficiency.get('framework_violation', {})
            
            recommendation = {
                'inefficiency_type': inefficiency_type,
                'recommendation': self._get_recommendation(inefficiency_type),
                'expected_improvement': self._get_expected_improvement(inefficiency_type),
                'framework_basis': framework_info.get('optimization', 'general_process_improvement'),
                'lean_principle': framework_info.get('lean_waste', 'unknown'),
                'agile_principle': framework_info.get('agile_principle', 'unknown')
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _get_recommendation(self, inefficiency_type):
        """Get specific recommendation for inefficiency type"""
        
        recommendations = {
            'supervisor_approval_bottleneck': 'Increase number of supervisors or implement delegation rules. Consider automated pre-approval for low-value requests.',
            'director_approval_bottleneck': 'Implement escalation rules. Director approval should only be required for high-value or high-risk requests.',
            'excessive_rejections': 'Implement pre-validation checks and automated compliance screening before submission.',
            'excessive_duration_international': 'Streamline international approval process. Consider regional approval authorities.',
            'excessive_duration_domestic': 'Implement automated approval for standard domestic travel below threshold amounts.',
            'process_complexity': 'Consolidate approval steps. Remove redundant activities and parallel process where possible.',
            'late_submission': 'Implement automated reminder system and mobile expense reporting capabilities.'
        }
        
        return recommendations.get(inefficiency_type, 'Review and optimize process flow')
    
    def _get_expected_improvement(self, inefficiency_type):
        """Get expected improvement for each inefficiency type"""
        
        improvements = {
            'supervisor_approval_bottleneck': '30-50% reduction in approval time',
            'director_approval_bottleneck': '40-60% reduction in high-level approval time', 
            'excessive_rejections': '2-14 day reduction in rework cycles',
            'excessive_duration_international': '20-30% reduction in total process time',
            'excessive_duration_domestic': '40-60% reduction in total process time',
            'process_complexity': '15-25% reduction in administrative overhead',
            'late_submission': '80% reduction in late submissions'
        }
        
        return improvements.get(inefficiency_type, '10-20% general improvement')
    
    def label_dataset(self, features_df):
        """Label entire dataset of cases"""
        
        labeled_data = []
        
        print(f"🏷️  Labeling {len(features_df)} cases based on research findings...")
        
        for idx, row in features_df.iterrows():
            case_features = row.to_dict()
            
            # Generate labels
            labels = self.label_case_inefficiencies(case_features)
            
            # Generate recommendations
            recommendations = self.generate_optimization_recommendations(labels['inefficiencies'])
            
            # Combine everything
            labeled_case = {
                'case_id': case_features['case_id'],
                'input_features': case_features,
                'inefficiency_labels': labels,
                'optimization_recommendations': recommendations,
                'training_label': {
                    'has_inefficiencies': len(labels['inefficiencies']) > 0,
                    'severity_level': 'high' if labels['severity_score'] >= 5 else 'medium' if labels['severity_score'] >= 2 else 'low',
                    'primary_bottleneck': labels['inefficiencies'][0]['type'] if labels['inefficiencies'] else None,
                    'optimization_potential_percent': labels['optimization_potential']
                }
            }
            
            labeled_data.append(labeled_case)
        
        return labeled_data

def main():
    """Main execution for labeling"""
    
    print("🏷️  Starting Research-Based Labeling System")
    print("This will create training labels based on BPI Challenge 2020 research findings")
    
    labeler = ResearchBasedLabeler()
    
    # Process all feature files
    processed_dir = Path("data/processed")
    if not processed_dir.exists():
        print("❌ No processed features found. Please run data exploration first.")
        return
    
    all_labeled_data = []
    
    for feature_file in processed_dir.glob("*_features.csv"):
        print(f"\n📊 Processing {feature_file.name}")
        
        features_df = pd.read_csv(feature_file)
        labeled_data = labeler.label_dataset(features_df)
        
        # Save labeled data
        output_file = processed_dir / f"{feature_file.stem}_labeled.json"
        with open(output_file, 'w') as f:
            json.dump(labeled_data, f, indent=2, default=str)
        
        print(f"💾 Saved {len(labeled_data)} labeled cases to {output_file}")
        
        # Statistics
        inefficient_cases = sum(1 for case in labeled_data if case['training_label']['has_inefficiencies'])
        high_severity = sum(1 for case in labeled_data if case['training_label']['severity_level'] == 'high')
        
        print(f"📈 Dataset Statistics:")
        print(f"   - Total cases: {len(labeled_data)}")
        print(f"   - Inefficient cases: {inefficient_cases} ({inefficient_cases/len(labeled_data):.1%})")
        print(f"   - High severity: {high_severity} ({high_severity/len(labeled_data):.1%})")
        
        all_labeled_data.extend(labeled_data)
    
    # Save combined dataset
    combined_file = processed_dir / "combined_labeled_dataset.json"
    with open(combined_file, 'w') as f:
        json.dump(all_labeled_data, f, indent=2, default=str)
    
    print(f"\n✅ Labeling complete! Combined dataset saved to {combined_file}")
    print(f"📊 Total labeled cases: {len(all_labeled_data)}")
    
    return all_labeled_data

if __name__ == "__main__":
    main()