from engine import Engine

if __name__ == "__main__":
    initialized = False
    try:
        initialized = Engine.Initialize()
        if initialized:
            Engine.EngineRun()
    except KeyboardInterrupt:
        # Allow a clean user-initiated stop without dumping a traceback.
        print("\n--- Interrupted by user (Ctrl+C) ---")
    finally:
        if initialized:
            Engine.Shutdown()

