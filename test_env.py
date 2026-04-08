import asyncio
from env import EthicalHackerEnv, ActionType
import json

async def test_easy_task():
    print("\n--- Testing EASY Task (Find Vulnerability) ---")
    env = EthicalHackerEnv(task_id="easy")
    obs = await env.reset()
    
    # Action 1: Scan
    obs, reward, done, info = await env.step({"action": ActionType.SCAN})
    print(f"Action: SCAN | Reward: {reward} | Done: {done} | Found: {obs.found_vulnerability}")
    
    score = env.grader()
    print(f"Grader Score: {score}")
    assert score == 0.99
    assert done == True

async def test_medium_task():
    print("\n--- Testing MEDIUM Task (Exploit) ---")
    env = EthicalHackerEnv(task_id="medium")
    obs = await env.reset()
    
    # Action 1: Scan
    await env.step({"action": ActionType.SCAN})
    # Action 2: Inject SQL (Payload must match 'admin'--' for medium task)
    obs, reward, done, info = await env.step({"action": ActionType.INJECT_SQL, "payload": "admin'--"})
    print(f"Action: INJECT_SQL | Reward: {reward} | Done: {done} | Logged In: {obs.logged_in}")
    
    score = env.grader()
    print(f"Grader Score: {score}")
    assert score == 0.99
    assert done == True

async def test_hard_task():
    print("\n--- Testing HARD Task (Exploit + Report + Patch) ---")
    env = EthicalHackerEnv(task_id="hard")
    await env.reset()
    
    # 1. Scan
    await env.step({"action": ActionType.SCAN})
    # 2. Exploit (Payload must match '' AND SLEEP(5)--' for hard task)
    await env.step({"action": ActionType.INJECT_SQL, "payload": "' AND SLEEP(5)--"})
    # 3. Report
    _, r_report, _, _ = await env.step({"action": ActionType.REPORT})
    print(f"Action: REPORT | Reward: {r_report}")
    # 4. Patch
    obs, r_patch, done, _ = await env.step({"action": ActionType.PATCH})
    print(f"Action: PATCH | Reward: {r_patch} | Done: {done} | Patched: {obs.patched}")
    
    score = env.grader()
    print(f"Grader Score: {score}")
    assert score == 0.99
    assert done == True

async def main():
    try:
        await test_easy_task()
        await test_medium_task()
        await test_hard_task()
        print("\n✅ All unit tests PASSED. Environment logic is correct and deterministic.")
    except Exception as e:
        print(f"\n❌ Test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
