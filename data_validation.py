import pandas as pd
import json
from pathlib import Path
import numpy as np

class DataValidationSuite:
    """
    Comprehensive validation suite for BPI Challenge 2020 data collection
    Validates data against published research findings for academic credibility
    """
    
    def __init__(self):
        self.data_dir = Path("data")
        self.processed_dir = self.data_dir / "processed"
        self.knowledge_dir = self.data_dir / "framework_knowledge"
        
        # Research benchmarks for validation (from published BPI Challenge 2020 papers)
        self.research_benchmarks = {
            'domestic_avg_duration': (8, 11),  # Research: 8-11 days normal
            'international_avg_duration': (66, 86),  # Research: 66-86 days normal
            'domestic_rejection_rate': 0.12,  # Research: 12% rejection rate
            'international_rejection_rate': 0.27,  # Research: 27% rejection rate
            'supervisor_approval_bottleneck': 39,  # Research: 39 days average
            'director_approval_bottleneck': 55,  # Research: 55 days average
            'domestic_success_rate': 0.9562,  # Research: 95.62% success rate
            'international_success_rate': 0.9594,  # Research: 95.94% success rate
        }
    
    def validate_data_download(self):
        """Validate that BPI Challenge data was downloaded correctly"""
        
        print("📥 VALIDATING DATA DOWNLOAD")
        print("=" * 40)
        
        expected_files = [
            "PermitLog.xes",
            "DomesticDeclarations.xes", 
            "InternationalDeclarations.xes",
            "PrepaidTravelCost.xes",
            "RequestForPayment.xes"
        ]
        
        # Expected file sizes (approximate, in MB)
        expected_sizes = {
            "PermitLog.xes": (30, 40),  # ~33.2 MB
            "DomesticDeclarations.xes": (18, 25),  # ~20.5 MB
            "InternationalDeclarations.xes": (25, 35),  # ~29.2 MB
            "PrepaidTravelCost.xes": (6, 10),  # ~7.8 MB
            "RequestForPayment.xes": (12, 18)  # ~15.2 MB
        }
        
        bpi_dir = self.data_dir / "bpi_challenge_2020"
        validation_results = {
            'download_complete': True,
            'file_details': {},
            'missing_files': [],
            'size_issues': []
        }
        
        print("Checking XES files:")
        for filename in expected_files:
            filepath = bpi_dir / filename
            if filepath.exists():
                size_mb = filepath.stat().st_size / (1024 * 1024)
                expected_range = expected_sizes.get(filename, (0, 100))
                
                size_ok = expected_range[0] <= size_mb <= expected_range[1]
                status = "✅" if size_ok else "⚠️"
                
                validation_results['file_details'][filename] = {
                    'size_mb': f"{size_mb:.1f}",
                    'size_ok': size_ok,
                    'expected_range': f"{expected_range[0]}-{expected_range[1]} MB"
                }
                
                print(f"  {status} {filename}: {size_mb:.1f} MB")
                
                if not size_ok:
                    validation_results['size_issues'].append(filename)
            else:
                validation_results['missing_files'].append(filename)
                validation_results['download_complete'] = False
                print(f"  ❌ Missing: {filename}")
        
        # Overall assessment
        if validation_results['download_complete'] and not validation_results['size_issues']:
            print("\n🎉 All files downloaded successfully with correct sizes!")
        elif validation_results['download_complete']:
            print(f"\n⚠️  Files downloaded but {len(validation_results['size_issues'])} have unexpected sizes")
        else:
            print(f"\n❌ {len(validation_results['missing_files'])} files missing")
        
        return validation_results
    
    def validate_feature_extraction(self):
        """Validate feature extraction results"""
        
        print("\n🔍 VALIDATING FEATURE EXTRACTION")
        print("=" * 40)
        
        validation_results = {
            'feature_files_found': 0,
            'total_cases': 0,
            'datasets': {},
            'feature_quality': {}
        }
        
        expected_features = [
            'case_id', 'total_duration_days', 'activity_count', 
            'unique_activities', 'has_rejections', 'rejection_count'
        ]
        
        for feature_file in self.processed_dir.glob("*_features.csv"):
            print(f"\n📊 Analyzing {feature_file.name}")
            
            try:
                df = pd.read_csv(feature_file)
                
                dataset_name = feature_file.stem.replace('_features', '')
                
                # Check required columns
                missing_features = [feat for feat in expected_features if feat not in df.columns]
                extra_features = [col for col in df.columns if col not in expected_features + ['is_international', 'activities_sequence', 'timestamps', 'approval_time_days']]
                
                dataset_stats = {
                    'case_count': len(df),
                    'avg_duration': df['total_duration_days'].mean() if 'total_duration_days' in df.columns else 0,
                    'avg_activities': df['activity_count'].mean() if 'activity_count' in df.columns else 0,
                    'rejection_rate': df['rejection_count'].mean() if 'rejection_count' in df.columns else 0,
                    'has_international': 'international' in dataset_name,
                    'missing_features': missing_features,
                    'data_quality_score': 1.0 - (len(missing_features) / len(expected_features))
                }
                
                validation_results['datasets'][dataset_name] = dataset_stats
                validation_results['total_cases'] += len(df)
                validation_results['feature_files_found'] += 1
                
                print(f"   Cases: {len(df):,}")
                print(f"   Avg Duration: {dataset_stats['avg_duration']:.1f} days")
                print(f"   Avg Activities: {dataset_stats['avg_activities']:.1f}")
                print(f"   Avg Rejections: {dataset_stats['rejection_rate']:.2f}")
                
                if missing_features:
                    print(f"   ⚠️  Missing features: {missing_features}")
                else:
                    print(f"   ✅ All required features present")
                
            except Exception as e:
                print(f"   ❌ Error analyzing {feature_file.name}: {e}")
        
        print(f"\n📈 FEATURE EXTRACTION SUMMARY:")
        print(f"   Total feature files: {validation_results['feature_files_found']}")
        print(f"   Total cases extracted: {validation_results['total_cases']:,}")
        
        return validation_results
    
    def validate_against_research_benchmarks(self):
        """Validate extracted data against published research findings"""
        
        print("\n🎯 VALIDATING AGAINST RESEARCH BENCHMARKS")
        print("=" * 50)
        print("Comparing your data to published BPI Challenge 2020 research")
        
        validation_results = {
            'benchmark_matches': {},
            'deviations': {},
            'overall_accuracy': 0,
            'research_credibility': 'unknown'
        }
        
        matches = 0
        total_benchmarks = 0
        
        # Validate domestic data
        domestic_file = self.processed_dir / "domestic_declarations_features.csv"
        if domestic_file.exists():
            print("\n🏠 DOMESTIC DECLARATIONS VALIDATION:")
            domestic_df = pd.read_csv(domestic_file)
            avg_domestic_duration = domestic_df['total_duration_days'].mean()
            
            # Validate domestic duration
            expected_range = self.research_benchmarks['domestic_avg_duration']
            within_range = expected_range[0] <= avg_domestic_duration <= expected_range[1]
            
            if within_range:
                validation_results['benchmark_matches']['domestic_duration'] = {
                    'actual': f"{avg_domestic_duration:.1f} days",
                    'expected': f"{expected_range[0]}-{expected_range[1]} days",
                    'status': 'MATCH'
                }
                matches += 1
                print(f"   ✅ Duration: {avg_domestic_duration:.1f} days (expected {expected_range[0]}-{expected_range[1]})")
            else:
                validation_results['deviations']['domestic_duration'] = {
                    'actual': f"{avg_domestic_duration:.1f} days",
                    'expected': f"{expected_range[0]}-{expected_range[1]} days",
                    'deviation': f"{((avg_domestic_duration - np.mean(expected_range)) / np.mean(expected_range) * 100):.1f}%"
                }
                print(f"   ❌ Duration: {avg_domestic_duration:.1f} days (expected {expected_range[0]}-{expected_range[1]})")
            
            total_benchmarks += 1
        
        # Validate international data
        international_file = self.processed_dir / "international_declarations_features.csv"
        if international_file.exists():
            print("\n🌍 INTERNATIONAL DECLARATIONS VALIDATION:")
            international_df = pd.read_csv(international_file)
            avg_international_duration = international_df['total_duration_days'].mean()
            
            # Validate international duration  
            expected_range = self.research_benchmarks['international_avg_duration']
            within_range = expected_range[0] <= avg_international_duration <= expected_range[1]
            
            if within_range:
                validation_results['benchmark_matches']['international_duration'] = {
                    'actual': f"{avg_international_duration:.1f} days",
                    'expected': f"{expected_range[0]}-{expected_range[1]} days",
                    'status': 'MATCH'
                }
                matches += 1
                print(f"   ✅ Duration: {avg_international_duration:.1f} days (expected {expected_range[0]}-{expected_range[1]})")
            else:
                validation_results['deviations']['international_duration'] = {
                    'actual': f"{avg_international_duration:.1f} days",
                    'expected': f"{expected_range[0]}-{expected_range[1]} days",
                    'deviation': f"{((avg_international_duration - np.mean(expected_range)) / np.mean(expected_range) * 100):.1f}%"
                }
                print(f"   ❌ Duration: {avg_international_duration:.1f} days (expected {expected_range[0]}-{expected_range[1]})")
            
            total_benchmarks += 1
        
        # Calculate overall accuracy
        if total_benchmarks > 0:
            accuracy = matches / total_benchmarks
            validation_results['overall_accuracy'] = accuracy
            
            if accuracy >= 0.8:
                validation_results['research_credibility'] = 'HIGH'
                print(f"\n🎉 EXCELLENT: {accuracy:.0%} match with published research!")
            elif accuracy >= 0.6:
                validation_results['research_credibility'] = 'MEDIUM'
                print(f"\n👍 GOOD: {accuracy:.0%} match with published research")
            else:
                validation_results['research_credibility'] = 'LOW'
                print(f"\n⚠️  CONCERN: Only {accuracy:.0%} match with published research")
        
        return validation_results
    
    def validate_labeling_quality(self):
        """Validate quality of generated labels"""
        
        print("\n🏷️  VALIDATING LABELING QUALITY")
        print("=" * 40)
        
        validation_results = {
            'labeled_files': 0,
            'total_labeled_cases': 0,
            'inefficiency_distribution': {},
            'label_consistency': True,
            'labeling_coverage': {}
        }
        
        for labeled_file in self.processed_dir.glob("*_labeled.json"):
            dataset_name = labeled_file.stem.replace('_labeled', '')
            print(f"\n🔍 Validating {dataset_name}:")
            
            try:
                with open(labeled_file) as f:
                    labeled_data = json.load(f)
                
                validation_results['labeled_files'] += 1
                validation_results['total_labeled_cases'] += len(labeled_data)
                
                # Analyze inefficiency distribution
                inefficient_cases = 0
                severity_distribution = {'high': 0, 'medium': 0, 'low': 0}
                
                for case in labeled_data:
                    inefficiencies = case.get('inefficiency_labels', {}).get('inefficiencies', [])
                    if inefficiencies:
                        inefficient_cases += 1
                    
                    # Track severity
                    severity = case.get('training_label', {}).get('severity_level', 'low')
                    severity_distribution[severity] += 1
                    
                    # Track inefficiency types
                    for inefficiency in inefficiencies:
                        inefficiency_type = inefficiency['type']
                        if inefficiency_type not in validation_results['inefficiency_distribution']:
                            validation_results['inefficiency_distribution'][inefficiency_type] = 0
                        validation_results['inefficiency_distribution'][inefficiency_type] += 1
                
                # Calculate coverage metrics
                inefficiency_rate = inefficient_cases / len(labeled_data) if labeled_data else 0
                validation_results['labeling_coverage'][dataset_name] = {
                    'total_cases': len(labeled_data),
                    'inefficient_cases': inefficient_cases,
                    'inefficiency_rate': inefficiency_rate,
                    'severity_distribution': severity_distribution
                }
                
                print(f"   Cases labeled: {len(labeled_data):,}")
                print(f"   Inefficient cases: {inefficient_cases:,} ({inefficiency_rate:.1%})")
                print(f"   Severity: High={severity_distribution['high']}, Med={severity_distribution['medium']}, Low={severity_distribution['low']}")
                
            except Exception as e:
                print(f"   ❌ Error validating {labeled_file.name}: {e}")
                validation_results['label_consistency'] = False
        
        # Overall labeling assessment
        total_inefficiency_types = len(validation_results['inefficiency_distribution'])
        print(f"\n📊 LABELING SUMMARY:")
        print(f"   Total labeled files: {validation_results['labeled_files']}")
        print(f"   Total labeled cases: {validation_results['total_labeled_cases']:,}")
        print(f"   Inefficiency types identified: {total_inefficiency_types}")
        
        if total_inefficiency_types >= 5:
            print("   ✅ Good variety of inefficiency patterns identified")
        else:
            print("   ⚠️  Limited variety of inefficiency patterns")
        
        return validation_results
    
    def validate_framework_knowledge(self):
        """Validate framework knowledge collection"""
        
        print("\n🧠 VALIDATING FRAMEWORK KNOWLEDGE")
        print("=" * 40)
        
        validation_results = {
            'knowledge_files': 0,
            'frameworks_covered': [],
            'completeness_score': 0,
            'content_quality': {}
        }
        
        expected_knowledge_files = [
            "agile_manifesto.json",
            "lean_principles.json", 
            "operating_model_frameworks.json",
            "inefficiency_detection_rules.json",
            "training_prompts.json",
            "complete_framework_knowledge.json"
        ]
        
        found_files = 0
        
        for filename in expected_knowledge_files:
            filepath = self.knowledge_dir / filename
            if filepath.exists():
                found_files += 1
                framework_name = filename.replace('.json', '')
                validation_results['frameworks_covered'].append(framework_name)
                
                # Check content quality
                try:
                    with open(filepath) as f:
                        content = json.load(f)
                    
                    content_size = len(json.dumps(content))
                    validation_results['content_quality'][framework_name] = {
                        'file_size_kb': content_size / 1024,
                        'has_content': content_size > 1000,  # At least 1KB of content
                        'structure_ok': isinstance(content, dict)
                    }
                    
                    print(f"   ✅ {filename} ({content_size/1024:.1f} KB)")
                    
                except Exception as e:
                    print(f"   ❌ {filename} (corrupted: {e})")
            else:
                print(f"   ❌ Missing: {filename}")
        
        validation_results['knowledge_files'] = found_files
        validation_results['completeness_score'] = found_files / len(expected_knowledge_files)
        
        # Assessment
        if validation_results['completeness_score'] >= 1.0:
            print("\n🎉 Complete framework knowledge base created!")
        elif validation_results['completeness_score'] >= 0.8:
            print(f"\n👍 Most framework knowledge collected ({validation_results['completeness_score']:.0%})")
        else:
            print(f"\n⚠️  Incomplete framework knowledge ({validation_results['completeness_score']:.0%})")
        
        return validation_results
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        
        print("\n" + "=" * 60)
        print("🔍 COMPREHENSIVE DATA VALIDATION REPORT")
        print("=" * 60)
        
        # Run all validations
        download_validation = self.validate_data_download()
        feature_validation = self.validate_feature_extraction()
        benchmark_validation = self.validate_against_research_benchmarks()
        labeling_validation = self.validate_labeling_quality()
        knowledge_validation = self.validate_framework_knowledge()
        
        # Calculate component scores
        scores = {
            'data_download': 1.0 if download_validation['download_complete'] and not download_validation['size_issues'] else 0.5 if download_validation['download_complete'] else 0.0,
            'feature_extraction': min(feature_validation['feature_files_found'] / 5, 1.0),  # Expect 5 feature files
            'research_alignment': benchmark_validation['overall_accuracy'],
            'labeling_quality': min(labeling_validation['labeled_files'] / 5, 1.0),  # Expect 5 labeled files
            'framework_knowledge': knowledge_validation['completeness_score']
        }
        
        overall_score = np.mean(list(scores.values()))
        
        print(f"\n📊 COMPONENT SCORES:")
        for component, score in scores.items():
            status = "✅" if score >= 0.8 else "⚠️" if score >= 0.6 else "❌"
            print(f"   {status} {component.replace('_', ' ').title()}: {score:.1%}")
        
        print(f"\n🎯 OVERALL VALIDATION SCORE: {overall_score:.1%}")
        
        # Overall assessment
        if overall_score >= 0.9:
            status = "EXCELLENT"
            message = "Data collection is complete and high quality. Ready for advanced AI training!"
            readiness = "READY_FOR_TRAINING"
        elif overall_score >= 0.7:
            status = "GOOD"
            message = "Data collection is solid with minor issues. Suitable for AI training."
            readiness = "READY_WITH_WARNINGS"
        elif overall_score >= 0.5:
            status = "ACCEPTABLE"
            message = "Data collection has issues but may be workable. Consider improvements."
            readiness = "NEEDS_IMPROVEMENT"
        else:
            status = "NEEDS_WORK"
            message = "Significant issues that should be addressed before proceeding."
            readiness = "NOT_READY"
        
        print(f"\n{status}: {message}")
        
        # Research credibility assessment
        research_credibility = benchmark_validation.get('research_credibility', 'unknown')
        if research_credibility == 'HIGH':
            print("🎓 HIGH RESEARCH CREDIBILITY: Your data closely matches published findings!")
        elif research_credibility == 'MEDIUM':
            print("📚 MEDIUM RESEARCH CREDIBILITY: Generally aligns with published research")
        elif research_credibility == 'LOW':
            print("⚠️  LOW RESEARCH CREDIBILITY: Significant deviation from published research")
        
        # Create comprehensive report
        report = {
            'validation_date': pd.Timestamp.now().isoformat(),
            'overall_score': overall_score,
            'status': status,
            'readiness': readiness,
            'research_credibility': research_credibility,
            'component_scores': scores,
            'detailed_results': {
                'download': download_validation,
                'features': feature_validation,
                'benchmarks': benchmark_validation,
                'labeling': labeling_validation,
                'knowledge': knowledge_validation
            },
            'recommendations': self._generate_recommendations(scores, overall_score)
        }
        
        # Save report
        report_file = self.data_dir / "validation_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n📁 Detailed validation report saved to: {report_file}")
        
        # Next steps
        print(f"\n🚀 RECOMMENDED NEXT STEPS:")
        if readiness == "READY_FOR_TRAINING":
            print("1. ✅ Proceed with AI agent development")
            print("2. ✅ Use your labeled dataset for training")
            print("3. ✅ Apply framework knowledge in agent prompts")
        elif readiness == "READY_WITH_WARNINGS":
            print("1. ⚠️  Review specific warnings above")
            print("2. ✅ Can proceed with AI training")
            print("3. ✅ Monitor for data quality issues")
        else:
            print("1. ❌ Address critical issues identified above")
            print("2. ❌ Re-run validation after fixes")
            print("3. ❌ Do not proceed with training until resolved")
        
        return report
    
    def _generate_recommendations(self, scores, overall_score):
        """Generate specific recommendations based on validation results"""
        
        recommendations = []
        
        if scores['data_download'] < 0.8:
            recommendations.append("Re-download missing or corrupted XES files from BPI Challenge 2020 repository")
        
        if scores['feature_extraction'] < 0.8:
            recommendations.append("Complete feature extraction for all 5 datasets")
        
        if scores['research_alignment'] < 0.7:
            recommendations.append("Investigate data processing issues - results should match published research")
        
        if scores['labeling_quality'] < 0.8:
            recommendations.append("Complete labeling process for all extracted features")
        
        if scores['framework_knowledge'] < 0.8:
            recommendations.append("Complete framework knowledge collection for comprehensive AI training")
        
        if overall_score >= 0.8:
            recommendations.append("Excellent work! Proceed with AI agent development and training")
        
        return recommendations

def main():
    """Main validation execution"""
    
    validator = DataValidationSuite()
    report = validator.generate_validation_report()
    
    return report

if __name__ == "__main__":
    main()