import requests
import json
from pathlib import Path
import time

class FrameworkKnowledgeCollector:
    """
    Collect comprehensive Agile and Lean framework knowledge for AI training
    
    PURPOSE: Create a knowledge base that teaches AI agents:
    1. Agile Principles → Identify rigid, slow processes
    2. Lean Methodology → Spot waste and inefficiencies  
    3. Operating Model Design → How organizations should be structured
    4. Framework Applications → Apply these to real workflows
    5. Optimization Rules → Generate specific improvements
    """
    
    def __init__(self):
        self.knowledge_dir = Path("data/framework_knowledge")
        self.knowledge_dir.mkdir(parents=True, exist_ok=True)
        
    def collect_agile_manifesto(self):
        """Collect complete Agile Manifesto with operating model applications"""
        
        agile_manifesto = {
            "source": "Agile Manifesto",
            "url": "https://agilealliance.org/agile101/the-agile-manifesto/",
            "description": "Core Agile values and principles for organizational workflow optimization",
            
            "values": [
                {
                    "value": "Individuals and interactions over processes and tools",
                    "workflow_application": "Prioritize human communication and collaboration in approval processes",
                    "operating_model_impact": "Design approval hierarchies that enable direct communication between stakeholders",
                    "inefficiency_detection": "Look for processes that rely too heavily on systems instead of human judgment"
                },
                {
                    "value": "Working software over comprehensive documentation", 
                    "workflow_application": "Focus on functional workflows rather than excessive documentation",
                    "operating_model_impact": "Minimize bureaucratic overhead and focus on value-delivering activities",
                    "inefficiency_detection": "Identify processes with excessive documentation requirements that don't add value"
                },
                {
                    "value": "Customer collaboration over contract negotiation",
                    "workflow_application": "Enable direct stakeholder collaboration in travel approval processes",
                    "operating_model_impact": "Create structures that facilitate collaboration between internal customers and service providers",
                    "inefficiency_detection": "Spot processes that create adversarial relationships between departments"
                },
                {
                    "value": "Responding to change over following a plan",
                    "workflow_application": "Create adaptive workflows that can handle exceptions and changes",
                    "operating_model_impact": "Build flexible organizational structures that can adapt to changing business needs",
                    "inefficiency_detection": "Find rigid processes that break down when requirements change"
                }
            ],
            
            "principles": [
                {
                    "principle": "Our highest priority is to satisfy the customer through early and continuous delivery of valuable software",
                    "workflow_application": "Deliver approvals quickly and continuously rather than in batches",
                    "operating_model_application": "Design approval processes that provide immediate value to employees",
                    "measurement": "Time from request to approval, stakeholder satisfaction scores"
                },
                {
                    "principle": "Welcome changing requirements, even late in development",
                    "workflow_application": "Allow travel request modifications without starting over",
                    "operating_model_application": "Create change management processes that are efficient and user-friendly",
                    "measurement": "Percentage of requests that can be modified without restarting the process"
                },
                {
                    "principle": "Deliver working software frequently, from a couple of weeks to a couple of months",
                    "workflow_application": "Process approvals in hours/days, not weeks/months",
                    "operating_model_application": "Establish service level agreements that prioritize speed",
                    "measurement": "Average approval cycle time, percentage of approvals within SLA"
                },
                {
                    "principle": "Business people and developers must work together daily",
                    "workflow_application": "Travelers and approvers should have direct communication channels",
                    "operating_model_application": "Remove barriers between business units and support functions",
                    "measurement": "Frequency of direct stakeholder communication, resolution time for issues"
                },
                {
                    "principle": "Build projects around motivated individuals",
                    "workflow_application": "Empower employees to make appropriate travel decisions within guidelines",
                    "operating_model_application": "Design roles and responsibilities that leverage individual expertise",
                    "measurement": "Employee empowerment scores, decision-making authority levels"
                },
                {
                    "principle": "The most efficient and effective method of conveying information is face-to-face conversation",
                    "workflow_application": "Use real-time communication tools for approval discussions rather than email chains",
                    "operating_model_application": "Design communication protocols that prioritize direct interaction",
                    "measurement": "Communication effectiveness scores, time to resolution for complex issues"
                },
                {
                    "principle": "Working software is the primary measure of progress",
                    "workflow_application": "Measure success by completed approvals, not documentation or meetings",
                    "operating_model_application": "Focus metrics on business outcomes rather than activity measures",
                    "measurement": "Business outcome metrics vs. activity metrics ratio"
                },
                {
                    "principle": "Agile processes promote sustainable development",
                    "workflow_application": "Create workflows that don't overburden approvers or create burnout",
                    "operating_model_application": "Design workload distribution that maintains quality and employee wellbeing",
                    "measurement": "Employee satisfaction, workload balance, quality metrics"
                },
                {
                    "principle": "Continuous attention to technical excellence and good design enhances agility",
                    "workflow_application": "Continuously improve workflow design and automation capabilities",
                    "operating_model_application": "Invest in capabilities and systems that enhance organizational agility",
                    "measurement": "Process improvement frequency, system capability maturity"
                },
                {
                    "principle": "Simplicity--the art of maximizing the amount of work not done--is essential",
                    "workflow_application": "Eliminate unnecessary approval steps and redundant activities",
                    "operating_model_application": "Design lean organizational structures that minimize waste",
                    "measurement": "Process step count, value-added activity percentage"
                },
                {
                    "principle": "The best architectures, requirements, and designs emerge from self-organizing teams",
                    "workflow_application": "Allow teams to optimize their own travel approval processes within guidelines",
                    "operating_model_application": "Enable autonomous teams with clear boundaries and objectives",
                    "measurement": "Team autonomy scores, self-optimization frequency"
                },
                {
                    "principle": "At regular intervals, the team reflects on how to become more effective",
                    "workflow_application": "Regular retrospectives on travel approval process effectiveness",
                    "operating_model_application": "Build continuous improvement into organizational routines",
                    "measurement": "Retrospective frequency, improvement implementation rate"
                }
            ],
            
            "operating_model_design_principles": {
                "structure": "Flat hierarchies with clear decision rights",
                "governance": "Lightweight governance focused on outcomes",
                "processes": "Streamlined processes with built-in flexibility",
                "culture": "Collaborative culture that embraces change",
                "metrics": "Focus on business outcomes and customer satisfaction"
            }
        }
        
        # Save Agile knowledge
        with open(self.knowledge_dir / "agile_manifesto.json", 'w') as f:
            json.dump(agile_manifesto, f, indent=2)
        
        print("✅ Collected comprehensive Agile Manifesto knowledge")
        return agile_manifesto
    
    def collect_lean_principles(self):
        """Collect comprehensive Lean methodology with operating model applications"""
        
        lean_principles = {
            "source": "Lean Manufacturing / Toyota Production System",
            "description": "Lean methodology for eliminating waste and optimizing organizational workflows",
            
            "seven_wastes": [
                {
                    "waste": "Transportation",
                    "definition": "Unnecessary movement of materials or information",
                    "workflow_application": "Minimize handoffs between approval stages",
                    "travel_example": "Avoid routing approvals through unnecessary departments",
                    "operating_model_impact": "Design organizational structure to minimize information handoffs",
                    "detection_methods": ["Process mapping", "Handoff analysis", "Information flow tracking"],
                    "optimization_strategies": ["Consolidate roles", "Direct routing", "Eliminate intermediaries"]
                },
                {
                    "waste": "Inventory", 
                    "definition": "Excess materials or information waiting to be processed",
                    "workflow_application": "Reduce approval queues and backlogs",
                    "travel_example": "Don't let travel requests accumulate waiting for batch processing",
                    "operating_model_impact": "Balance capacity with demand to prevent bottlenecks",
                    "detection_methods": ["Queue analysis", "Work-in-progress tracking", "Capacity utilization"],
                    "optimization_strategies": ["Level loading", "Capacity planning", "Flow optimization"]
                },
                {
                    "waste": "Motion",
                    "definition": "Unnecessary movement of people",
                    "workflow_application": "Minimize clicks, screen changes, and system switching",
                    "travel_example": "Single interface for all travel approval activities",
                    "operating_model_impact": "Design workspaces and systems for efficiency",
                    "detection_methods": ["User journey mapping", "Time and motion studies", "System interaction analysis"],
                    "optimization_strategies": ["Interface consolidation", "Workflow automation", "Ergonomic design"]
                },
                {
                    "waste": "Waiting",
                    "definition": "Idle time waiting for the next process step",
                    "workflow_application": "Eliminate approval bottlenecks and delays",
                    "travel_example": "Automated approvals for standard requests under thresholds",
                    "operating_model_impact": "Balance resources and eliminate bottlenecks",
                    "detection_methods": ["Cycle time analysis", "Bottleneck identification", "Resource utilization"],
                    "optimization_strategies": ["Resource balancing", "Parallel processing", "Automation"]
                },
                {
                    "waste": "Overproduction",
                    "definition": "Producing more than what is needed",
                    "workflow_application": "Don't create unnecessary documentation or approvals",
                    "travel_example": "Avoid requiring multiple approvals for low-risk travel",
                    "operating_model_impact": "Right-size processes to actual requirements",
                    "detection_methods": ["Value analysis", "Requirement tracing", "Output utilization"],
                    "optimization_strategies": ["Just-in-time processing", "Demand-driven workflows", "Value stream focus"]
                },
                {
                    "waste": "Over-processing",
                    "definition": "More processing than required",
                    "workflow_application": "Eliminate redundant approval steps",
                    "travel_example": "Don't duplicate budget checks across multiple approval levels",
                    "operating_model_impact": "Streamline processes to essential activities only",
                    "detection_methods": ["Process analysis", "Value stream mapping", "Activity analysis"],
                    "optimization_strategies": ["Process consolidation", "Single point of truth", "Elimination of redundancy"]
                },
                {
                    "waste": "Defects",
                    "definition": "Errors requiring rework",
                    "workflow_application": "Prevent rejections through upfront validation",
                    "travel_example": "Pre-validate compliance before submission",
                    "operating_model_impact": "Build quality into processes from the start",
                    "detection_methods": ["Error tracking", "Rework analysis", "Quality metrics"],
                    "optimization_strategies": ["Error-proofing", "Upstream quality", "Prevention over correction"]
                }
            ],
            
            "lean_principles": [
                {
                    "principle": "Define Value",
                    "description": "Identify what creates value for the customer",
                    "workflow_application": "Focus on what travelers and approvers actually need",
                    "operating_model_application": "Align organizational activities with stakeholder value",
                    "implementation_steps": ["Customer voice analysis", "Value definition", "Non-value activity identification"],
                    "success_metrics": ["Customer satisfaction", "Value delivery time", "Value-added ratio"]
                },
                {
                    "principle": "Map the Value Stream",
                    "description": "Identify all steps in the process and eliminate waste",
                    "workflow_application": "Document entire approval workflow and eliminate non-value steps",
                    "operating_model_application": "Map end-to-end organizational processes",
                    "implementation_steps": ["Current state mapping", "Future state design", "Gap analysis"],
                    "success_metrics": ["Process efficiency", "Waste reduction", "Cycle time improvement"]
                },
                {
                    "principle": "Create Flow",
                    "description": "Make value-creating steps flow smoothly",
                    "workflow_application": "Eliminate bottlenecks and create smooth approval flow",
                    "operating_model_application": "Design organizational structure for optimal flow",
                    "implementation_steps": ["Bottleneck elimination", "Resource balancing", "Flow optimization"],
                    "success_metrics": ["Throughput improvement", "Flow efficiency", "Lead time reduction"]
                },
                {
                    "principle": "Establish Pull",
                    "description": "Only produce what is needed when it's needed",  
                    "workflow_application": "Process approvals based on actual demand, not batches",
                    "operating_model_application": "Align organizational capacity with actual demand",
                    "implementation_steps": ["Demand analysis", "Capacity planning", "Pull system design"],
                    "success_metrics": ["Inventory reduction", "Response time", "Capacity utilization"]
                },
                {
                    "principle": "Pursue Perfection",
                    "description": "Continuously improve the process",
                    "workflow_application": "Regular optimization of approval workflows based on data",
                    "operating_model_application": "Build continuous improvement into organizational DNA",
                    "implementation_steps": ["Performance monitoring", "Improvement identification", "Change implementation"],
                    "success_metrics": ["Improvement frequency", "Performance trends", "Innovation rate"]
                }
            ],
            
            "operating_model_applications": {
                "organizational_structure": "Lean organizational design minimizes layers and maximizes value flow",
                "process_design": "Eliminate waste from all organizational processes",
                "performance_management": "Focus metrics on flow, quality, and customer value",
                "continuous_improvement": "Build kaizen culture into daily operations",
                "leadership_philosophy": "Leaders as coaches and improvement facilitators"
            }
        }
        
        # Save Lean knowledge
        with open(self.knowledge_dir / "lean_principles.json", 'w') as f:
            json.dump(lean_principles, f, indent=2)
            
        print("✅ Collected comprehensive Lean principles knowledge")
        return lean_principles
    
    def collect_operating_model_frameworks(self):
        """Collect operating model design frameworks"""
        
        operating_model_frameworks = {
            "definition": "An operating model defines how an organization creates and delivers value through its structure, processes, governance, and capabilities",
            
            "mckinsey_organize_to_value": {
                "source": "McKinsey Organize to Value Framework",
                "description": "Comprehensive framework for designing high-performance operating models",
                "elements": [
                    {
                        "element": "Strategy & Direction",
                        "description": "Clear strategic direction and value proposition",
                        "workflow_application": "Align travel approval strategy with business objectives",
                        "implementation": "Define approval policies that support business strategy",
                        "metrics": ["Strategic alignment score", "Policy compliance", "Business objective achievement"]
                    },
                    {
                        "element": "Structure & Governance", 
                        "description": "Organizational structure and decision-making processes",
                        "workflow_application": "Define clear approval hierarchies and decision rights",
                        "implementation": "Create approval matrix with clear authority levels",
                        "metrics": ["Decision speed", "Clarity of roles", "Accountability measures"]
                    },
                    {
                        "element": "Processes & Systems",
                        "description": "Core business processes and supporting technology",
                        "workflow_application": "Standardize and optimize approval workflows",
                        "implementation": "Implement consistent approval processes with technology support",
                        "metrics": ["Process efficiency", "System utilization", "Automation rate"]
                    },
                    {
                        "element": "People & Culture",
                        "description": "Talent, skills, and organizational culture",
                        "workflow_application": "Train approvers and travelers on efficient processes",
                        "implementation": "Develop capabilities and culture that support efficient approvals",
                        "metrics": ["Employee satisfaction", "Capability maturity", "Culture health"]
                    },
                    {
                        "element": "Performance Management",
                        "description": "Metrics, incentives, and performance monitoring",
                        "workflow_application": "Measure and improve approval cycle times",
                        "implementation": "Implement KPIs and incentives that drive optimal behavior",
                        "metrics": ["KPI achievement", "Performance trends", "Incentive effectiveness"]
                    }
                ]
            },
            
            "target_operating_model_design": {
                "description": "Framework for designing future-state operating models",
                "components": [
                    {
                        "component": "Value Streams",
                        "description": "End-to-end processes that deliver value to customers",
                        "travel_application": "Map complete travel approval and reimbursement value stream",
                        "design_principles": ["Customer-centric", "End-to-end optimization", "Value focus"]
                    },
                    {
                        "component": "Organizational Structure",
                        "description": "How roles, responsibilities, and reporting relationships are organized",
                        "travel_application": "Design approval hierarchy that balances control with speed",
                        "design_principles": ["Span of control optimization", "Clear accountability", "Minimal layers"]
                    },
                    {
                        "component": "Governance Model",
                        "description": "Decision-making frameworks and oversight mechanisms",
                        "travel_application": "Create approval governance that ensures compliance and efficiency",
                        "design_principles": ["Risk-based decisions", "Appropriate oversight", "Delegation frameworks"]
                    },
                    {
                        "component": "Technology Architecture",
                        "description": "Systems and technology that enable the operating model",
                        "travel_application": "Implement travel systems that support streamlined approvals",
                        "design_principles": ["User experience focus", "Integration", "Automation where appropriate"]
                    },
                    {
                        "component": "Performance Framework",
                        "description": "Metrics and management systems that drive performance",
                        "travel_application": "KPIs that balance speed, compliance, and cost control",
                        "design_principles": ["Balanced scorecard", "Leading indicators", "Continuous improvement"]
                    }
                ]
            },
            
            "agile_operating_model": {
                "description": "Operating model design principles based on Agile methodology",
                "characteristics": [
                    "Cross-functional teams with end-to-end accountability",
                    "Rapid decision-making with appropriate governance",
                    "Continuous improvement and adaptation",
                    "Customer-centric value delivery",
                    "Technology-enabled collaboration and automation"
                ],
                "implementation_patterns": [
                    {
                        "pattern": "Squad Model",
                        "description": "Small, autonomous teams with clear missions",
                        "travel_application": "Dedicated travel approval squads for different business units"
                    },
                    {
                        "pattern": "Platform Model", 
                        "description": "Shared services and capabilities that enable agility",
                        "travel_application": "Common travel platform serving all business units"
                    },
                    {
                        "pattern": "Network Model",
                        "description": "Dynamic collaboration across organizational boundaries",
                        "travel_application": "Flexible approval networks based on expertise and availability"
                    }
                ]
            }
        }
        
        # Save operating model frameworks
        with open(self.knowledge_dir / "operating_model_frameworks.json", 'w') as f:
            json.dump(operating_model_frameworks, f, indent=2)
            
        print("✅ Collected operating model framework knowledge")
        return operating_model_frameworks
    
    
    def create_inefficiency_detection_rules(self):
        """Create comprehensive rules for detecting inefficiencies based on frameworks"""
        
        detection_rules = {
            "description": "Comprehensive rules for detecting workflow inefficiencies using Agile and Lean principles",
            
            "agile_violations": [
                {
                    "violation": "excessive_approval_layers",
                    "description": "Too many approval levels violates Agile 'simplicity' principle",
                    "detection_rule": "approval_levels > 3",
                    "threshold": "> 3 approval levels for standard requests",
                    "framework_basis": "Agile Principle: Simplicity - maximize work not done",
                    "optimization": "Consolidate approval levels, implement delegation rules",
                    "expected_improvement": "50-70% reduction in approval time"
                },
                {
                    "violation": "slow_feedback_loops", 
                    "description": "Long approval times violate 'early and continuous delivery' principle",
                    "detection_rule": "approval_time > 5_days",
                    "threshold": "> 5 days for standard approvals",
                    "framework_basis": "Agile Principle: Early and continuous delivery of value",
                    "optimization": "Implement real-time approval notifications, parallel processing",
                    "expected_improvement": "60-80% faster feedback cycles"
                },
                {
                    "violation": "inflexible_process",
                    "description": "Cannot handle changes/exceptions violates 'responding to change'",
                    "detection_rule": "change_requires_restart == true",
                    "threshold": "Process restarts required for minor changes",
                    "framework_basis": "Agile Value: Responding to change over following a plan",
                    "optimization": "Build flexibility into process design",
                    "expected_improvement": "90% reduction in process restarts"
                },
                {
                    "violation": "poor_collaboration",
                    "description": "Lack of direct communication violates 'individuals and interactions'",
                    "detection_rule": "direct_communication_rate < 0.3",
                    "threshold": "< 30% of approvals involve direct stakeholder communication",
                    "framework_basis": "Agile Value: Individuals and interactions over processes and tools",
                    "optimization": "Enable direct approver-traveler communication channels",
                    "expected_improvement": "40% faster issue resolution"
                }
            ],
            
            "lean_waste_detection": [
                {
                    "waste_type": "waiting",
                    "detection_rule": "queue_time > 2_days OR approval_bottleneck_identified",
                    "threshold": "> 2 days waiting in approval queue OR identified bottleneck",
                    "root_causes": ["Insufficient approver capacity", "Batch processing", "Resource imbalance"],
                    "optimization": "Increase approver capacity, implement continuous flow, balance resources",
                    "measurement": "Queue time reduction, throughput improvement"
                },
                {
                    "waste_type": "defects",
                    "detection_rule": "rejection_rate > 0.15 OR rework_cycles > 1",
                    "threshold": "> 15% rejection rate OR multiple rework cycles",
                    "root_causes": ["Unclear requirements", "Poor validation", "Inadequate training"],
                    "optimization": "Implement pre-validation, improve requirements clarity, enhance training",
                    "measurement": "First-pass yield, rejection rate reduction"
                },
                {
                    "waste_type": "overprocessing",
                    "detection_rule": "redundant_activities > 2 OR duplicate_approvals > 1",
                    "threshold": "> 2 redundant activities OR duplicate approval steps",
                    "root_causes": ["Process design flaws", "Lack of integration", "Compliance overkill"],
                    "optimization": "Consolidate approval steps, integrate systems, risk-based compliance",
                    "measurement": "Process step reduction, value-added ratio improvement"
                },
                {
                    "waste_type": "transportation",
                    "detection_rule": "handoff_count > 4 OR system_switches > 3",
                    "threshold": "> 4 handoffs OR > 3 system switches",
                    "root_causes": ["Poor process design", "System fragmentation", "Organizational silos"],
                    "optimization": "Reduce handoffs, integrate systems, cross-functional teams",
                    "measurement": "Handoff reduction, system integration score"
                },
                {
                    "waste_type": "inventory",
                    "detection_rule": "backlog_size > capacity_per_day * 3",
                    "threshold": "Backlog > 3 days of processing capacity",
                    "root_causes": ["Capacity constraints", "Demand variability", "Poor flow design"],
                    "optimization": "Capacity balancing, demand smoothing, flow optimization",
                    "measurement": "Backlog reduction, flow efficiency"
                },
                {
                    "waste_type": "motion",
                    "detection_rule": "user_clicks > 20 OR screen_changes > 8",
                    "threshold": "> 20 clicks OR > 8 screen changes per approval",
                    "root_causes": ["Poor user interface", "System complexity", "Workflow design"],
                    "optimization": "UI/UX improvement, workflow simplification, system consolidation",
                    "measurement": "User effort reduction, satisfaction scores"
                },
                {
                    "waste_type": "overproduction",
                    "detection_rule": "unused_approvals > 0.1 OR excessive_documentation == true",
                    "threshold": "> 10% of approvals unused OR excessive documentation requirements",
                    "root_causes": ["Poor demand forecasting", "Over-engineering", "Compliance overkill"],
                    "optimization": "Just-in-time approvals, right-size documentation, risk-based approach",
                    "measurement": "Utilization improvement, documentation efficiency"
                }
            ],
            
            "operating_model_violations": [
                {
                    "violation": "unclear_decision_rights",
                    "description": "Ambiguous approval authority creates delays and confusion",
                    "detection_rule": "approval_escalations > 0.2 OR authority_conflicts > 0",
                    "optimization": "Clear RACI matrix, delegation frameworks, authority limits",
                    "framework_basis": "Operating Model: Structure & Governance"
                },
                {
                    "violation": "misaligned_incentives",
                    "description": "Performance metrics don't encourage efficient approvals",
                    "detection_rule": "approval_speed_not_measured OR quality_only_focus",
                    "optimization": "Balanced scorecard with speed and quality metrics",
                    "framework_basis": "Operating Model: Performance Management"
                },
                {
                    "violation": "inadequate_capabilities",
                    "description": "Approvers lack skills or tools for efficient processing",
                    "detection_rule": "training_gap_identified OR system_limitations == true",
                    "optimization": "Capability development, system improvements, automation",
                    "framework_basis": "Operating Model: People & Capabilities"
                }
            ],
            
            "integrated_optimization_recommendations": {
                "high_rejection_rate": {
                    "agile_solution": "Implement fast feedback loops with pre-validation",
                    "lean_solution": "Eliminate defects through poka-yoke (error-proofing)",
                    "operating_model_solution": "Redesign process to prevent errors upstream",
                    "combined_approach": "Pre-validation + real-time feedback + upstream quality",
                    "expected_roi": "40-60% reduction in rework costs"
                },
                "approval_bottlenecks": {
                    "agile_solution": "Empower self-organizing teams with spending authority",
                    "lean_solution": "Eliminate waiting waste through resource balancing",
                    "operating_model_solution": "Implement escalation and delegation frameworks",
                    "combined_approach": "Empowered teams + balanced resources + clear escalation",
                    "expected_roi": "50-70% faster approval cycles"
                },
                "process_complexity": {
                    "agile_solution": "Maximize work not done (simplicity principle)",
                    "lean_solution": "Value stream mapping to eliminate non-value activities",
                    "operating_model_solution": "Process redesign focusing on value-added steps",
                    "combined_approach": "Simplification + waste elimination + value focus",
                    "expected_roi": "30-50% process efficiency improvement"
                }
            }
        }
        
        # Save detection rules
        with open(self.knowledge_dir / "inefficiency_detection_rules.json", 'w') as f:
            json.dump(detection_rules, f, indent=2)
            
        print("✅ Created comprehensive inefficiency detection rules")
        return detection_rules
    
    def create_training_prompts(self):
        """Create comprehensive prompt templates for AI training"""
        
        training_prompts = {
            "description": "Comprehensive prompt templates for training AI agents on workflow optimization",
            
            "workflow_analysis_prompt": """
You are an expert in Agile and Lean methodologies analyzing organizational workflows for optimization opportunities.

CONTEXT: You have been provided with workflow data from an organizational process that needs optimization.

WORKFLOW DATA:
{workflow_data}

ANALYSIS FRAMEWORK:
1. **Agile Principles Analysis**:
   - Evaluate against 4 Agile values and 12 principles
   - Focus on simplicity, fast feedback, collaboration, and adaptability
   - Identify violations of Agile principles

2. **Lean Methodology Analysis**:
   - Identify the 7 wastes: Transportation, Inventory, Motion, Waiting, Overproduction, Over-processing, Defects
   - Apply 5 Lean principles: Define Value, Map Value Stream, Create Flow, Establish Pull, Pursue Perfection
   - Calculate waste impact and optimization potential

3. **Operating Model Assessment**:
   - Evaluate structure, governance, processes, capabilities, and performance management
   - Identify misalignments between strategy and execution
   - Assess organizational design effectiveness

REQUIRED OUTPUT:
1. **Inefficiency Identification**: List specific inefficiencies with framework violations
2. **Root Cause Analysis**: Explain underlying causes using framework principles  
3. **Optimization Recommendations**: Provide specific, actionable improvements
4. **Expected Impact**: Quantify improvement potential with metrics
5. **Implementation Priority**: Rank recommendations by impact and feasibility

FORMAT: Provide structured JSON response with clear sections for each analysis area.
""",
            
            "optimization_recommendation_prompt": """
You are a process optimization expert generating specific improvement recommendations.

IDENTIFIED INEFFICIENCIES:
{inefficiencies}

ORGANIZATIONAL CONTEXT:
{organizational_context}

OPTIMIZATION FRAMEWORK:
Apply integrated Agile + Lean + Operating Model approach to generate recommendations that:

1. **Address Root Causes**: Target fundamental issues, not just symptoms
2. **Are Implementable**: Can be executed within 30-90 days with available resources
3. **Provide Measurable Value**: Include specific KPIs and expected improvements
4. **Consider Change Management**: Account for organizational readiness and adoption
5. **Align with Frameworks**: Consistent with Agile and Lean principles

FOR EACH RECOMMENDATION, PROVIDE:
- **Recommendation Title**: Clear, actionable statement
- **Implementation Steps**: Detailed execution plan with timeline
- **Expected ROI/Improvement**: Quantified benefits (time, cost, quality)
- **Risk Factors**: Potential challenges and mitigation strategies
- **Success Metrics**: KPIs to measure implementation success
- **Framework Alignment**: How it supports Agile/Lean principles
- **Resource Requirements**: People, technology, and budget needs

OUTPUT FORMAT: Structured recommendations prioritized by impact and feasibility.
""",
            
            "framework_alignment_assessment_prompt": """
Evaluate the following workflow optimization against established frameworks.

OPTIMIZATION RECOMMENDATION:
{optimization}

ASSESSMENT CRITERIA:

1. **Agile Manifesto Alignment** (1-10 scale):
   - Values: Individuals & interactions, Working software, Customer collaboration, Responding to change
   - Principles: All 12 Agile principles evaluation
   - Justification for each score

2. **Lean Methodology Alignment** (1-10 scale):
   - Waste Elimination: How well does it address the 7 wastes
   - Lean Principles: Application of 5 core Lean principles
   - Continuous Improvement: Built-in improvement mechanisms

3. **Operating Model Best Practices** (1-10 scale):
   - Structure & Governance: Clear roles and decision rights
   - Process Excellence: Streamlined, value-adding processes
   - Performance Management: Appropriate metrics and incentives
   - Capability Development: Skills and technology enablement

4. **Integration Assessment**:
   - How well do the recommendations work together
   - Potential conflicts or synergies
   - Overall coherence of the optimization approach

PROVIDE:
- Detailed scoring with justification
- Identification of gaps or misalignments
- Suggestions for improving framework alignment
- Overall assessment of optimization quality
""",
            
            "process_mining_analysis_prompt": """
You are analyzing process mining data to identify optimization opportunities.

PROCESS DATA:
{process_data}

ANALYSIS FOCUS:
1. **Process Discovery**: Identify actual process flows vs. intended design
2. **Conformance Checking**: Find deviations from standard processes
3. **Performance Analysis**: Measure cycle times, throughput, and bottlenecks
4. **Root Cause Analysis**: Determine why inefficiencies occur

FRAMEWORK APPLICATION:
- **Agile Lens**: Look for inflexibility, slow feedback, poor collaboration
- **Lean Lens**: Identify waste types and value stream inefficiencies
- **Operating Model Lens**: Assess structural and governance issues

OUTPUT REQUIREMENTS:
1. Process flow visualization insights
2. Quantified performance metrics
3. Bottleneck identification and impact
4. Deviation analysis with root causes
5. Optimization recommendations with expected impact
6. Implementation roadmap with priorities

Use data-driven insights to support all recommendations.
""",
            
            "stakeholder_impact_analysis_prompt": """
Analyze the stakeholder impact of proposed workflow optimizations.

OPTIMIZATION RECOMMENDATIONS:
{recommendations}

STAKEHOLDER GROUPS:
{stakeholder_groups}

ANALYSIS FRAMEWORK:
1. **Impact Assessment**: How each recommendation affects different stakeholders
2. **Change Readiness**: Stakeholder readiness for proposed changes
3. **Resistance Factors**: Potential sources of resistance and mitigation
4. **Success Factors**: What each stakeholder group needs for success

FOR EACH STAKEHOLDER GROUP, ANALYZE:
- Current pain points and how recommendations address them
- Benefits they will receive from the optimization
- Potential concerns or resistance factors
- Required support and change management approach
- Success measures from their perspective

PROVIDE:
- Stakeholder impact matrix
- Change management recommendations
- Communication strategy for each group
- Implementation sequencing based on stakeholder readiness
- Risk mitigation for stakeholder-related challenges
"""
        }
        
        # Save training prompts
        with open(self.knowledge_dir / "training_prompts.json", 'w') as f:
            json.dump(training_prompts, f, indent=2)
            
        print("✅ Created comprehensive training prompt templates")
        return training_prompts
    
    def collect_all_framework_knowledge(self):
        """Collect all framework knowledge in comprehensive format"""
        
        print("🧠 COLLECTING COMPREHENSIVE FRAMEWORK KNOWLEDGE")
        print("=" * 60)
        print("Creating complete knowledge base for AI-driven workflow optimization")
        print("This includes Agile, Lean, Operating Models, and integrated applications")
        print("=" * 60)
        
        knowledge = {}
        
        # Collect all frameworks
        print("\n1️⃣  Collecting Agile Manifesto & Principles...")
        knowledge['agile'] = self.collect_agile_manifesto()
        
        print("\n2️⃣  Collecting Lean Methodology & 7 Wastes...")
        knowledge['lean'] = self.collect_lean_principles()
        
        print("\n3️⃣  Collecting Operating Model Frameworks...")
        knowledge['operating_models'] = self.collect_operating_model_frameworks()
        
        print("\n4️⃣  Creating Inefficiency Detection Rules...")
        knowledge['detection_rules'] = self.create_inefficiency_detection_rules()
        
        print("\n5️⃣  Creating Training Prompt Templates...")
        knowledge['prompts'] = self.create_training_prompts()
        
        # Create comprehensive combined knowledge base
        combined_knowledge = {
            "metadata": {
                "creation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "version": "1.0",
                "description": "Complete framework knowledge base for AI-driven workflow optimization",
                "scope": "Agile, Lean, Operating Models, and integrated optimization approaches",
                "application": "Training AI agents for organizational workflow analysis and optimization"
            },
            
            "framework_summary": {
                "agile_principles": "12 principles focused on adaptability, collaboration, and value delivery",
                "lean_methodology": "7 wastes identification and 5 core principles for waste elimination", 
                "operating_models": "Comprehensive frameworks for organizational design and optimization",
                "integration": "Combined approach leveraging strengths of all methodologies"
            },
            
            "frameworks": knowledge,
            
            "usage_instructions": {
                "training_phase": {
                    "description": "Use this knowledge base to train AI agents on framework principles",
                    "implementation": "Include framework knowledge in training prompts and fine-tuning data",
                    "validation": "Test agent responses against framework principles for accuracy"
                },
                "inference_phase": {
                    "description": "Reference during workflow analysis to ensure framework alignment", 
                    "implementation": "Use detection rules and optimization patterns during analysis",
                    "quality_assurance": "Validate recommendations against framework best practices"
                },
                "optimization_phase": {
                    "description": "Apply these principles when generating improvement recommendations",
                    "implementation": "Use integrated optimization approaches for maximum impact",
                    "measurement": "Track improvement metrics aligned with framework goals"
                }
            },
            
            "integration_methodology": {
                "approach": "Synergistic application of Agile, Lean, and Operating Model principles",
                "benefits": "More comprehensive optimization than single-framework approaches",
                "implementation": "Layered analysis using all three frameworks simultaneously",
                "expected_outcomes": "30-70% improvement in organizational workflow efficiency"
            }
        }
        
        # Save complete knowledge base
        with open(self.knowledge_dir / "complete_framework_knowledge.json", 'w') as f:
            json.dump(combined_knowledge, f, indent=2)
        
        print(f"\n✅ FRAMEWORK KNOWLEDGE COLLECTION COMPLETE!")
        print("=" * 60)
        print(f"📁 Knowledge base location: {self.knowledge_dir}")
        print(f"📊 Framework components: {len(knowledge)}")
        print(f"🎯 Ready for AI agent training on workflow optimization")
        
        # Summary statistics
        total_principles = len(knowledge['agile']['principles'])
        total_wastes = len(knowledge['lean']['seven_wastes']) 
        total_detection_rules = len(knowledge['detection_rules']['agile_violations']) + len(knowledge['detection_rules']['lean_waste_detection'])
        
        print(f"\n📈 Knowledge Base Statistics:")
        print(f"   • Agile Principles: {total_principles}")
        print(f"   • Lean Wastes & Principles: {total_wastes} + 5")
        print(f"   • Detection Rules: {total_detection_rules}")
        print(f"   • Training Prompts: {len(knowledge['prompts'])}")
        print(f"   • Operating Model Components: Multiple frameworks")
        
        return combined_knowledge

def main():
    """Main execution for comprehensive framework collection"""
    
    collector = FrameworkKnowledgeCollector()
    knowledge_base = collector.collect_all_framework_knowledge()
    
    print(f"\n🚀 NEXT STEPS:")
    print("1. Run data_exploration.py to extract features from your BPI Challenge data")
    print("2. Run research_labeling.py to create training labels")
    print("3. Use this knowledge base to train your AI agents")
    print("4. Apply the integrated optimization approach to real workflows")
    
    return knowledge_base

if __name__ == "__main__":
    main()