#!/usr/bin/env python3
"""
Strands Agents Multi-Agent System Demo

This demo showcases:
1. Sequential Content Creation Workflow
2. Parallel Batch Processing Workflow

Using 3 core tools:
- Web Search (simulated)
- File Operations
- Data Parser
"""

from sequential_workflow import content_creation_workflow
from parallel_workflow import batch_processing_workflow

def main():
    print("=" * 60)
    print("STRANDS AGENTS MULTI-AGENT SYSTEM DEMO")
    print("=" * 60)
    
    # Demo 1: Sequential Content Creation Workflow
    print("\n🔄 DEMO 1: SEQUENTIAL CONTENT CREATION WORKFLOW")
    print("-" * 50)
    
    topic = "Serverless Architecture on AWS"
    sequential_result = content_creation_workflow(topic, "demo_sequential_output")
    
    print(f"✅ Sequential workflow completed!")
    print(f"   Topic: {sequential_result['topic']}")
    print(f"   Files created: {len(sequential_result['files_created'])}")
    print(f"   Output directory: {sequential_result['output_directory']}")
    
    # Demo 2: Parallel Batch Processing Workflow
    print("\n⚡ DEMO 2: PARALLEL BATCH PROCESSING WORKFLOW")
    print("-" * 50)
    
    batch_tasks = [
        {
            "type": "research",
            "query": "AWS Lambda best practices"
        },
        {
            "type": "research", 
            "query": "Container orchestration with ECS"
        },
        {
            "type": "data_processing",
            "operation": "structure_findings",
            "findings": ["Microservices architecture", "Event-driven design", "Serverless patterns"],
            "format": "json"
        },
        {
            "type": "file_processing",
            "operation": "create_structure",
            "base_path": "demo_parallel_output/reports",
            "structure": ["research", "analysis", "summaries"]
        },
        {
            "type": "data_processing",
            "operation": "parse_data",
            "data": '{"service": "lambda", "benefits": ["cost-effective", "scalable"]}',
            "input_format": "json",
            "output_format": "json"
        }
    ]
    
    parallel_result = batch_processing_workflow(batch_tasks, "demo_parallel_output")
    
    print(f"✅ Parallel workflow completed!")
    print(f"   Total tasks: {parallel_result['total_tasks']}")
    print(f"   Successful: {parallel_result['successful_tasks']}")
    print(f"   Failed: {parallel_result['failed_tasks']}")
    print(f"   Output directory: {parallel_result['output_directory']}")
    
    # Summary
    print("\n📊 DEMO SUMMARY")
    print("-" * 50)
    print("✅ Sequential Workflow: Content Creation")
    print("   - Research Agent → Data Processor → File Manager")
    print("   - Linear execution with dependency chain")
    print("   - Use case: Comprehensive content generation")
    
    print("\n✅ Parallel Workflow: Batch Processing")
    print("   - Multiple agents working simultaneously")
    print("   - Concurrent execution with ThreadPoolExecutor")
    print("   - Use case: High-throughput data processing")
    
    print("\n🛠️  TOOLS USED:")
    print("   1. Web Search - Information gathering")
    print("   2. File Operations - Data persistence")
    print("   3. Data Parser - Format transformation")
    
    print("\n🏗️  ARCHITECTURE:")
    print("   - Strands Agents SDK for agent creation")
    print("   - Model-driven approach with tool integration")
    print("   - Production-ready patterns for AWS deployment")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()