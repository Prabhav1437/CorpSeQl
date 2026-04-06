from env import EthicalHackerEnv, ActionType
import json

def test_easy_task():
    print("\n--- Testing EASY Task (Find Vulnerability) ---")
    env = EthicalHackerEnv(task_id="easy")
    obs = env.reset()
    
    # Action 1: Scan
    obs, reward, done, info = env.step({"action": ActionType.SCAN})
    print(f"Action: SCAN | Reward: {reward} | Done: {done} | Found: {obs.found_vulnerability}")
    
    score = env.grader()
    print(f"Grader Score: {score}")
    assert score == 1.0
    assert done == True

def test_medium_task():
    print("\n--- Testing MEDIUM Task (Exploit) ---")
    env = EthicalHackerEnv(task_id="medium")
    obs = env.reset()
    
    # Action 1: Scan
    env.step({"action": ActionType.SCAN})
    # Action 2: Inject SQL
    obs, reward, done, info = env.step({"action": ActionType.INJECT_SQL, "payload": "' OR '1'='1"})
    print(f"Action: INJECT_SQL | Reward: {reward} | Done: {done} | Logged In: {obs.logged_in}")
    
    score = env.grader()
    print(f"Grader Score: {score}")
    assert score == 1.0
    assert done == True

def test_hard_task():
    print("\n--- Testing HARD Task (Exploit + Report + Patch) ---")
    env = EthicalHackerEnv(task_id="hard")
    env.reset()
    
    # 1. Scan
    env.step({"action": ActionType.SCAN})
    # 2. Exploit
    env.step({"action": ActionType.INJECT_SQL, "payload": "' OR '1'='1"})
    # 3. Report
    _, r_report, _, _ = env.step({"action": ActionType.REPORT})
    print(f"Action: REPORT | Reward: {r_report}")
    # 4. Patch
    obs, r_patch, done, _ = env.step({"action": ActionType.PATCH})
    print(f"Action: PATCH | Reward: {r_patch} | Done: {done} | Patched: {obs.patched}")
    
    score = env.grader()
    print(f"Grader Score: {score}")
    assert score >= 0.99 # Should be 1.0 (0.33+0.33+0.34)
    assert done == True

if __name__ == "__main__":
    try:
        test_easy_task()
        test_medium_task()
        test_hard_task()
        print("\n✅ All unit tests PASSED. Environment logic is correct and deterministic.")
    except Exception as e:
        print(f"\n❌ Test FAILED: {str(e)}")
