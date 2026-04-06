import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from env import EthicalHackerEnv, ActionType

load_dotenv()

# Pre-Submission Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-8B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN", "")

# Standard OpenAI client configuration (compatible with Hugging Face)
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

def run_task(task_id: str):
    env = EthicalHackerEnv(task_id=task_id)
    obs = env.reset()
    
    steps = 0
    total_rewards = []
    done = False
    
    # [START] STRICT FORMAT
    print(f"[START] task={task_id} env=ethical-hacker model={MODEL_NAME}", flush=True)
    
    while not done and steps < 10:
        steps += 1
        
        system_prompt = f"""
        Objective: {task_id.upper()}.
        The overall objective is: Discover a login vulnerability (scan), exploit it (' OR '1'='1), report it, and patch it.
        
        Available Actions: scan, inject_sql, login_normal, report, patch
        - scan: Find vulnerabilities.
        - inject_sql: Pass payload "' OR '1'='1" to login.
        - report: Ethical reporting.
        - patch: Mitigation (must report first).
        
        Current Instruction:
        - EASY: Find vulnerability (scan).
        - MEDIUM: Find and log in.
        - HARD: Find, log in, report, and patch.
        
        Provide response in JSON exactly: {{"action": "action_type", "payload": "optional_string"}}
        """

        try:
            # Reproducibility: Use temperature=0 to ensure deterministic model output
            response = client.chat.completions.create(
                model=MODEL_NAME, 
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Current Observation: {obs.model_dump_json()}"}
                ],
                temperature=0 
            )
            content = response.choices[0].message.content
            
            # Extract JSON cleanly for Llama-3 models
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            action_data = json.loads(content)
            
            # Step in environment
            obs, reward, done, info = env.step(action_data)
            total_rewards.append(reward)
            
            # [STEP] STRICT FORMAT COMPLIANCE
            # reward=0.20 (not 0.2), done=false (not False), error=null (not None)
            done_str = "true" if done else "false"
            err_msg = info.get("error", "null")
            error_val = "null" if err_msg in [None, "null", "None"] else str(err_msg).replace("\n", " ")
            
            print(f"[STEP] step={steps} action={action_data.get('action')} reward={reward:.2f} done={done_str} error={error_val}", flush=True)
            
        except Exception as e:
            # Handle model or environment failures gracefully without extra logs
            print(f"[STEP] step={steps} action=null reward=0.00 done=true error={str(e).replace('\n', ' ')}", flush=True)
            break

    # Final scoring and logging
    score = env.grader()
    rewards_str = ",".join([f"{r:.2f}" for r in total_rewards])
    # [END] STRICT FORMAT: success=true, score=1.00
    success_str = "true" if score >= 0.9 else "false"
    print(f"[END] success={success_str} steps={steps} score={score:.2f} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    for t in ["easy", "medium", "hard"]:
        run_task(t)
