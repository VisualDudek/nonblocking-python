import asyncio
from dataclasses import dataclass
from enum import Enum

class State(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class StepResult:
    state: State
    message: str
    data: dict = None

class SimpleWorkflow:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.current_state = State.PENDING
    
    async def step_1_validate(self) -> StepResult:
        print(f"🔍 Validating {self.task_id}...")
        
        # Simulate validation work and return result
        return await asyncio.sleep(1, result=StepResult(
            state=State.PROCESSING,
            message="Validation complete",
            data={"valid": True, "user_id": 123}
        ))
    
    async def step_2_process(self) -> StepResult:
        print(f"⚙️  Processing {self.task_id}...")
        
        # Simulate processing work and return result
        return await asyncio.sleep(2, result=StepResult(
            state=State.PROCESSING,
            message="Processing complete",
            data={"processed_items": 42, "duration": 2.1}
        ))
    
    async def step_3_finalize(self) -> StepResult:
        print(f"✅ Finalizing {self.task_id}...")
        
        # Simulate finalization and return result
        return await asyncio.sleep(0.5, result=StepResult(
            state=State.COMPLETED,
            message="Task completed successfully",
            data={"final_result": "SUCCESS", "task_id": self.task_id}
        ))
    
    async def run(self):
        """Execute the workflow"""
        print(f"\n🚀 Starting workflow: {self.task_id}")
        
        try:
            # Run each step and update state
            result1 = await self.step_1_validate()
            self.current_state = result1.state
            print(f"   ✓ {result1.message}")
            
            result2 = await self.step_2_process()  
            self.current_state = result2.state
            print(f"   ✓ {result2.message}")
            
            result3 = await self.step_3_finalize()
            self.current_state = result3.state
            print(f"   ✓ {result3.message}")
            
            return result3
            
        except Exception as e:
            self.current_state = State.FAILED
            print(f"   ❌ Failed: {e}")
            return StepResult(State.FAILED, f"Workflow failed: {e}")

# Example usage
async def main():
    # Single workflow
    workflow = SimpleWorkflow("TASK-001")
    final_result = await workflow.run()
    print(f"\nFinal state: {workflow.current_state.value}")
    print(f"Final data: {final_result.data}")
    
    print("\n" + "="*50)


    # Multiple concurrent workflows
    print("Running multiple workflows concurrently:")
    workflows = [SimpleWorkflow(f"TASK-{i:03d}") for i in range(2, 5)]
    
    results = await asyncio.gather(*[wf.run() for wf in workflows])
    
    print("\nResults:")
    for wf, result in zip(workflows, results):
        print(f"  {wf.task_id}: {result.state.value} - {result.message}")

if __name__ == "__main__":
    asyncio.run(main())