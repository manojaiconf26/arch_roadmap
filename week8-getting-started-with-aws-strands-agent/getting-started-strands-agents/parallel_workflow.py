import concurrent.futures
import os
import json
from research_agent import research_topic
from data_processor_agent import process_data

def batch_processing_workflow(batch_tasks: list, output_dir: str = "batch_output") -> dict:
    """Execute parallel batch processing workflow"""
    print(f"\n=== Starting Batch Processing Workflow ===")
    print(f"Processing {len(batch_tasks)} tasks in parallel")
    
    # Create output directory directly
    os.makedirs(f"{output_dir}/research_results", exist_ok=True)
    os.makedirs(f"{output_dir}/processed_data", exist_ok=True)
    os.makedirs(f"{output_dir}/batch_files", exist_ok=True)
    
    # Execute tasks in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        future_to_task = {}
        
        for i, task in enumerate(batch_tasks):
            task_type = task.get("type", "research")
            
            if task_type == "research":
                future = executor.submit(execute_research_task, task, i, output_dir)
            elif task_type == "data_processing":
                future = executor.submit(execute_data_processing_task, task, i, output_dir)
            elif task_type == "file_processing":
                future = executor.submit(execute_file_processing_task, task, i, output_dir)
            else:
                continue
            
            future_to_task[future] = (task, i)
        
        # Collect results
        results = []
        for future in concurrent.futures.as_completed(future_to_task):
            task, task_id = future_to_task[future]
            try:
                result = future.result()
                result["task_id"] = task_id
                results.append(result)
                print(f"Completed task {task_id}: {task.get('type', 'unknown')}")
            except Exception as e:
                results.append({
                    "task_id": task_id,
                    "status": "error",
                    "error": str(e)
                })
                print(f"Failed task {task_id}: {str(e)}")
    
    # Save batch results summary directly
    batch_summary = create_batch_summary(results, batch_tasks)
    with open(f"{output_dir}/batch_summary.json", 'w', encoding='utf-8') as f:
        f.write(batch_summary)
    
    print(f"=== Batch Processing Workflow Completed ===\n")
    
    return {
        "status": "completed",
        "total_tasks": len(batch_tasks),
        "successful_tasks": len([r for r in results if r.get("status") == "completed"]),
        "failed_tasks": len([r for r in results if r.get("status") == "error"]),
        "results": results,
        "output_directory": output_dir
    }

def execute_research_task(task: dict, task_id: int, output_dir: str) -> dict:
    """Execute a research task"""
    topic = task.get("query", task.get("topic", "Unknown topic"))
    result = research_topic(topic)
    
    # Save individual result directly
    with open(f"{output_dir}/research_results/research_task_{task_id}.txt", 'w', encoding='utf-8') as f:
        f.write(str(result))
    
    return result

def execute_data_processing_task(task: dict, task_id: int, output_dir: str) -> dict:
    """Execute a data processing task"""
    result = process_data(task)
    
    # Save individual result directly
    with open(f"{output_dir}/processed_data/data_task_{task_id}.json", 'w', encoding='utf-8') as f:
        f.write(str(result))
    
    return result

def execute_file_processing_task(task: dict, task_id: int, output_dir: str) -> dict:
    """Execute a file processing task"""
    # Direct file operations
    operation = task.get("operation")
    if operation == "create_structure":
        base_path = task.get("base_path", "")
        structure = task.get("structure", [])
        for folder in structure:
            os.makedirs(f"{base_path}/{folder}", exist_ok=True)
        return {"status": "completed", "operation": operation}
    return {"status": "completed", "operation": operation}

def create_batch_summary(results: list, original_tasks: list) -> str:
    """Create summary of batch processing results"""
    summary = {
        "batch_processing_summary": {
            "total_tasks": len(original_tasks),
            "completed_tasks": len([r for r in results if r.get("status") == "completed"]),
            "failed_tasks": len([r for r in results if r.get("status") == "error"]),
            "task_breakdown": {
                "research_tasks": len([t for t in original_tasks if t.get("type") == "research"]),
                "data_processing_tasks": len([t for t in original_tasks if t.get("type") == "data_processing"]),
                "file_processing_tasks": len([t for t in original_tasks if t.get("type") == "file_processing"])
            },
            "results": results
        }
    }
    
    return json.dumps(summary, indent=2)

if __name__ == "__main__":
    # Example batch tasks
    sample_batch_tasks = [
        {"type": "research", "query": "Machine Learning trends 2024"},
        {"type": "research", "query": "Cloud Computing security"},
        {"type": "data_processing", "operation": "structure_findings", "findings": ["AI advancement", "Cloud adoption"], "format": "json"},
        {"type": "file_processing", "operation": "create_structure", "base_path": "test_output", "structure": ["logs", "reports"]}
    ]
    
    # Execute batch processing
    result = batch_processing_workflow(sample_batch_tasks, "batch_test_output")
    print("Batch Processing Result:", result)